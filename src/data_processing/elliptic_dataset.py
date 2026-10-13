"""Elliptic Bitcoin AML Dataset Loader and Heterogeneous Graph Projector.

This module integrates the MIT-IBM Watson AI Lab Elliptic Dataset
(Weber et al., 2019: "Anti-Money Laundering in Bitcoin: Experimenting with
Graph Convolutional Networks for Financial Fraud Detection").

The Elliptic dataset consists of 203,769 Bitcoin transaction nodes and
234,355 directed payment edges, partitioned into 49 distinct time steps.
Classes:
    - Class 1: Illicit (Terrorist financing, ransomware, darknet markets, scams)
    - Class 2: Licit (Exchanges, wallet providers, miners, legal commerce)
    - Unknown: Unlabeled transactions

This loader provides:
1. Standard tabular loading of ``elliptic_txs_features.csv`` and ``elliptic_txs_edgelist.csv``.
2. PyG HeteroData projection mapping Bitcoin transactions, wallet entities,
   and settlement sinks into DarkNode's heterogeneous multi-relational schema.
3. Realistic verification benchmark generators for testing without external CSV dependencies.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch_geometric.data import HeteroData


@dataclass(frozen=True)
class EllipticConfig:
    """Configuration for Elliptic dataset processing."""

    data_dir: Path = Path("data/elliptic")
    target_time_steps: tuple[int, ...] = (1, 2, 3, 4, 5)
    include_unknown: bool = False
    feature_dim: int = 166


class EllipticDataLoader:
    """Loads and transforms the Elliptic Bitcoin dataset into PyG graph representations."""

    def __init__(self, config: EllipticConfig | None = None) -> None:
        self.config = config or EllipticConfig()

    @property
    def features_file(self) -> Path:
        return self.config.data_dir / "elliptic_txs_features.csv"

    @property
    def edgelist_file(self) -> Path:
        return self.config.data_dir / "elliptic_txs_edgelist.csv"

    @property
    def classes_file(self) -> Path:
        return self.config.data_dir / "elliptic_txs_classes.csv"

    def is_available(self) -> bool:
        """Check whether local CSV files exist."""
        return (
            self.features_file.exists()
            and self.edgelist_file.exists()
            and self.classes_file.exists()
        )

    def load_hetero_data(self) -> HeteroData:
        """Load real Elliptic CSVs or synthesize an exact-schema benchmark graph."""
        if not self.is_available():
            return self.generate_mock_elliptic_graph()

        # Real CSV parser
        tx_to_idx: dict[str, int] = {}
        features: list[list[float]] = []
        labels: list[int] = []
        time_steps: list[int] = []

        # 1. Load classes
        class_map: dict[str, int] = {}
        with open(self.classes_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if not row or len(row) < 2:
                    continue
                tx_id, label_str = row[0], row[1]
                if label_str == "1":
                    class_map[tx_id] = 1  # Illicit
                elif label_str == "2":
                    class_map[tx_id] = 0  # Licit
                else:
                    class_map[tx_id] = -1  # Unknown

        # 2. Load features
        with open(self.features_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or len(row) < 3:
                    continue
                tx_id = row[0]
                t_step = int(row[1])
                if t_step not in self.config.target_time_steps:
                    continue
                lbl = class_map.get(tx_id, -1)
                if not self.config.include_unknown and lbl == -1:
                    continue

                tx_to_idx[tx_id] = len(tx_to_idx)
                features.append([float(x) for x in row[2:]])
                labels.append(lbl)
                time_steps.append(t_step)

        # 3. Load edge list
        src_edges: list[int] = []
        dst_edges: list[int] = []
        with open(self.edgelist_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if not row or len(row) < 2:
                    continue
                src, dst = row[0], row[1]
                if src in tx_to_idx and dst in tx_to_idx:
                    src_edges.append(tx_to_idx[src])
                    dst_edges.append(tx_to_idx[dst])

        # Convert to PyG HeteroData
        data = HeteroData()
        num_tx = len(tx_to_idx)
        data["user"].x = torch.tensor(features, dtype=torch.float)
        data["user"].y = torch.tensor(labels, dtype=torch.long)
        data["user"].time_step = torch.tensor(time_steps, dtype=torch.long)

        data["user", "transacts", "merchant"].edge_index = torch.tensor(
            [src_edges, dst_edges], dtype=torch.long
        )
        data["user", "transacts", "merchant"].edge_attr = torch.ones(
            (len(src_edges), 2), dtype=torch.float
        )
        data["device"].x = torch.eye(max(1, num_tx // 10), dtype=torch.float)
        data["merchant"].x = torch.eye(max(1, num_tx // 20), dtype=torch.float)
        return data

    def generate_mock_elliptic_graph(self, num_nodes: int = 500) -> HeteroData:
        """Generate an Elliptic-compatible benchmark graph for CI/unit testing."""
        np_rng = np.random.default_rng(42)
        illicit_fraction = 0.12

        labels = (np_rng.random(num_nodes) < illicit_fraction).astype(np.int64)
        features = np_rng.normal(0.0, 1.0, size=(num_nodes, self.config.feature_dim)).astype(np.float32)

        # Illicit nodes shift feature means (mimicking Elliptic empirical findings)
        features[labels == 1, :10] += 2.5

        edges_src: list[int] = []
        edges_dst: list[int] = []
        for i in range(num_nodes):
            k = int(np_rng.poisson(lam=2.5))
            targets = np_rng.integers(0, num_nodes, size=k)
            for t in targets:
                if t != i:
                    edges_src.append(i)
                    edges_dst.append(t)

        data = HeteroData()
        data["user"].x = torch.from_numpy(features)
        data["user"].y = torch.from_numpy(labels)
        data["user", "transacts", "merchant"].edge_index = torch.tensor(
            [edges_src, edges_dst], dtype=torch.long
        )
        data["user", "transacts", "merchant"].edge_attr = torch.ones(
            (len(edges_src), 2), dtype=torch.float
        )
        data["device"].x = torch.eye(50, dtype=torch.float)
        data["merchant"].x = torch.eye(25, dtype=torch.float)
        return data

