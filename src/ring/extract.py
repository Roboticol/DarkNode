"""Ring extraction and scoring for heterogeneous fraud detection graphs."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any

import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
import numpy as np
import torch
from torch import Tensor
from torch_geometric.data import HeteroData


def _normalize_node_key(node: Any) -> tuple[str, int | str]:
    """Normalize a node identifier into (type, id)."""
    if isinstance(node, tuple) and len(node) >= 2:
        return str(node[0]), node[1]
    if isinstance(node, str):
        if "_" in node:
            parts = node.split("_", 1)
            return parts[0], parts[1]
        return "user", node
    return "user", node


def _to_user_id(node: Any) -> int | str:
    """Extract the raw user ID from a node representation."""
    ntype, nid = _normalize_node_key(node)
    try:
        return int(nid)
    except (ValueError, TypeError):
        return nid


def _build_nx_from_hetero(data: HeteroData) -> nx.MultiDiGraph:
    """Build a MultiDiGraph from PyG HeteroData if nx_graph is not provided."""
    g = nx.MultiDiGraph()
    for ntype in data.node_types:
        num_nodes = data[ntype].num_nodes
        for i in range(num_nodes):
            g.add_node((ntype, i), node_type=ntype)

    for edge_type in data.edge_types:
        src_type, rel, dst_type = edge_type
        edge_index = data[edge_type].edge_index
        edge_attr = data[edge_type].get("edge_attr", None)
        for i in range(edge_index.shape[1]):
            src = (src_type, int(edge_index[0, i]))
            dst = (dst_type, int(edge_index[1, i]))
            attrs: dict[str, Any] = {"relation": rel}
            if edge_attr is not None:
                if edge_attr.shape[1] >= 1:
                    attrs["amount"] = float(edge_attr[i, 0])
                if edge_attr.shape[1] >= 2:
                    attrs["timestamp"] = float(edge_attr[i, 1])
            g.add_edge(src, dst, **attrs)
    return g


def extract_rings(
    data: HeteroData | dict[str, Any] | None = None,
    nx_graph: nx.Graph | nx.MultiDiGraph | None = None,
    user_scores: Tensor | np.ndarray | Sequence[float] | Mapping[Any, float] | None = None,
    threshold: float = 0.5,
    top_k: int | None = 10,
) -> list[dict[str, Any]]:
    """Extract, analyze, and rank fraud rings from a heterogeneous graph.

    Args:
        data: Optional PyG HeteroData object or dictionary containing 'data' and 'nx'.
        nx_graph: Optional NetworkX graph representing nodes and relations.
        user_scores: Optional fraud risk probabilities per user (defaults to 1.0).
        threshold: Score cutoff for identifying high-risk candidate users.
        top_k: Maximum number of ranked rings to return (or None for all).

    Returns:
        A list of ring dictionaries ranked by fraud ring risk score.
    """
    # 1. Parameter resolution
    if isinstance(data, dict):
        if nx_graph is None and "nx" in data:
            nx_graph = data["nx"]
        if "data" in data and not isinstance(data.get("data"), dict):
            data = data["data"]

    # In case arguments were swapped
    if isinstance(data, (nx.Graph, nx.MultiDiGraph)) and (
        nx_graph is None or isinstance(nx_graph, HeteroData)
    ):
        data, nx_graph = nx_graph, data

    if nx_graph is None:
        if isinstance(data, HeteroData):
            nx_graph = _build_nx_from_hetero(data)
        else:
            raise ValueError("Either nx_graph or HeteroData must be provided to extract_rings.")

    # 2. Extract user list and score mapping
    user_nodes = []
    for node, attrs in nx_graph.nodes(data=True):
        ntype, nid = _normalize_node_key(node)
        if ntype == "user" or attrs.get("node_type") == "user":
            user_nodes.append(node)

    # Resolve score mapping
    score_map: dict[Any, float] = {}
    if user_scores is not None:
        if isinstance(user_scores, Tensor):
            user_scores = user_scores.detach().cpu().numpy()
        if isinstance(user_scores, np.ndarray) or (
            isinstance(user_scores, Sequence) and not isinstance(user_scores, (str, bytes))
        ):
            for idx, s in enumerate(user_scores):
                score_map[idx] = float(s)
                score_map[("user", idx)] = float(s)
        elif isinstance(user_scores, Mapping):
            for k, v in user_scores.items():
                score_map[k] = float(v)
                score_map[_to_user_id(k)] = float(v)
    else:
        # Default all users to 1.0 if no external scores provided
        for u in user_nodes:
            score_map[u] = 1.0
            score_map[_to_user_id(u)] = 1.0

    # 3. Filter high-risk users
    high_risk_users = set()
    for u in user_nodes:
        uid = _to_user_id(u)
        score = score_map.get(u, score_map.get(uid, 0.0))
        if score >= threshold:
            high_risk_users.add(u)

    if not high_risk_users:
        return []

    # 4. Construct user connection graph for community detection
    user_g = nx.Graph()
    for u in high_risk_users:
        user_g.add_node(u)

    # Add edges between high-risk users sharing devices or IPs
    for u1 in high_risk_users:
        # Check all neighbors in nx_graph
        neighbors = set()
        if hasattr(nx_graph, "successors"):
            neighbors.update(nx_graph.successors(u1))
        if hasattr(nx_graph, "predecessors"):
            neighbors.update(nx_graph.predecessors(u1))
        if hasattr(nx_graph, "neighbors"):
            neighbors.update(nx_graph.neighbors(u1))

        for nbr in neighbors:
            ntype, _ = _normalize_node_key(nbr)
            if ntype == "device":
                # Find all users sharing this device
                dev_users = set()
                if hasattr(nx_graph, "predecessors"):
                    dev_users.update(nx_graph.predecessors(nbr))
                if hasattr(nx_graph, "successors"):
                    dev_users.update(nx_graph.successors(nbr))
                if hasattr(nx_graph, "neighbors"):
                    dev_users.update(nx_graph.neighbors(nbr))

                for other in dev_users:
                    if other in high_risk_users and other != u1:
                        prev_w = user_g.get_edge_data(u1, other, {}).get("weight", 0.0)
                        user_g.add_edge(u1, other, weight=prev_w + 3.0, reason="shared_device")

            elif ntype == "user" and nbr in high_risk_users and nbr != u1:
                prev_w = user_g.get_edge_data(u1, nbr, {}).get("weight", 0.0)
                user_g.add_edge(u1, nbr, weight=prev_w + 2.0, reason="shared_ip")

    # 5. Run community detection (greedy_modularity_communities)
    communities: list[set[Any]] = []
    # If the user graph has connected components
    for comp in nx.connected_components(user_g):
        if len(comp) < 2:
            continue
        sub = user_g.subgraph(comp)
        if sub.number_of_edges() > 0:
            try:
                comms = list(greedy_modularity_communities(sub, weight="weight"))
                for c in comms:
                    if len(c) >= 2:
                        communities.append(set(c))
                    else:
                        # Singletons from community detection within connected components
                        pass
            except Exception:
                communities.append(set(comp))
        else:
            communities.append(set(comp))

    # If no multi-user communities found, check if entire high_risk_users can form a group
    if not communities and len(high_risk_users) >= 2:
        communities = [set(high_risk_users)]

    # 6. Analyze and score each ring
    extracted_rings: list[dict[str, Any]] = []

    for ring_idx, comm in enumerate(communities):
        members = sorted(list(comm), key=lambda x: str(_to_user_id(x)))
        member_ids = [_to_user_id(m) for m in members]

        # Calculate average model score
        member_scores = [score_map.get(m, score_map.get(_to_user_id(m), 1.0)) for m in members]
        avg_model_score = float(np.mean(member_scores)) if member_scores else 0.0

        # Signals
        # 1. Shared device ratio
        user_devices: dict[Any, set[Any]] = {}
        for m in members:
            m_devs = set()
            m_nbrs = set()
            if hasattr(nx_graph, "neighbors"):
                m_nbrs.update(nx_graph.neighbors(m))
            if hasattr(nx_graph, "successors"):
                m_nbrs.update(nx_graph.successors(m))
            for nbr in m_nbrs:
                if _normalize_node_key(nbr)[0] == "device":
                    m_devs.add(nbr)
            user_devices[m] = m_devs

        device_user_counts: Counter[Any] = Counter()
        for devs in user_devices.values():
            for d in devs:
                device_user_counts[d] += 1

        shared_devices = {d for d, c in device_user_counts.items() if c > 1}
        members_sharing_device = sum(1 for devs in user_devices.values() if any(d in shared_devices for d in devs))
        shared_device_ratio = float(members_sharing_device / len(members)) if members else 0.0

        # 2. Shared IP pairs
        shared_ip_pairs = 0
        member_set = set(members)
        for i, m1 in enumerate(members):
            for m2 in members[i + 1 :]:
                has_ip_edge = False
                if nx_graph.has_edge(m1, m2):
                    edge_dict = nx_graph.get_edge_data(m1, m2)
                    if any("shared_ip" in str(data.get("relation", "")) or "ip" in data for data in (edge_dict.values() if isinstance(edge_dict, dict) else [edge_dict])):
                        has_ip_edge = True
                if not has_ip_edge and nx_graph.has_edge(m2, m1):
                    edge_dict = nx_graph.get_edge_data(m2, m1)
                    if any("shared_ip" in str(data.get("relation", "")) or "ip" in data for data in (edge_dict.values() if isinstance(edge_dict, dict) else [edge_dict])):
                        has_ip_edge = True
                if has_ip_edge:
                    shared_ip_pairs += 1

        # 3. Transaction velocity & timestamps
        tx_timestamps = []
        for m in members:
            out_edges = nx_graph.out_edges(m, data=True) if hasattr(nx_graph, "out_edges") else nx_graph.edges(m, data=True)
            for _, dst, edata in out_edges:
                if _normalize_node_key(dst)[0] == "merchant" or edata.get("relation") in ("transaction", "transacts"):
                    ts = edata.get("timestamp")
                    if ts is not None:
                        tx_timestamps.append(float(ts))

        if len(tx_timestamps) >= 2:
            span_seconds = max(tx_timestamps) - min(tx_timestamps)
            span_hours = max(span_seconds / 3600.0, 0.05)
            velocity = len(tx_timestamps) / span_hours
        elif len(tx_timestamps) == 1:
            velocity = 1.0
        else:
            velocity = 0.0

        # 4. Fresh accounts count
        fresh_accounts = 0
        for m in members:
            ndata = nx_graph.nodes[m] if m in nx_graph else {}
            if ndata.get("is_fresh") or ndata.get("fresh_account"):
                fresh_accounts += 1
            elif isinstance(data, HeteroData) and "user" in data.node_types:
                uid = _to_user_id(m)
                if isinstance(uid, int) and uid < data["user"].num_nodes:
                    # Synthetic graph sets user.x[:, 1] = 1.0 or user_id near start/end
                    pass

        # 5. Composite Weighted Ring Risk Score
        # Formula combines model score and behavioral graph signals
        s_model = avg_model_score
        s_device = shared_device_ratio
        max_possible_pairs = max(1, len(members) * (len(members) - 1) // 2)
        s_ip = min(shared_ip_pairs / max_possible_pairs, 1.0)
        s_velocity = min(velocity / 10.0, 1.0)  # >10 tx/hr is high velocity
        s_fresh = min(fresh_accounts / max(1, len(members)), 1.0)

        weighted_score = (
            0.35 * s_model +
            0.25 * s_device +
            0.20 * s_ip +
            0.15 * s_velocity +
            0.05 * s_fresh
        )
        final_score = round(float(np.clip(weighted_score, 0.0, 1.0)), 4)

        # 6. Extract visualization subgraph for frontend (vis-network format)
        vis_nodes = []
        vis_edges = []
        node_ids_added = set()

        # Add member user nodes
        for m in members:
            nid = f"user_{_to_user_id(m)}"
            node_ids_added.add(nid)
            vis_nodes.append({
                "id": nid,
                "label": f"User {_to_user_id(m)}",
                "group": "user",
                "title": f"Risk Score: {score_map.get(m, 1.0):.2f}",
                "value": score_map.get(m, 1.0),
            })

        # Add connected devices and merchants
        for m in members:
            m_nid = f"user_{_to_user_id(m)}"
            m_edges = nx_graph.out_edges(m, data=True) if hasattr(nx_graph, "out_edges") else nx_graph.edges(m, data=True)
            for _, dst, edata in m_edges:
                dtype, did = _normalize_node_key(dst)
                rel = edata.get("relation", "connected")
                dst_nid = f"{dtype}_{did}"

                if dtype in ("device", "merchant"):
                    if dst_nid not in node_ids_added:
                        node_ids_added.add(dst_nid)
                        vis_nodes.append({
                            "id": dst_nid,
                            "label": f"{dtype.capitalize()} {did}",
                            "group": dtype,
                            "title": f"Type: {dtype.capitalize()} | ID: {did}",
                        })
                    vis_edges.append({
                        "from": m_nid,
                        "to": dst_nid,
                        "label": rel,
                    })
                elif dtype == "user" and dst in member_set and str(m) < str(dst):
                    vis_edges.append({
                        "from": m_nid,
                        "to": dst_nid,
                        "label": rel,
                    })

        ring_entry = {
            "ring_id": ring_idx,
            "score": final_score,
            "member_count": len(members),
            "members": member_ids,
            "avg_model_score": round(avg_model_score, 4),
            "shared_device_ratio": round(shared_device_ratio, 4),
            "shared_device_pct": round(shared_device_ratio * 100.0, 1),
            "shared_ip_pairs": shared_ip_pairs,
            "transaction_velocity": round(velocity, 2),
            "fresh_account_count": fresh_accounts,
            "reason_signals": {
                "shared_device_pct": round(shared_device_ratio * 100.0, 1),
                "shared_ip_pairs": shared_ip_pairs,
                "transaction_velocity": round(velocity, 2),
                "fresh_accounts": fresh_accounts,
                "avg_model_score": round(avg_model_score, 4),
            },
            "graph": {
                "nodes": vis_nodes,
                "edges": vis_edges,
            },
        }
        extracted_rings.append(ring_entry)

    # Rank rings by score descending, then member count
    extracted_rings.sort(key=lambda r: (r["score"], r["member_count"]), reverse=True)
    for i, r in enumerate(extracted_rings):
        r["rank"] = i + 1

    if top_k is not None:
        return extracted_rings[:top_k]
    return extracted_rings

