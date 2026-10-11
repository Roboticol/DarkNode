"""Unit test and self-check for ring extraction on a synthetic 3-node fraud ring."""

from datetime import datetime, timezone
import networkx as nx
import pytest
import torch
from torch_geometric.data import HeteroData

from src.ring.extract import extract_rings


def test_obvious_three_node_ring() -> None:
    # 1. Build NetworkX graph
    nx_graph = nx.MultiDiGraph()

    # 3 user nodes, 1 shared device, 1 merchant
    for u in (0, 1, 2):
        nx_graph.add_node(("user", u), node_type="user")
    nx_graph.add_node(("device", 0), node_type="device")
    nx_graph.add_node(("merchant", 0), node_type="merchant")

    # Obvious shared device among all 3 users
    for u in (0, 1, 2):
        nx_graph.add_edge(("user", u), ("device", 0), relation="shared_device")

    # Obvious shared IP between pairs
    shared_ip = "192.168.1.100"
    nx_graph.add_edge(("user", 0), ("user", 1), relation="shared_ip", ip=shared_ip)
    nx_graph.add_edge(("user", 1), ("user", 2), relation="shared_ip", ip=shared_ip)
    nx_graph.add_edge(("user", 0), ("user", 2), relation="shared_ip", ip=shared_ip)

    # High transaction velocity: 15 transactions in 1 minute
    start_ts = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc).timestamp()
    for u in (0, 1, 2):
        for tx_idx in range(5):
            nx_graph.add_edge(
                ("user", u),
                ("merchant", 0),
                relation="transaction",
                amount=100.0,
                timestamp=start_ts + tx_idx * 5,
            )

    # 2. Build minimal PyG HeteroData representation
    data = HeteroData()
    data["user"].num_nodes = 3
    data["user"].x = torch.ones((3, 4), dtype=torch.float)
    data["user"].y = torch.ones(3, dtype=torch.long)
    data["device"].num_nodes = 1
    data["merchant"].num_nodes = 1

    data["user", "uses", "device"].edge_index = torch.tensor(
        [[0, 1, 2], [0, 0, 0]], dtype=torch.long
    )
    data["user", "shares_ip", "user"].edge_index = torch.tensor(
        [[0, 1, 0, 1, 2, 2], [1, 0, 2, 2, 1, 0]], dtype=torch.long
    )

    tx_sources = []
    tx_merchants = []
    tx_attrs = []
    for u in (0, 1, 2):
        for tx_idx in range(5):
            tx_sources.append(u)
            tx_merchants.append(0)
            tx_attrs.append([100.0, start_ts + tx_idx * 5])

    data["user", "transacts", "merchant"].edge_index = torch.tensor(
        [tx_sources, tx_merchants], dtype=torch.long
    )
    data["user", "transacts", "merchant"].edge_attr = torch.tensor(
        tx_attrs, dtype=torch.float
    )

    # 3. Run extract_rings
    user_scores = [0.95, 0.98, 0.92]
    rings = extract_rings(data=data, nx_graph=nx_graph, user_scores=user_scores)

    # 4. Assertions
    assert len(rings) >= 1, "Should detect at least 1 fraud ring"
    top_ring = rings[0]

    # Verify right members found
    assert set(top_ring["members"]) == {0, 1, 2}, f"Expected members {0, 1, 2}, got {top_ring['members']}"

    # Verify score is above 0.5
    assert top_ring["score"] > 0.5, f"Expected score > 0.5, got {top_ring['score']}"
    assert top_ring["shared_device_pct"] == 100.0
    assert top_ring["shared_ip_pairs"] >= 2
    assert top_ring["transaction_velocity"] > 5.0

