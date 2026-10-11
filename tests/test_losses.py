import torch

from src.losses import FocalLoss


def test_focal_loss_returns_finite_scalar() -> None:
    logits = torch.tensor([[2.0, -1.0], [-1.0, 2.0]])
    targets = torch.tensor([0, 1])
    loss = FocalLoss(alpha=torch.tensor([0.25, 0.75]))(logits, targets)
    assert loss.ndim == 0
    assert torch.isfinite(loss)
