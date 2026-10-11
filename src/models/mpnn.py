"""Heterogeneous message-passing model with transaction-velocity features."""

from __future__ import annotations

from collections.abc import Mapping

import torch
from torch import Tensor, nn
from torch_geometric.data import HeteroData
from torch_geometric.nn import HeteroConv, SAGEConv
from torch_geometric.utils import scatter


class TransactionVelocity(nn.Module):
    """Encode per-user transaction count and rate over the observed time span."""

    def __init__(self, output_dim: int) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(2, output_dim),
            nn.ReLU(),
            nn.Linear(output_dim, output_dim),
        )

    def forward(self, data: HeteroData, num_users: int    ) -> Tensor:
        edge_type = ("user", "transacts", "merchant")
        edge_store = data[edge_type]
        source_users = edge_store.edge_index[0]
        if "edge_attr" not in edge_store or edge_store.edge_attr.shape[1] < 2:
            return self.network(
                torch.zeros(
                    (num_users, 2),
                    dtype=data["user"].x.dtype,
                    device=data["user"].x.device,
                )
            )
        timestamps = edge_store.edge_attr[:, 1]
        count = scatter(
            torch.ones_like(timestamps),
            source_users,
            dim=0,
            dim_size=num_users,
            reduce="sum",
        )
        if timestamps.numel():
            earliest = scatter(
                timestamps, source_users, dim=0, dim_size=num_users, reduce="min"
            )
            latest = scatter(
                timestamps, source_users, dim=0, dim_size=num_users, reduce="max"
            )
            span = (latest - earliest).clamp_min(1.0).masked_fill(count == 0, 1.0)
        else:
            span = torch.ones_like(count)
        velocity = count / span
        return self.network(torch.stack((torch.log1p(count), torch.log1p(velocity)), dim=-1))


class HeterogeneousMPNN(nn.Module):
    """Multi-layer heterogeneous GraphSAGE model for user-level fraud scores."""

    def __init__(
        self,
        hidden_channels: int = 64,
        num_layers: int = 2,
        num_classes: int = 2,
        dropout: float = 0.2,
    ) -> None:
        super().__init__()
        if num_layers < 1:
            raise ValueError("num_layers must be positive")
        relations = (
            ("user", "transacts", "merchant"),
            ("merchant", "rev_transacts", "user"),
            ("user", "uses", "device"),
            ("device", "rev_uses", "user"),
            ("user", "shares_ip", "user"),
        )
        self.convs = nn.ModuleList(
            [
                HeteroConv(
                    {
                        relation: SAGEConv((-1, -1), hidden_channels)
                        for relation in relations
                    },
                    aggr="sum",
                )
                for _ in range(num_layers)
            ]
        )
        self.velocity = TransactionVelocity(hidden_channels)
        self.classifier = nn.Sequential(
            nn.Linear(hidden_channels * 2, hidden_channels),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_channels, num_classes),
        )
        self.dropout = dropout

    @staticmethod
    def _with_reverse_edges(
        edge_index_dict: Mapping[tuple[str, str, str], Tensor],
    ) -> dict[tuple[str, str, str], Tensor]:
        edges = dict(edge_index_dict)
        reverse_pairs = {
            ("user", "transacts", "merchant"): ("merchant", "rev_transacts", "user"),
            ("user", "uses", "device"): ("device", "rev_uses", "user"),
        }
        for forward, reverse in reverse_pairs.items():
            if forward in edges:
                edges[reverse] = edges[forward].flip(0)
        return edges

    def forward(self, data: HeteroData) -> Tensor:
        x_dict = {node_type: data[node_type].x for node_type in data.node_types}
        edge_index_dict = self._with_reverse_edges(data.edge_index_dict)
        for convolution in self.convs:
            x_dict = convolution(x_dict, edge_index_dict)
            x_dict = {
                node_type: torch.relu(torch.dropout(features, self.dropout, self.training))
                for node_type, features in x_dict.items()
            }
        velocity = self.velocity(data, data["user"].num_nodes)
        return self.classifier(torch.cat((x_dict["user"], velocity), dim=-1))
