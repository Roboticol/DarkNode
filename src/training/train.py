"""Train and evaluate the heterogeneous fraud-ring detector."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch
from sklearn.metrics import average_precision_score, roc_auc_score
from torch import Tensor
from torch.optim import Adam
from torch_geometric.data import HeteroData

from src.losses import FocalLoss
from src.models.mpnn import HeterogeneousMPNN
from src.schema import validate_schema


@dataclass(frozen=True)
class TrainingConfig:
    """Configuration for deterministic full-graph training."""

    epochs: int = 20
    learning_rate: float = 1e-3
    weight_decay: float = 1e-4
    validation_fraction: float = 0.2
    seed: int = 7


def set_seed(seed: int) -> None:
    """Seed supported random number generators for repeatable experiments."""

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def split_users(
    labels: Tensor,
    validation_fraction: float,
    *,
    seed: int,
) -> tuple[Tensor, Tensor]:
    """Create a reproducible stratified train/validation split."""

    if not 0 < validation_fraction < 1:
        raise ValueError("validation_fraction must be between 0 and 1")
    if labels.ndim != 1 or labels.numel() < 2:
        raise ValueError("labels must be a one-dimensional tensor with at least two values")
    generator = torch.Generator(device=labels.device).manual_seed(seed)
    train_parts: list[Tensor] = []
    validation_parts: list[Tensor] = []
    for class_id in torch.unique(labels, sorted=True):
        class_indices = torch.where(labels == class_id)[0]
        shuffled = class_indices[torch.randperm(class_indices.numel(), generator=generator)]
        validation_count = max(1, int(round(class_indices.numel() * validation_fraction)))
        if validation_count >= class_indices.numel():
            validation_count = class_indices.numel() - 1
        validation_parts.append(shuffled[:validation_count])
        train_parts.append(shuffled[validation_count:])
    train = torch.cat(train_parts)
    validation = torch.cat(validation_parts)
    return train.sort().values, validation.sort().values


def _metrics(logits: Tensor, labels: Tensor) -> dict[str, float]:
    probabilities = logits.softmax(dim=-1)[:, 1].detach().cpu().numpy()
    targets = labels.detach().cpu().numpy()
    result = {"accuracy": float((logits.argmax(dim=-1) == labels).float().mean())}
    if len(np.unique(targets)) > 1:
        result["roc_auc"] = float(roc_auc_score(targets, probabilities))
        result["average_precision"] = float(average_precision_score(targets, probabilities))
    else:
        result["roc_auc"] = float("nan")
        result["average_precision"] = float("nan")
    return result


def train_model(
    data: HeteroData,
    *,
    config: TrainingConfig | None = None,
    model: HeterogeneousMPNN | None = None,
) -> tuple[HeterogeneousMPNN, dict[str, Any]]:
    """Train a model on user labels and return it with validation metrics."""

    validate_schema(data)
    config = config or TrainingConfig()
    if config.epochs < 1:
        raise ValueError("epochs must be positive")
    labels = data["user"].get("y")
    if labels is None:
        raise ValueError("data['user'].y is required for supervised training")
    set_seed(config.seed)
    train_indices, validation_indices = split_users(
        labels, config.validation_fraction, seed=config.seed
    )
    model = model or HeterogeneousMPNN()
    optimizer = Adam(model.parameters(), lr=config.learning_rate, weight_decay=config.weight_decay)
    loss_fn = FocalLoss(alpha=torch.tensor([0.25, 0.75]))
    history: list[dict[str, float]] = []

    for epoch in range(1, config.epochs + 1):
        model.train()
        optimizer.zero_grad()
        logits = model(data)
        loss = loss_fn(logits[train_indices], labels[train_indices])
        loss.backward()
        optimizer.step()
        model.eval()
        with torch.no_grad():
            validation_logits = model(data)[validation_indices]
            metrics = _metrics(validation_logits, labels[validation_indices])
        history.append({"epoch": float(epoch), "loss": float(loss.detach()), **metrics})

    return model, {"history": history, "train_indices": train_indices, "validation_indices": validation_indices}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path, help="Path to a graph produced by the generator")
    parser.add_argument("--epochs", type=int, default=TrainingConfig.epochs)
    parser.add_argument("--seed", type=int, default=TrainingConfig.seed)
    parser.add_argument("--output", type=Path, default=Path("data/fraud_model.pt"))
    args = parser.parse_args()

    payload = torch.load(args.graph, weights_only=False)
    data = payload["data"] if isinstance(payload, dict) else payload
    nx_graph = payload.get("nx", None) if isinstance(payload, dict) else None
    metadata = payload.get("metadata", {}) if isinstance(payload, dict) else {}

    model, report = train_model(data, config=TrainingConfig(epochs=args.epochs, seed=args.seed))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"model_state": model.state_dict(), "report": report}, args.output)
    final = report["history"][-1]

    print("\n" + "=" * 65)
    print("                    MODEL TRAINING RESULTS")
    print("=" * 65)
    print(f"Saved model to:      {args.output}")
    print(f"Validation Loss:     {final['loss']:.4f}")
    print(f"Validation Accuracy: {final['accuracy']:.4f}")
    print(f"Validation ROC-AUC:  {final['roc_auc']:.4f}")
    print(f"Validation AP:       {final['average_precision']:.4f}")

    # Baseline comparison
    from src.ring.baseline import evaluate_baseline
    val_indices = report["validation_indices"]
    base_metrics = evaluate_baseline(data, eval_indices=val_indices)

    print("\n" + "-" * 65)
    print("         BENCHMARK: GNN MPNN vs. RULE-BASED BASELINE")
    print("-" * 65)
    print(f" {'Metric':<20} | {'GNN (DarkNode)':<18} | {'Rule-Based Baseline':<18}")
    print(" " + "-" * 61)
    print(f" {'Accuracy':<20} | {final['accuracy']:<18.4f} | {base_metrics['accuracy']:<18.4f}")
    print(f" {'ROC-AUC':<20} | {final['roc_auc']:<18.4f} | {base_metrics['roc_auc']:<18.4f}")
    print(f" {'Average Precision':<20} | {final['average_precision']:<18.4f} | {base_metrics['average_precision']:<18.4f}")
    print(f" {'F1-Score':<20} | {'N/A (Soft)':<18} | {base_metrics['f1']:<18.4f}")

    # Per-ring extraction & summary
    from src.ring.extract import extract_rings
    model.eval()
    with torch.no_grad():
        all_probs = model(data).softmax(dim=-1)[:, 1]

    rings = extract_rings(data=data, nx_graph=nx_graph, user_scores=all_probs, top_k=10)

    print("\n" + "-" * 65)
    print("            TOP DETECTED FRAUD RINGS SUMMARY")
    print("-" * 65)
    if rings:
        print(f" {'Rank':<5} | {'Ring ID':<8} | {'Score':<8} | {'Members':<8} | {'Shared Dev%':<12} | {'Tx Velocity':<11}")
        print(" " + "-" * 61)
        for r in rings[:5]:
            print(
                f" {r['rank']:<5} | {r['ring_id']:<8} | {r['score']:<8.4f} | "
                f"{r['member_count']:<8} | {r['shared_device_pct']:<12.1f} | {r['transaction_velocity']:<11.1f}"
            )
        print(f"\n[+] Total Candidate Fraud Rings Extracted: {len(rings)}")
    else:
        print("No fraud rings met the risk threshold.")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
