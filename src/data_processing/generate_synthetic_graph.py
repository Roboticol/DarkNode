"""Generate a synthetic heterogeneous fraud-detection graph.

The generated graph contains:

* ``user``, ``merchant``, and ``device`` nodes.
* ``user -> merchant`` transaction edges.
* ``user <-> device`` shared-device edges.
* ``user <-> user`` shared-IP edges (the IP value is kept as an edge
  attribute so an additional IP node type is not required).

Fraud rings are injected as disjoint groups of users. Ring members share a
device and IP address, transact with a small merchant cohort, and generate
many transactions within a short time window. The resulting user and
transaction labels are ground truth for supervised MPNN experiments.

Example:
    python -m src.data_processing.generate_synthetic_graph --output data/fraud_graph.pt
"""

from __future__ import annotations

import argparse
import ipaddress
import random
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np
import torch
from torch_geometric.data import HeteroData


@dataclass(frozen=True)
class GeneratorConfig:
    """Parameters controlling synthetic graph generation."""

    num_users: int = 1_000
    num_merchants: int = 200
    num_devices: int = 800
    transactions_per_user: int = 12
    fraud_ring_fraction: float = 0.10
    ring_size: int = 8
    ring_transactions_per_user: int = 30
    ring_merchant_count: int = 4
    seed: int = 7


def _timestamp_to_epoch(value: datetime) -> float:
    return value.timestamp()


def _random_ip(rng: random.Random, index: int) -> str:
    """Return a deterministic private-range IP for an entity."""

    # 10.0.0.0/8 provides enough addresses for the requested synthetic scale.
    return str(ipaddress.IPv4Address((10 << 24) + index + rng.randrange(1, 256)))


def _add_transaction(
    graph: nx.MultiDiGraph,
    transactions: list[dict[str, Any]],
    user_id: int,
    merchant_id: int,
    timestamp: datetime,
    amount: float,
    is_fraud: bool,
    ring_id: int,
    transaction_id: int,
) -> None:
    """Add one transaction to NetworkX and the tabular transaction buffer."""

    graph.add_edge(
        ("user", user_id),
        ("merchant", merchant_id),
        key=f"transaction-{transaction_id}",
        relation="transaction",
        amount=amount,
        timestamp=_timestamp_to_epoch(timestamp),
        is_fraud=is_fraud,
        ring_id=ring_id,
    )
    transactions.append(
        {
            "user_id": user_id,
            "merchant_id": merchant_id,
            "amount": amount,
            "timestamp": _timestamp_to_epoch(timestamp),
            "is_fraud": int(is_fraud),
            "ring_id": ring_id,
        }
    )


