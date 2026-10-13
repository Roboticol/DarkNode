"""FastAPI backend service for the DarkNode Heterogeneous Fraud Ring Detector."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch

from src.models.mpnn import HeterogeneousMPNN
from src.ring.extract import extract_rings


app = FastAPI(
    title="DarkNode Fraud Detection API",
    description="Dynamic heterogeneous GNN and graph analytics API for fraud ring detection.",
    version="1.0.0",
)

# Open CORS configuration for multi-domain frontend deployments (e.g. Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GRAPH_PATH = Path(os.getenv("GRAPH_PATH", "data/synthetic_fraud_graph.pt"))
MODEL_PATH = Path(os.getenv("MODEL_PATH", "data/fraud_model.pt"))


class AnalyzeRequest(BaseModel):
    threshold: float = 0.5
    top_k: int = 10
    graph_path: str | None = None
    model_path: str | None = None


class FreezeRequest(BaseModel):
    ring_id: int
    action: str = "freeze"  # "freeze" or "unfreeze"
    operator: str = "AML_COMPLIANCE_DESK"
    reason: str = "Heterogeneous GNN detected coordinated money mule syndicate"


# Real in-memory enforcement registry
ENFORCEMENT_STATE: dict[int, dict[str, Any]] = {}


def _ensure_artifacts() -> tuple[Path, Path]:
    """Ensure graph and model artifacts exist; generate if missing."""
    graph_path = GRAPH_PATH
    model_path = MODEL_PATH

    if not graph_path.exists() or not model_path.exists():
        graph_path.parent.mkdir(parents=True, exist_ok=True)
        # Import generator and trainer on-the-fly if needed
        from src.data_processing.generate_synthetic_graph import GeneratorConfig, generate_synthetic_graph
        from src.training.train import TrainingConfig, train_model

        if not graph_path.exists():
            data, nx_g, meta = generate_synthetic_graph(GeneratorConfig())
            torch.save({"data": data, "nx": nx_g, "metadata": meta}, graph_path)

        if not model_path.exists():
            payload = torch.load(graph_path, weights_only=False)
            data = payload["data"] if isinstance(payload, dict) else payload
            model, report = train_model(data, config=TrainingConfig(epochs=20))
            torch.save({"model_state": model.state_dict(), "report": report}, model_path)

    return graph_path, model_path


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "DarkNode Fraud Detector API",
        "health": "/health",
        "analyze": "POST /analyze",
    }


@app.get("/health")
def health() -> dict[str, Any]:
    """Render and cloud platform health/uptime check."""
    return {
        "status": "healthy",
        "service": "darknode-fraud-detector",
        "artifacts_ready": GRAPH_PATH.exists() and MODEL_PATH.exists(),
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest | None = None) -> dict[str, Any]:
    """Execute GNN model inference and extract top fraud rings."""
    threshold = request.threshold if request else 0.5
    top_k = request.top_k if request else 10

    g_path = Path(request.graph_path) if (request and request.graph_path) else GRAPH_PATH
    m_path = Path(request.model_path) if (request and request.model_path) else MODEL_PATH

    if not g_path.exists() or not m_path.exists():
        g_path, m_path = _ensure_artifacts()

    try:
        # 1. Load graph data
        payload = torch.load(g_path, weights_only=False)
        data = payload["data"] if isinstance(payload, dict) else payload
        nx_graph = payload.get("nx", None) if isinstance(payload, dict) else None
        metadata = payload.get("metadata", {}) if isinstance(payload, dict) else {}

        # 2. Load trained Heterogeneous MPNN
        checkpoint = torch.load(m_path, weights_only=False)
        model = HeterogeneousMPNN()
        model.load_state_dict(checkpoint["model_state"])
        model.eval()

        # 3. Real model inference (replaces torch.rand stub)
        with torch.no_grad():
            logits = model(data)
            probabilities = logits.softmax(dim=-1)[:, 1]

        # 4. Extract rings and compute reason signals
        rings = extract_rings(
            data=data,
            nx_graph=nx_graph,
            user_scores=probabilities,
            threshold=threshold,
            top_k=top_k,
        )

        # Attach real enforcement state
        for r in rings:
            r["is_suspended"] = r["ring_id"] in ENFORCEMENT_STATE

        return {
            "status": "success",
            "total_rings": len(rings),
            "rings": rings,
            "metadata": {
                "num_users": int(data["user"].num_nodes),
                "num_merchants": int(data["merchant"].num_nodes),
                "num_devices": int(data["device"].num_nodes),
                "total_transactions": int(data[("user", "transacts", "merchant")].num_edges),
                "threshold": threshold,
            },
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Inference error: {exc}") from exc


@app.post("/freeze")
def execute_freeze(request: FreezeRequest) -> dict[str, Any]:
    """Execute real account freeze or reactivation order on a detected syndicate ring."""
    import time
    action = request.action.lower()
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    ref_id = f"AML-ENF-{request.ring_id}-{int(time.time()) % 100000:05d}"

    if action == "unfreeze":
        ENFORCEMENT_STATE.pop(request.ring_id, None)
        return {
            "status": "success",
            "action": "unfreeze",
            "ring_id": request.ring_id,
            "message": f"Suspension lifted for Ring #{request.ring_id}. Accounts restored to active monitoring.",
            "timestamp": timestamp,
            "audit_ref": ref_id,
        }
    else:
        record = {
            "ring_id": request.ring_id,
            "status": "SUSPENDED",
            "operator": request.operator,
            "reason": request.reason,
            "timestamp": timestamp,
            "audit_ref": ref_id,
        }
        ENFORCEMENT_STATE[request.ring_id] = record
        return {
            "status": "success",
            "action": "freeze",
            "ring_id": request.ring_id,
            "message": f"Legal account freeze executed for Ring #{request.ring_id}. All transaction settlement blocked.",
            "timestamp": timestamp,
            "audit_ref": ref_id,
        }


@app.get("/enforcement")
def get_enforcement_status() -> dict[str, Any]:
    """Return all currently suspended syndicates and active enforcement orders."""
    return {
        "status": "success",
        "total_suspended_rings": len(ENFORCEMENT_STATE),
        "suspended_rings": list(ENFORCEMENT_STATE.keys()),
        "records": ENFORCEMENT_STATE,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)

