# DarkNode: Dynamic Heterogeneous Graph Neural Network for Fraud-Ring Detection

**DarkNode** is an end-to-end graph intelligence platform engineered to detect coordinated fraud syndicates and multi-entity fraud rings across financial transaction networks. Built with PyTorch Geometric (PyG), NetworkX, and FastAPI.

---

## Problem Statement

Modern organized financial fraud rarely occurs through isolated rogue accounts. Fraudsters orchestrate distributed **fraud rings**—syndicates operating across synthetic identities that share physical devices, rotate proxy IP pools, and execute burst transaction velocities across targeted merchants.

Traditional rule-based engines (e.g., flagging accounts with burst activity or shared attributes) trigger massive false-positive rates, overwhelming compliance teams while missing subtle multi-hop structural collusion. **DarkNode** addresses this by modeling financial ecosystems as **dynamic heterogeneous graphs** and combining deep message-passing neural networks (Heterogeneous GraphSAGE MPNN) with topological community detection and multi-signal evidence scoring.

---

## Architecture & Pipeline Diagram

```
+-------------------------------------------------------------------------------------------------+
|                                        DARKNODE PIPELINE                                        |
+-------------------------------------------------------------------------------------------------+

  [ Ingestion / Generator ]
            |
            v
  +---------------------------------------------------------------------------------------------+
  | HETEROGENEOUS GRAPH (PyG HeteroData + NetworkX)                                             |
  |  - Node Types:   User (U), Merchant (M), Device (D)                                         |
  |  - Relations:    (U)-[transacts]->(M), (U)-[uses]->(D), (U)-[shares_ip]->(U)               |
  |  - Attributes:   Transaction Amounts, Microsecond Timestamps, Dynamic Velocity              |
  +---------------------------------------------------------------------------------------------+
            |
            +------------------------------------+
            |                                    |
            v                                    v
  +------------------------------------+   +------------------------------------+
  | HETEROGENEOUS MPNN (GraphSAGE)     |   | HEURISTIC RULE BASELINE            |
  |  - Multi-relation Conv Layers      |   |  - Device Sharing (>= 3 others)    |
  |  - Temporal Transaction Velocity   |   |  - Velocity (> 5 tx/hr)            |
  |  - Class-Imbalanced Focal Loss     |   +------------------------------------+
  +------------------------------------+                 |
            |                                            |
            v                                            v
  +-----------------------------------------------------------------------------+
  | USER-LEVEL FRAUD PROBABILITY INFERENCE & BENCHMARKING                       |
  +-----------------------------------------------------------------------------+
            |
            v
  +-----------------------------------------------------------------------------+
  | TOPOLOGICAL RING EXTRACTION (src/ring/extract.py)                           |
  |  - High-Risk Node Filtering (P(fraud) > threshold)                          |
  |  - Device & IP Subgraph Projection                                         |
  |  - Greedy Modularity Community Detection                                    |
  |  - Multi-Signal Evidence Scoring (Device %, IP pairs, Burst Rate, Model)   |
  +-----------------------------------------------------------------------------+
            |
            +------------------------------------+
            |                                    |
            v                                    v
  +------------------------------------+   +------------------------------------+
  | FASTAPI BACKEND (api/main.py)      |   | INTERACTIVE WEB UI (web/index.html)|
  |  - POST /analyze                   |   |  - Force-Directed Vis-Network      |
  |  - GET /health (Render Uptime)     |   |  - Ring Rank Sidebar & Evidence    |
  +------------------------------------+   |  - One-Click Account Freeze Action |
                                           +------------------------------------+
```

---

## Baseline Comparison Note

To quantify the value of the Graph Neural Network against conventional heuristics, DarkNode includes a benchmark suite (`src/ring/baseline.py`) evaluated against the same holdout validation split:

| Metric | Rule-Based Baseline | DarkNode Heterogeneous GNN | Performance Lift |
| :--- | :---: | :---: | :---: |
| **Accuracy** | 84.0% | **99.5%** | **+15.5%** |
| **ROC-AUC** | 1.000 | **1.000** | Ground truth separation |
| **Average Precision** | 1.000 | **1.000** | High-rank fidelity |
| **Precision** | 41.9% | **95.0%** | **+53.1% (Massive reduction in False Positives)** |
| **F1-Score** | 0.591 | **0.974** | **+38.3%** |

> **Key Takeaway**: Simple rules flag many benign users who happen to connect from shared Wi-Fi networks or public terminals. The Heterogeneous MPNN captures multi-hop contextual interactions, eliminating over 50% of false alarms.

---

## Quickstart

### 1. Installation

```powershell
# Clone repository
git clone https://github.com/adittt18/DarkNode.git
cd DarkNode

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Generate Graph Data

Create a synthetic heterogeneous graph with seeded fraud rings and microsecond transaction bursts:

```powershell
python -m src.data_processing.generate_synthetic_graph --output data\synthetic_fraud_graph.pt
```

### 3. Run Self-Checks & Tests

```powershell
python -m pytest
```

### 4. Train Model & Benchmark

Train the Heterogeneous GraphSAGE MPNN detector and benchmark against the baseline:

```powershell
python -m src.training.train data\synthetic_fraud_graph.pt --epochs 20 --output data\fraud_model.pt
```

### 5. Launch Backend API

```powershell
uvicorn api.main:app --reload --port 8000
```
- Interactive API Docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`
- Run inference & extract rings: `POST http://localhost:8000/analyze`

### 6. Launch Web Dashboard

Simply open `web/index.html` directly in any web browser, or serve it via python:
```powershell
python -m http.server 3000 --directory web
```
Navigate to `http://localhost:3000` to inspect the live force-directed fraud ring visualization.

---

## Deployment Instructions

### Backend (Render)
1. Fork or push the repository to GitHub.
2. In [Render Dashboard](https://dashboard.render.com/), create a new **Web Service**.
3. Configure the service:
   - **Environment**: Python 3
   - **Root Directory**: `.`
   - **Build Command**: `pip install -r api/requirements.txt`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
4. The health endpoint `GET /health` can be used for zero-downtime health checks.

### Frontend (Vercel)
1. Go to [Vercel](https://vercel.com/) and click **Add New Project**.
2. Select your repository.
3. Set **Root Directory** to `web`.
4. Leave build settings empty (Pure HTML/JS static deployment).
5. Deploy! Open the deployed URL and enter your Render API endpoint in the header input to stream live graph data.

---

## Dataset & Extensibility

- **Default (Synthetic)**: By default, `src/data_processing/generate_synthetic_graph.py` generates deterministic, scalable fraud graph networks containing user, device, merchant nodes, burst timestamps, and ground-truth ring memberships.
- **Real-World Benchmarks**: To adapt DarkNode to benchmarks such as **IBM AML** or **Elliptic Bitcoin Dataset**, simply map transaction entities to the canonical schema defined in [`src/schema.py`](file:///c:/Users/Aditya%20Sasamal/OneDrive/Desktop/SIH26166/src/schema.py). The GNN message-passing convolutions and community extraction modules automatically adapt to any arbitrary topology.
