"""Rule-based heuristic baseline fraud detector for comparison with GNN."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.metrics import accuracy_score, average_precision_score, precision_recall_fscore_support, roc_auc_score
import torch
from torch import Tensor
from torch_geometric.data import HeteroData


def compute_baseline_scores(
    data: HeteroData,
    device_share_threshold: int = 3,
    velocity_threshold: float = 5.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute rule-based fraud flags and continuous heuristic risk scores.

    Flags a user as fraud if:
    - They share a device with >= 3 other users (device degree >= 4)
    OR
    - Their transaction velocity exceeds 5 transactions per hour.

    Returns:
        (binary_predictions, continuous_scores)
    """
    num_users = data["user"].num_nodes

    # 1. Device sharing
    device_edge_type = ("user", "uses", "device")
    user_shares_count = np.zeros(num_users, dtype=int)

    if device_edge_type in data.edge_types:
        user_ids = data[device_edge_type].edge_index[0].cpu().numpy()
        device_ids = data[device_edge_type].edge_index[1].cpu().numpy()

        # Build mapping: device -> set of users
        dev_to_users: dict[int, set[int]] = {}
        user_to_devs: dict[int, set[int]] = {}
        for u, d in zip(user_ids, device_ids):
            dev_to_users.setdefault(d, set()).add(u)
            user_to_devs.setdefault(u, set()).add(d)

        # For each user, find maximum other users sharing any of their devices
        for u, devs in user_to_devs.items():
            max_others = 0
            for d in devs:
                others = len(dev_to_users[d]) - 1
                if others > max_others:
                    max_others = others
            user_shares_count[u] = max_others

    # 2. Transaction velocity
    tx_edge_type = ("user", "transacts", "merchant")
    user_velocities = np.zeros(num_users, dtype=float)

    if tx_edge_type in data.edge_types and "edge_attr" in data[tx_edge_type]:
        user_ids = data[tx_edge_type].edge_index[0].cpu().numpy()
        timestamps = data[tx_edge_type].edge_attr[:, 1].cpu().numpy()

        user_tx_times: dict[int, list[float]] = {}
        for u, ts in zip(user_ids, timestamps):
            user_tx_times.setdefault(u, []).append(float(ts))

        for u, t_list in user_tx_times.items():
            if len(t_list) >= 2:
                span_hours = max((max(t_list) - min(t_list)) / 3600.0, 0.05)
                user_velocities[u] = len(t_list) / span_hours
            elif len(t_list) == 1:
                user_velocities[u] = 1.0

    # 3. Rule application
    device_flag = user_shares_count >= device_share_threshold
    velocity_flag = user_velocities > velocity_threshold
    binary_preds = (device_flag | velocity_flag).astype(int)

    # Normalized continuous heuristic score for ROC-AUC & AP
    s_device = np.clip(user_shares_count / max(device_share_threshold, 1), 0.0, 1.0)
    s_vel = np.clip(user_velocities / max(velocity_threshold * 2, 1.0), 0.0, 1.0)
    continuous_scores = np.clip(0.5 * s_device + 0.5 * s_vel, 0.0, 1.0)

    return binary_preds, continuous_scores


def evaluate_baseline(
    data: HeteroData,
    eval_indices: Tensor | np.ndarray | None = None,
    device_share_threshold: int = 3,
    velocity_threshold: float = 5.0,
) -> dict[str, float]:
    """Evaluate the rule-based baseline on validation/test users."""
    binary_preds, continuous_scores = compute_baseline_scores(
        data,
        device_share_threshold=device_share_threshold,
        velocity_threshold=velocity_threshold,
    )

    labels = data["user"].y.cpu().numpy()
    if eval_indices is not None:
        if isinstance(eval_indices, Tensor):
            eval_indices = eval_indices.cpu().numpy()
        labels = labels[eval_indices]
        binary_preds = binary_preds[eval_indices]
        continuous_scores = continuous_scores[eval_indices]

    acc = float(accuracy_score(labels, binary_preds))
    prec, rec, f1, _ = precision_recall_fscore_support(labels, binary_preds, average="binary", zero_division=0)

    try:
        roc = float(roc_auc_score(labels, continuous_scores))
    except ValueError:
        roc = float("nan")

    try:
        ap = float(average_precision_score(labels, continuous_scores))
    except ValueError:
        ap = float("nan")

    return {
        "accuracy": acc,
        "precision": float(prec),
        "recall": float(rec),
        "f1": float(f1),
        "roc_auc": roc,
        "average_precision": ap,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path, nargs="?", default=Path("data/synthetic_fraud_graph.pt"))
    args = parser.parse_args()

    payload = torch.load(args.graph, weights_only=False)
    data = payload["data"] if isinstance(payload, dict) else payload

    metrics = evaluate_baseline(data)
    print("=" * 55)
    print("      RULE-BASED HEURISTIC BASELINE RESULTS")
    print("=" * 55)
    print(f"Accuracy:          {metrics['accuracy']:.4f}")
    print(f"Precision:         {metrics['precision']:.4f}")
    print(f"Recall:            {metrics['recall']:.4f}")
    print(f"F1-Score:          {metrics['f1']:.4f}")
    print(f"ROC-AUC:           {metrics['roc_auc']:.4f}")
    print(f"Average Precision: {metrics['average_precision']:.4f}")
    print("=" * 55)


if __name__ == "__main__":
    main()