def generate_synthetic_graph(
    config: GeneratorConfig | None = None,
) -> tuple[HeteroData, nx.MultiDiGraph, dict[str, Any]]:
    """Generate a PyG ``HeteroData`` object and its NetworkX source graph.

    Args:
        config: Generation parameters. Defaults to :class:`GeneratorConfig`.

    Returns:
        A tuple containing the model-ready PyG graph, the NetworkX graph used
        to construct it, and metadata including fraud-ring membership.
    """

    config = config or GeneratorConfig()
    if config.num_users < config.ring_size:
        raise ValueError("num_users must be at least ring_size")
    if config.num_merchants < config.ring_merchant_count:
        raise ValueError("num_merchants must be at least ring_merchant_count")
    if config.num_devices < 1:
        raise ValueError("num_devices must be positive")
    if not 0 < config.fraud_ring_fraction <= 1:
        raise ValueError("fraud_ring_fraction must be between 0 and 1")
    if config.ring_size < 2:
        raise ValueError("ring_size must be at least 2")
    if config.ring_merchant_count < 1:
        raise ValueError("ring_merchant_count must be positive")

    rng = random.Random(config.seed)
    np_rng = np.random.default_rng(config.seed)
    graph = nx.MultiDiGraph()
    start_time = datetime(2025, 1, 1, tzinfo=timezone.utc)

    for user_id in range(config.num_users):
        graph.add_node(("user", user_id), node_type="user")
    for merchant_id in range(config.num_merchants):
        graph.add_node(("merchant", merchant_id), node_type="merchant")
    for device_id in range(config.num_devices):
        graph.add_node(("device", device_id), node_type="device")

    user_ips: dict[int, str] = {}
    user_devices: dict[int, int] = {}
    for user_id in range(config.num_users):
        device_id = rng.randrange(config.num_devices)
        user_devices[user_id] = device_id
        user_ips[user_id] = _random_ip(rng, user_id)
        graph.add_edge(
            ("user", user_id),
            ("device", device_id),
            relation="shared_device",
        )

    # Create normal user-to-user shared-IP relationships by assigning a small
    # number of users to each synthetic IP, then inject ring-specific IPs below.
    for user_id in range(0, config.num_users - 1, 5):
        shared_ip = _random_ip(rng, config.num_users + user_id)
        for member in range(user_id, min(user_id + 5, config.num_users)):
            user_ips[member] = shared_ip
        members = list(range(user_id, min(user_id + 5, config.num_users)))
        for left_index, left in enumerate(members):
            for right in members[left_index + 1 :]:
                graph.add_edge(
                    ("user", left),
                    ("user", right),
                    relation="shared_ip",
                    ip=shared_ip,
                )
                graph.add_edge(
                    ("user", right),
                    ("user", left),
                    relation="shared_ip",
                    ip=shared_ip,
                )

    ring_user_count = max(config.ring_size, int(config.num_users * config.fraud_ring_fraction))
    ring_count = max(1, ring_user_count // config.ring_size)
    if ring_count > config.num_devices:
        raise ValueError("num_devices must be at least the number of fraud rings")
    ring_users = list(range(ring_user_count))
    transactions: list[dict[str, Any]] = []
    fraud_user_labels = np.zeros(config.num_users, dtype=np.int64)
    ring_ids = np.full(config.num_users, -1, dtype=np.int64)
    transaction_id = 0

    for ring_id in range(ring_count):
        members = ring_users[ring_id * config.ring_size : (ring_id + 1) * config.ring_size]
        if len(members) < config.ring_size:
            break
        fraud_user_labels[members] = 1
        ring_ids[members] = ring_id
        ring_device = config.num_devices - 1 - ring_id
        ring_ip = _random_ip(rng, 1_000_000 + ring_id)
        merchant_pool = [
            (ring_id * config.ring_merchant_count + offset) % config.num_merchants
            for offset in range(config.ring_merchant_count)
        ]

        for member in members:
            graph.add_edge(
                ("user", member),
                ("device", ring_device),
                relation="shared_device",
                is_fraud=True,
                ring_id=ring_id,
            )
            user_devices[member] = ring_device
            user_ips[member] = ring_ip

        for left_index, left in enumerate(members):
            for right in members[left_index + 1 :]:
                graph.add_edge(
                    ("user", left),
                    ("user", right),
                    relation="shared_ip",
                    ip=ring_ip,
                    is_fraud=True,
                    ring_id=ring_id,
                )
                graph.add_edge(
                    ("user", right),
                    ("user", left),
                    relation="shared_ip",
                    ip=ring_ip,
                    is_fraud=True,
                    ring_id=ring_id,
                )

        # Close timestamps create an anomalously high transaction velocity.
        for member in members:
            for transaction_offset in range(config.ring_transactions_per_user):
                timestamp = start_time + timedelta(
                    hours=ring_id,
                    minutes=transaction_offset // 3,
                    seconds=transaction_offset % 3,
                )
                _add_transaction(
                    graph,
                    transactions,
                    member,
                    rng.choice(merchant_pool),
                    timestamp,
                    float(np_rng.lognormal(mean=3.4, sigma=0.35)),
                    True,
                    ring_id,
                    transaction_id,
                )
                transaction_id += 1

    for user_id in range(ring_user_count, config.num_users):
        for _ in range(config.transactions_per_user):
            timestamp = start_time + timedelta(
                days=rng.randrange(90),
                minutes=rng.randrange(24 * 60),
            )
            _add_transaction(
                graph,
                transactions,
                user_id,
                rng.randrange(config.num_merchants),
                timestamp,
                float(np_rng.lognormal(mean=3.0, sigma=0.8)),
                False,
                -1,
                transaction_id,
            )
            transaction_id += 1

    data = HeteroData()
    data["user"].x = torch.tensor(
        [
            [user_id / max(config.num_users - 1, 1), 1.0]
            for user_id in range(config.num_users)
        ],
        dtype=torch.float,
    )
    data["user"].y = torch.from_numpy(fraud_user_labels)
    data["user"].ring_id = torch.from_numpy(ring_ids)
    data["merchant"].x = torch.eye(config.num_merchants, dtype=torch.float)
    data["device"].x = torch.eye(config.num_devices, dtype=torch.float)

    transaction_rows = transactions
    data["user", "transacts", "merchant"].edge_index = torch.tensor(
        [
            [row["user_id"] for row in transaction_rows],
            [row["merchant_id"] for row in transaction_rows],
        ],
        dtype=torch.long,
    )
    data["user", "transacts", "merchant"].edge_attr = torch.tensor(
        [
            [row["amount"], row["timestamp"]]
            for row in transaction_rows
        ],
        dtype=torch.float,
    )
    data["user", "transacts", "merchant"].y = torch.tensor(
        [row["is_fraud"] for row in transaction_rows], dtype=torch.long
    )

    shared_device_edges = [
        (source[1], target[1])
        for source, target, edge_data in graph.edges(data=True)
        if edge_data["relation"] == "shared_device"
    ]
    data["user", "uses", "device"].edge_index = torch.tensor(
        shared_device_edges, dtype=torch.long
    ).t().contiguous()

    shared_ip_edges = [
        (source[1], target[1])
        for source, target, edge_data in graph.edges(data=True)
        if edge_data["relation"] == "shared_ip"
    ]
    data["user", "shares_ip", "user"].edge_index = torch.tensor(
        shared_ip_edges, dtype=torch.long
    ).t().contiguous()

    graph_metadata = {
        "seed": config.seed,
        "num_fraud_rings": ring_count,
        "fraud_user_fraction": float(fraud_user_labels.mean()),
        "transaction_count": len(transactions),
        "fraud_transaction_count": sum(row["is_fraud"] for row in transactions),
    }
    metadata = {
        **graph_metadata,
        "ring_members": {
            ring_id: [user_id for user_id in range(config.num_users) if ring_ids[user_id] == ring_id]
            for ring_id in range(ring_count)
        },
        "user_devices": user_devices,
        "user_ips": user_ips,
    }
    return data, graph, metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/synthetic_fraud_graph.pt"))
    parser.add_argument("--users", type=int, default=GeneratorConfig.num_users)
    parser.add_argument("--merchants", type=int, default=GeneratorConfig.num_merchants)
    parser.add_argument("--devices", type=int, default=GeneratorConfig.num_devices)
    parser.add_argument("--fraud-ring-fraction", type=float, default=GeneratorConfig.fraud_ring_fraction)
    parser.add_argument("--ring-size", type=int, default=GeneratorConfig.ring_size)
    parser.add_argument("--seed", type=int, default=GeneratorConfig.seed)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = GeneratorConfig(
        num_users=args.users,
        num_merchants=args.merchants,
        num_devices=args.devices,
        fraud_ring_fraction=args.fraud_ring_fraction,
        ring_size=args.ring_size,
        seed=args.seed,
    )
    data, graph, metadata = generate_synthetic_graph(config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"data": data, "nx": graph, "metadata": metadata}, args.output)
    print(
        f"Saved {metadata['transaction_count']} transactions, "
        f"{metadata['num_fraud_rings']} fraud rings, and "
        f"{metadata['fraud_transaction_count']} fraud transactions to {args.output}"
    )


if __name__ == "__main__":
    main()
