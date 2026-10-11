"""DarkNode: End-to-End Execution and Evaluation Demo.

Demonstrates:
1. Loading the heterogeneous fraud graph.
2. Loading the trained HeterogeneousMPNN model checkpoint.
3. Performing inference across all users.
4. Evaluating performance (Accuracy, Precision, Recall, F1, ROC-AUC).
5. Inspecting detected fraud rings and high-risk suspect users.
"""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
import torch
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, average_precision_score

from src.models.mpnn import HeterogeneousMPNN


def run_demo() -> None:
    graph_path = Path("data/synthetic_fraud_graph.pt")
    model_path = Path("data/fraud_model.pt")

    if not graph_path.exists():
        print(f"Error: {graph_path} not found. Please run the graph generator first.")
        sys.exit(1)

    if not model_path.exists():
        print(f"Error: {model_path} not found. Please train the model first.")
        sys.exit(1)

    print("=" * 65)
    print("       DARKNODE: DYNAMIC HETEROGENEOUS GRAPH FRAUD DETECTOR")
    print("=" * 65)

    # 1. Load Data
    payload = torch.load(graph_path, weights_only=False)
    data = payload["data"] if isinstance(payload, dict) else payload
    metadata = payload.get("metadata", {})

    print("\n[+] Graph Topology & Metadata:")
    print(f"    - User nodes:         {data['user'].num_nodes:,}")
    print(f"    - Merchant nodes:     {data['merchant'].num_nodes:,}")
    print(f"    - Device nodes:       {data['device'].num_nodes:,}")
    print(f"    - Transactions:       {data[('user', 'transacts', 'merchant')].num_edges:,}")
    print(f"    - Shared Device edges:{data[('user', 'uses', 'device')].num_edges:,}")
    print(f"    - Shared IP edges:    {data[('user', 'shares_ip', 'user')].num_edges:,}")
    print(f"    - Ground Truth Rings: {metadata.get('num_fraud_rings', 'N/A')}")
    print(f"    - Fraud Transactions: {metadata.get('fraud_transaction_count', 'N/A'):,}")

    # 2. Load Model
    checkpoint = torch.load(model_path, weights_only=False)
    model = HeterogeneousMPNN()
    model.load_state_dict(checkpoint["model_state"])
    model.eval()

    # 3. Model Inference
    with torch.no_grad():
        logits = model(data)
        probabilities = logits.softmax(dim=-1)[:, 1].cpu().numpy()
        predictions = logits.argmax(dim=-1).cpu().numpy()

    labels = data["user"].y.cpu().numpy()
    val_indices = checkpoint["report"]["validation_indices"].cpu().numpy()
    train_indices = checkpoint["report"]["train_indices"].cpu().numpy()

    # 4. Evaluation on Validation Split
    val_true = labels[val_indices]
    val_pred = predictions[val_indices]
    val_probs = probabilities[val_indices]

    val_roc = roc_auc_score(val_true, val_probs)
    val_ap = average_precision_score(val_true, val_probs)

    print("\n[+] Validation Set Results (20% holdout split):")
    print(f"    - Users Evaluated:    {len(val_indices)}")
    print(f"    - ROC-AUC:            {val_roc:.4f}")
    print(f"    - Average Precision:  {val_ap:.4f}")
    print("\n" + classification_report(val_true, val_pred, target_names=["Legitimate", "Fraud Ring Member"]))

    cm = confusion_matrix(val_true, val_pred)
    print("Confusion Matrix:")
    print(f"    True Negative: {cm[0, 0]:3d} | False Positive: {cm[0, 1]:3d}")
    print(f"    False Negative: {cm[1, 0]:3d} | True Positive:  {cm[1, 1]:3d}")

    # 5. Top Suspects
    top_suspects = np.argsort(probabilities)[::-1][:10]
    ring_members = metadata.get("ring_members", [])
    user_ips = metadata.get("user_ips", {})
    # Invert ring_members mapping: ring_id -> list of user_ids
    user_to_ring = {}
    for ring_idx, members in ring_members.items():
        for member in members:
            user_to_ring[member] = ring_idx

    print("\n[+] Top 10 High-Risk Fraud Suspects Detected by GNN:")
    print(" Rank | User ID | Fraud Prob | Predicted  | Ground Truth | Ring ID | Shared IP")
    print(" " + "-" * 72)
    for rank, uid in enumerate(top_suspects, 1):
        prob = probabilities[uid]
        pred_label = "Fraud" if predictions[uid] == 1 else "Legit"
        actual_label = "Fraud" if labels[uid] == 1 else "Legit"
        r_id = user_to_ring.get(uid, "None")
        ip = user_ips.get(uid, "N/A")
        print(f"  {rank:2d}  | {uid:7d} |   {prob*100:5.1f}%   |   {pred_label:5s}    |    {actual_label:5s}     | Ring {str(r_id):3s} | {ip}")

    # 6. Fraud Ring Detection Rate
    ring_detection = {}
    for ring_idx, members in ring_members.items():
        ring_detection[ring_idx] = {
            "total": len(members),
            "detected": sum(1 for m in members if predictions[m] == 1),
        }

    fully_caught = sum(1 for r in ring_detection.values() if r["detected"] == r["total"])
    print(f"\n[+] Fraud Ring Synthesis Detection:")
    print(f"    - Total Injected Rings: {len(ring_detection)}")
    print(f"    - 100% Caught Rings:    {fully_caught} / {len(ring_detection)} ({fully_caught/len(ring_detection)*100:.1f}%)")
    print(f"    - Fraudster Recall:     {sum(r['detected'] for r in ring_detection.values())} / {sum(r['total'] for r in ring_detection.values())} ({sum(r['detected'] for r in ring_detection.values())/sum(r['total'] for r in ring_detection.values())*100:.1f}%)")

    print("\n" + "=" * 65)
    print("Pipeline executed successfully!")
    print("=" * 65)


if __name__ == "__main__":
    run_demo()
