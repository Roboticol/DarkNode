import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("torch_geometric")

from src.schema import EDGE_TYPES, NODE_TYPES, build_hetero_data, validate_schema


def test_build_heterogeneous_schema() -> None:
    data = build_hetero_data(
        users=[{"segment": "new"}],
        merchants=[{"segment": "retail"}],
        devices=[{"kind": "mobile"}],
        transactions=[{"user_id": 0, "merchant_id": 0, "amount": 10, "timestamp": 1}],
        shared_devices=[{"user_id": 0, "device_id": 0}],
        shared_ips=[{"source_user_id": 0, "target_user_id": 0}],
        user_categorical=("segment",),
        merchant_categorical=("segment",),
        device_categorical=("kind",),
    )
    validate_schema(data)
    assert set(data.node_types) == set(NODE_TYPES)
    assert set(data.edge_types) == set(EDGE_TYPES)
    assert data["user"].x.shape == (1, 1)
