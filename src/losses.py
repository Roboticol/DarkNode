"""Loss functions for imbalanced fraud detection."""

from __future__ import annotations

import torch
from torch import Tensor, nn
from torch.nn import functional as F


class FocalLoss(nn.Module):
    """Multi-class focal loss with optional per-class weighting.

    The modulating factor ``(1 - p_t) ** gamma`` down-weights easy examples,
    while ``alpha`` can increase the contribution of the rare fraud class.
    """

    def __init__(
        self,
        alpha: float | Tensor = 0.25,
        gamma: float = 2.0,
        reduction: str = "mean",
    ) -> None:
        super().__init__()
        if gamma < 0:
            raise ValueError("gamma must be non-negative")
        if reduction not in {"none", "mean", "sum"}:
            raise ValueError("reduction must be one of: none, mean, sum")
        alpha_tensor = torch.as_tensor(alpha, dtype=torch.float)
        self.register_buffer("alpha", alpha_tensor)
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, logits: Tensor, targets: Tensor) -> Tensor:
        if logits.ndim < 2:
            raise ValueError("logits must have shape [batch_size, num_classes]")
        if targets.shape != logits.shape[:-1]:
            raise ValueError("targets must match logits dimensions excluding the class dimension")
        targets = targets.long()
        if targets.numel() and (targets.min() < 0 or targets.max() >= logits.size(-1)):
            raise ValueError("targets contain a class index outside the logits class range")
        log_prob = F.log_softmax(logits, dim=-1)
        log_pt = log_prob.gather(-1, targets.unsqueeze(-1)).squeeze(-1)
        pt = log_pt.exp()
        if self.alpha.numel() == 1:
            alpha_t = self.alpha.to(logits).expand_as(pt)
        else:
            if self.alpha.numel() != logits.size(-1):
                raise ValueError("alpha must be scalar or have one value per class")
            alpha_t = self.alpha.to(logits).gather(0, targets)
        loss = -alpha_t * (1.0 - pt).pow(self.gamma) * log_pt
        if self.reduction == "sum":
            return loss.sum()
        if self.reduction == "mean":
            return loss.mean()
        return loss
