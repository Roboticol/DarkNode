import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("torch_geometric")

from src.data_processing.generate_synthetic_graph import GeneratorConfig, generate_synthetic_graph
from src.training.train import TrainingConfig, split_users, train_model


def test_split_users_is_reproducible_and_disjoint() -> None:
    labels = torch.tensor([0, 0, 0, 1, 1, 1])
    first = split_users(labels, 0.34, seed=11)
    second = split_users(labels, 0.34, seed=11)
    assert torch.equal(first[0], second[0])
    assert torch.equal(first[1], second[1])
    assert not torch.isin(first[0], first[1]).any()


def test_train_model_returns_history() -> None:
    data, _, _ = generate_synthetic_graph(
        GeneratorConfig(
            num_users=24,
            num_merchants=6,
            num_devices=12,
            transactions_per_user=2,
            ring_size=4,
            ring_transactions_per_user=4,
        )
    )
    _, report = train_model(data, config=TrainingConfig(epochs=1, seed=3))
    assert len(report["history"]) == 1
    assert "average_precision" in report["history"][0]
