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
  +------------------------------------+   |  - Account Freeze Simulation (Demo)|
                                           +------------------------------------+
```

---

## Baseline Comparison Note & Metric Analysis

To evaluate model performance, DarkNode includes a rule-based heuristic baseline (`src/ring/baseline.py`) evaluated against the same holdout validation split:

| Metric | Rule-Based Heuristic | DarkNode Heterogeneous GNN | Performance Analysis |
| :--- | :---: | :---: | :--- |
| **Accuracy** | 84.0% | **99.5%** | **+15.5% overall accuracy gain** |
| **ROC-AUC** | 1.000 | **1.000** | Saturated on synthetic signals (see note below) |
| **Average Precision** | 1.000 | **1.000** | Saturated on synthetic signals (see note below) |
| **Precision** | 41.9% | **95.0%** | **+53.1% lift (58% drop in false alarms)** |
| **F1-Score** | 0.591 | **0.974** | **+38.3% lift in balanced detection** |

### Why ROC-AUC and AP Don't Tell the Full Story
On synthetic benchmark datasets with clean demarcations, ranked discrimination metrics like **ROC-AUC** and **Average Precision (AP)** both saturate near `1.000` because extreme burst velocity pushes true fraudsters into the top ranking deciles for both approaches.

The **critical operational gap** is revealed in **Precision (41.9% vs. 95.0%)** and **F1-Score (0.591 vs. 0.974)**:
- **Heuristic Failure**: Simple thresholds (sharing a device with 3+ users or exceeding 5 tx/hr) flag legitimate users in public Wi-Fi hotspots, shared family devices, or during promotional shopping bursts—producing a **58.1% false-positive rate** that would overwhelm fraud operations.
- **GNN Advantage**: The Heterogeneous MPNN synthesizes multi-hop neighborhood context (e.g. *who* else uses the device, *which* merchant cohort is targeted, and *how* the temporal network evolves), effectively filtering out benign shared devices while preserving 95%+ precision.

---

## Quickstart

### 1. Installation

```bash
# Clone repository
git clone https://github.com/adittt18/DarkNode.git
cd DarkNode

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

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

Train the Heterogeneous GraphSAGE MPNN detector and benchmark against the heuristic baseline:

```powershell
python -m src.training.train data\synthetic_fraud_graph.pt --epochs 20 --output data\fraud_model.pt
```

### 5. Launch Backend API

```powershell
uvicorn api.main:app --reload --port 8000
```
- Interactive API Documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`
- Run inference & extract rings: `POST http://localhost:8000/analyze`

### 6. Launch Web Dashboard

Simply open `web/index.html` directly in any web browser, or serve it locally:
```powershell
python -m http.server 3000 --directory web
```
Navigate to `http://localhost:3000` to inspect the live force-directed fraud ring visualization.

---

## Deployment Instructions

### Backend (Render)
1. In [Render Dashboard](https://dashboard.render.com/), create a new **Web Service** linked to your repository.
2. Configuration:
   - **Environment**: Python 3
   - **Root Directory**: `.`
   - **Build Command**: `pip install -r api/requirements.txt`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
3. **Resource Optimization Note**:
   - `api/requirements.txt` is pre-configured with CPU-only PyTorch (`--extra-index-url https://download.pytorch.org/whl/cpu`) to keep the build image under Render's free tier slug and 512 MB memory threshold.
   - For low-memory instances, set environment variable `WEB_CONCURRENCY=1`.
4. The health endpoint `GET /health` is configured for zero-downtime uptime monitoring.

### Frontend (Vercel)
1. Go to [Vercel](https://vercel.com/) and click **Add New Project**.
2. Select your repository.
3. Set **Root Directory** to `web`.
4. Leave build settings empty (Pure HTML/JS static deployment).
5. Deploy! In the live dashboard, enter your Render API endpoint in the top header to stream live graph data.

---

## Dataset Scope & Real-World Adaptation

- **Default Benchmark (Synthetic)**: By default, `src/data_processing/generate_synthetic_graph.py` generates deterministic, scalable fraud networks containing user, device, merchant nodes, burst timestamps, and ground-truth ring memberships.
- **Real-World AML Data Limitations**: Public anti-money-laundering datasets like **Elliptic (Bitcoin)** or **IBM AML** primarily capture transaction flows (address-to-address or entity-to-entity) and **lack physical device or IP telemetry**. 
- **Adapting to Real Environments**: DarkNode is intentionally architected for production banking and fintech environments where rich telemetry (device fingerprints, browser hashes, IP subnets, merchant gateways) is available. For pure transaction datasets without device data, the schema can be projected into bipartite user-merchant or account-account flow subgraphs, though the system demonstrates maximum defensive lift when multi-entity relationships are present.

---

## Interactive UI Features

- **Force-Directed Graph**: Powered by `vis-network` with smooth physics stabilization and node clustering.
- **Evidence Inspector**: Breakdowns of shared device %, shared IP pairs, burst velocity, GNN fraud confidence, and rapid accounts.
- **Node-Level Focus**: Click individual user accounts to zoom and isolate their neighborhood graph.
- **Account Freeze Simulation (Demo)**: A simulated mitigation action designed for hackathon walkthroughs to demonstrate operational compliance workflows.
- **JSON Export**: One-click download of structured ring payloads for compliance auditing.

---

## Acknowledgements & Attribution

This project builds upon the foundational research and graph schema designs from **Apate** by **Oishik Guha**, expanded here into the **DarkNode** platform with community ring extraction, heuristic benchmarking, a lightweight FastAPI backend, and an interactive intelligence interface.

---

## License

This project is licensed under the [MIT License](LICENSE).
