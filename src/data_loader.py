"""Memory-conscious temporal neighbor loading for heterogeneous PyG graphs."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import torch
from torch_geometric.data import HeteroData
from torch_geometric.loader import NeighborLoader

from src.schema import validate_schema


def sort_transactions_temporally(data: HeteroData) -> HeteroData:
    """Return a graph whose transaction edges are sorted by ascending time."""

    edge_type = ("user", "transacts", "merchant")
    if edge_type not in data.edge_types or "edge_attr" not in data[edge_type]:
        return data
    timestamps = data[edge_type].edge_attr[:, 1]
    order = torch.argsort(timestamps, stable=True)
    data[edge_type].edge_index = data[edge_type].edge_index[:, order]
    data[edge_type].edge_attr = data[edge_type].edge_attr[order]
    for key in ("y", "input_id"):
        if key in data[edge_type]:
            data[edge_type][key] = data[edge_type][key][order]
    return data


class TemporalNeighborLoader:
    """Chronological mini-batch wrapper around PyG's heterogeneous sampler.

    ``NeighborLoader`` samples only the configured number of neighbors per
    relation, limiting memory growth. Batches are yielded in chronological
    order according to the earliest transaction timestamp in each batch.
    """

    def __init__(
        self,
        data: HeteroData,
        *,
        input_nodes: tuple[str, torch.Tensor] | None = None,
        num_neighbors: list[int] | dict[Any, list[int]] | None = None,
        batch_size: int = 256,
        shuffle: bool = False,
        **loader_kwargs: Any,
    ) -> None:
        validate_schema(data)
        self.data = sort_transactions_temporally(data)
        if input_nodes is None:
            input_nodes = ("user", self._chronological_user_order(self.data))
        if num_neighbors is None:
            num_neighbors = [15, 10]
        self.loader = NeighborLoader(
            self.data,
            num_neighbors=num_neighbors,
            input_nodes=input_nodes,
            batch_size=batch_size,
            shuffle=shuffle,
            **loader_kwargs,
        )
        self.shuffle = shuffle

    def __iter__(self) -> Iterator[HeteroData]:
        yield from self.loader

    def __len__(self) -> int:
        return len(self.loader)

    @staticmethod
    def _chronological_user_order(data: HeteroData) -> torch.Tensor:
        edge_type = ("user", "transacts", "merchant")
        num_users = data["user"].num_nodes
        if edge_type not in data.edge_types or "edge_attr" not in data[edge_type]:
            return torch.arange(num_users)
        edge_store = data[edge_type]
        timestamps = edge_store.edge_attr[:, 1]
        user_ids = edge_store.edge_index[0]
        earliest = torch.full(
            (num_users,),
            torch.finfo(timestamps.dtype).max,
            dtype=timestamps.dtype,
        )
        if timestamps.numel():
            earliest.scatter_reduce_(
                0,
                user_ids,
                timestamps,
                reduce="amin",
                include_self=True,
            )
        return torch.argsort(earliest, stable=True)
