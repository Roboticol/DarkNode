"""Schema and feature utilities for the fraud-detection heterogeneous graph."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Any

import torch
from torch import Tensor, nn
from torch_geometric.data import HeteroData

NodeType = str
EdgeType = tuple[str, str, str]

NODE_TYPES: tuple[NodeType, ...] = ("user", "merchant", "device")
EDGE_TYPES: tuple[EdgeType, ...] = (
    ("user", "transacts", "merchant"),
    ("user", "uses", "device"),
    ("user", "shares_ip", "user"),
)


class CategoricalEncoder:
    """Stable categorical-to-integer mapping suitable for embedding lookup."""

    def __init__(self, unknown_index: int = 0) -> None:
        self.unknown_index = unknown_index
        self._mapping: dict[Any, int] = {}

    @property
    def cardinality(self) -> int:
        return max(len(self._mapping) + self.unknown_index, 1)

    def fit(self, values: Iterable[Any]) -> "CategoricalEncoder":
        for value in values:
            if value not in self._mapping:
                self._mapping[value] = len(self._mapping) + self.unknown_index
        return self

    def transform(self, values: Iterable[Any]) -> Tensor:
        return torch.tensor(
            [self._mapping.get(value, self.unknown_index) for value in values],
            dtype=torch.long,
        )

    def fit_transform(self, values: Iterable[Any]) -> Tensor:
        values = list(values)
        self.fit(values)
        return self.transform(values)


class DenseCategoricalEmbedding(nn.Module):
    """Learnable dense representation for categorical IDs."""

    def __init__(self, cardinality: int, embedding_dim: int) -> None:
        super().__init__()
        self.embedding = nn.Embedding(max(cardinality, 1), embedding_dim)

    def forward(self, category_ids: Tensor) -> Tensor:
        return self.embedding(category_ids.long())


def encode_categorical_features(
    records: Sequence[Mapping[str, Any]],
    columns: Sequence[str],
    *,
    embedding_dim: int = 16,
) -> tuple[Tensor, nn.ModuleDict, dict[str, CategoricalEncoder]]:
    """Encode categorical record fields and return trainable dense features.

    The returned feature tensor is produced by embedding each categorical
    column. The embedding modules remain trainable and can be registered on a
    model, while the encoders preserve the category-to-ID mapping for inference.
    """

    embeddings = nn.ModuleDict()
    encoders: dict[str, CategoricalEncoder] = {}
    encoded_columns: list[Tensor] = []
    for column in columns:
        encoder = CategoricalEncoder().fit(record.get(column) for record in records)
        encoders[column] = encoder
        ids = encoder.transform(record.get(column) for record in records)
        embedding = DenseCategoricalEmbedding(encoder.cardinality, embedding_dim)
        embeddings[column] = embedding
        encoded_columns.append(embedding(ids))
    if not encoded_columns:
        return torch.empty((len(records), 0)), embeddings, encoders
    return torch.cat(encoded_columns, dim=-1), embeddings, encoders


def _records_to_features(
    records: Sequence[Mapping[str, Any]],
    categorical_columns: Sequence[str],
    numerical_columns: Sequence[str],
) -> Tensor:
    """Build a numeric tensor from records, encoding categories as IDs."""

    if not records:
        return torch.empty((0, len(categorical_columns) + len(numerical_columns)), dtype=torch.float)

    columns: list[Tensor] = []
    for column in categorical_columns:
        columns.append(CategoricalEncoder().fit_transform(record.get(column) for record in records))
    for column in numerical_columns:
        columns.append(
            torch.tensor(
                [[float(record.get(column, 0.0))] for record in records],
                dtype=torch.float,
            ).squeeze(-1)
        )
    if not columns:
        return torch.empty((len(records), 0), dtype=torch.float)
    return torch.stack(
        [column.float() if column.ndim == 1 else column for column in columns],
        dim=-1,
    )


def build_hetero_data(
    users: Sequence[Mapping[str, Any]],
    merchants: Sequence[Mapping[str, Any]],
    devices: Sequence[Mapping[str, Any]],
    transactions: Sequence[Mapping[str, Any]],
    shared_devices: Sequence[Mapping[str, Any]],
    shared_ips: Sequence[Mapping[str, Any]],
    *,
    user_categorical: Sequence[str] = (),
    merchant_categorical: Sequence[str] = (),
    device_categorical: Sequence[str] = (),
) -> HeteroData:
    """Ingest entity/relationship records into the canonical PyG schema.

    Relationship records must use integer ``user_id``, ``merchant_id`` and
    ``device_id`` values. Transaction records may additionally contain
    ``amount``, ``timestamp`` and ``is_fraud``.
    """

    data = HeteroData()
    data["user"].x = _records_to_features(users, user_categorical, ())
    data["merchant"].x = _records_to_features(merchants, merchant_categorical, ())
    data["device"].x = _records_to_features(devices, device_categorical, ())

    def edge_index(rows: Sequence[Mapping[str, Any]], left: str, right: str) -> Tensor:
        return torch.tensor(
            [[int(row[left]) for row in rows], [int(row[right]) for row in rows]],
            dtype=torch.long,
        )

    data["user", "transacts", "merchant"].edge_index = edge_index(
        transactions, "user_id", "merchant_id"
    )
    if transactions:
        data["user", "transacts", "merchant"].edge_attr = torch.tensor(
            [
                [
                    float(row.get("amount", 0.0)),
                    float(row.get("timestamp", 0.0)),
                ]
                for row in transactions
            ],
            dtype=torch.float,
        )
        if any("is_fraud" in row for row in transactions):
            data["user", "transacts", "merchant"].y = torch.tensor(
                [int(row.get("is_fraud", 0)) for row in transactions],
                dtype=torch.long,
            )
    data["user", "uses", "device"].edge_index = edge_index(
        shared_devices, "user_id", "device_id"
    )
    data["user", "shares_ip", "user"].edge_index = edge_index(
        shared_ips, "source_user_id", "target_user_id"
    )
    return data


def validate_schema(data: HeteroData) -> None:
    """Raise a useful error if required node or edge stores are malformed."""

    missing_nodes = [node_type for node_type in NODE_TYPES if node_type not in data.node_types]
    missing_edges = [edge_type for edge_type in EDGE_TYPES if edge_type not in data.edge_types]
    if missing_nodes or missing_edges:
        raise ValueError(
            f"Invalid heterogeneous schema; missing nodes={missing_nodes}, "
            f"missing edges={missing_edges}"
        )
    for node_type in NODE_TYPES:
        features = data[node_type].get("x")
        if features is None or features.ndim != 2:
            raise ValueError(f"Node type {node_type!r} must provide a 2D x feature tensor")
    for edge_type in EDGE_TYPES:
        edge_index = data[edge_type].get("edge_index")
        if edge_index is None or edge_index.ndim != 2 or edge_index.shape[0] != 2:
            raise ValueError(f"Edge type {edge_type!r} must provide edge_index with shape [2, E]")
