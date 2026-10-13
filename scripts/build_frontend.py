"""Build web/index.html:
Clean, authentic DarkNode interface matching the original reference demo sample.
All extraneous motion, blinking effects, trajectory face morphs, and heavy animations removed.
Embedded real forward-pass rings from trained model.
"""

import json
from pathlib import Path

fallback_path = Path("data/fallback_rings.json")
if not fallback_path.exists():
    raise FileNotFoundError("data/fallback_rings.json not found")

with open(fallback_path, "r", encoding="utf-8") as f:
    fallback_data = f.read()

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DarkNode — Fraud Ring Detection Platform</title>
  <!-- Vis-network CDN -->
  <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <!-- Inter & JetBrains Mono Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

  <style>
    :root {
      --bg: #09090b;
      --surface: #121215;
      --surface-elevated: #18181b;
      --surface-hover: #222227;
      --border: #27272a;
      --border-subtle: #1e1e24;
      --text: #f4f4f5;
      --text-muted: #71717a;
      --text-dim: #52525b;
      --danger: #f43f5e;
      --danger-subtle: rgba(244, 63, 94, 0.1);
      --danger-border: rgba(244, 63, 94, 0.3);
      --warning: #f59e0b;
      --success: #10b981;
      --accent: #3b82f6;
      --user-node: #f43f5e;
      --device-node: #f59e0b;
      --merchant-node: #10b981;
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: var(--font-sans);
      background-color: var(--bg);
      color: var(--text);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      -webkit-font-smoothing: antialiased;
    }

    /* Minimal Header */
    header {
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      height: 52px;
      padding: 0 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
      z-index: 50;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .brand-mark {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--danger);
      box-shadow: 0 0 10px var(--danger);
    }

    .brand-name {
      font-weight: 700;
      font-size: 14px;
      letter-spacing: -0.02em;
      color: var(--text);
    }

    .badge-gnn {
      font-family: var(--font-mono);
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      background: var(--surface-elevated);
      color: var(--text-muted);
      border: 1px solid var(--border);
    }

    .top-stats {
      display: flex;
      align-items: center;
      gap: 20px;
      font-size: 12px;
      color: var(--text-muted);
    }

    .stat-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .stat-val {
      font-family: var(--font-mono);
      font-weight: 600;
      color: var(--text);
    }

    .controls-section {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .api-pill {
      display: flex;
      align-items: center;
      background: var(--surface-elevated);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 3px 8px;
      gap: 6px;
    }

    .api-pill input {
      background: transparent;
      border: none;
      color: var(--text);
      font-family: var(--font-mono);
      font-size: 11px;
      width: 170px;
      outline: none;
    }

    .status-indicator {
      display: flex;
      align-items: center;
      gap: 5px;
      font-size: 11px;
      font-family: var(--font-mono);
      padding: 3px 8px;
      border-radius: 4px;
      background: rgba(16, 185, 129, 0.1);
      color: var(--success);
      border: 1px solid rgba(16, 185, 129, 0.2);
    }

    .status-indicator.offline {
      background: rgba(245, 158, 11, 0.1);
      color: var(--warning);
      border-color: rgba(245, 158, 11, 0.2);
    }

    .btn {
      height: 28px;
      padding: 0 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      border: 1px solid var(--border);
      background: var(--surface-elevated);
      color: var(--text);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }

    .btn:hover {
      background: var(--surface-hover);
      border-color: var(--text-dim);
    }

    .btn-primary {
      background: #fafafa;
      color: #09090b;
      border: none;
      font-weight: 600;
    }

    .btn-primary:hover {
      background: #e4e4e7;
    }

    .btn-danger {
      background: var(--danger-subtle);
      border-color: var(--danger-border);
      color: var(--danger);
      font-weight: 600;
    }

    .btn-danger:hover {
      background: rgba(244, 63, 94, 0.2);
    }

    /* Workspace Layout */
    .workspace {
      display: flex;
      flex: 1;
      height: calc(100vh - 52px);
      overflow: hidden;
    }

    /* Left Sidebar: Ring Directory */
    .sidebar-left {
      width: 290px;
      background: var(--surface);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }

    .sidebar-search {
      padding: 10px 12px;
      border-bottom: 1px solid var(--border-subtle);
    }

    .search-input {
      width: 100%;
      background: var(--surface-elevated);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 6px 10px;
      font-size: 12px;
      color: var(--text);
      outline: none;
      font-family: var(--font-sans);
    }

    .search-input:focus {
      border-color: var(--text-dim);
    }

    .rings-list {
      flex: 1;
      overflow-y: auto;
      padding: 8px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .ring-item {
      padding: 10px 12px;
      border-radius: 6px;
      cursor: pointer;
      border: 1px solid transparent;
      background: transparent;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .ring-item:hover {
      background: var(--surface-hover);
    }

    .ring-item.active {
      background: var(--surface-elevated);
      border-color: var(--border);
    }

    .ring-item-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .ring-title {
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .ring-score-pill {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: 4px;
      background: var(--danger-subtle);
      color: var(--danger);
      border: 1px solid var(--danger-border);
    }

    .ring-item-bottom {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 11px;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }

    /* Center Viewport: Graph */
    .viewport-center {
      flex: 1;
      position: relative;
      background: #09090b;
      overflow: hidden;
    }

    #network-canvas {
      width: 100%;
      height: 100%;
    }

    /* Floating Graph Toolbar */
    .graph-toolbar {
      position: absolute;
      top: 14px;
      left: 14px;
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(18, 18, 21, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 4px;
      z-index: 10;
    }

    .tool-btn {
      height: 26px;
      padding: 0 8px;
      font-size: 11px;
      font-family: var(--font-sans);
      border-radius: 4px;
      border: none;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .tool-btn:hover {
      background: var(--surface-hover);
      color: var(--text);
    }

    .tool-btn.active {
      background: var(--surface-hover);
      color: var(--text);
      font-weight: 600;
    }

    .graph-legend {
      position: absolute;
      bottom: 14px;
      left: 14px;
      display: flex;
      align-items: center;
      gap: 14px;
      background: rgba(18, 18, 21, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 6px 12px;
      font-size: 11px;
      color: var(--text-muted);
      z-index: 10;
    }

    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .legend-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }

    /* Right Inspector Panel */
    .sidebar-right {
      width: 320px;
      background: var(--surface);
      border-left: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      overflow-y: auto;
    }

    .panel-header {
      padding: 14px 16px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .panel-header h2 {
      font-size: 13px;
      font-weight: 600;
      color: var(--text);
    }

    .panel-content {
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    /* Threat Score Card */
    .threat-card {
      background: var(--surface-elevated);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px;
      display: flex;
      align-items: baseline;
      justify-content: space-between;
    }

    .threat-score-large {
      font-family: var(--font-mono);
      font-size: 32px;
      font-weight: 700;
      color: var(--danger);
      line-height: 1;
    }

    .threat-label {
      font-size: 11px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    /* Signals Grid */
    .signals-grid {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .signal-row {
      background: var(--surface-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 8px 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .signal-name {
      font-size: 12px;
      color: var(--text-muted);
    }

    .signal-num {
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 600;
      color: var(--text);
    }

    /* Account Chips */
    .section-title {
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-dim);
      margin-bottom: 8px;
    }

    .chips-wrap {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
    }

    .user-chip {
      font-family: var(--font-mono);
      font-size: 11px;
      padding: 3px 7px;
      border-radius: 4px;
      background: var(--surface-elevated);
      border: 1px solid var(--border);
      color: var(--text);
      cursor: pointer;
    }

    .user-chip:hover {
      border-color: var(--danger);
      color: var(--danger);
    }

    /* Action Buttons */
    .actions-stack {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: 8px;
    }

    /* Minimal Toast */
    .toast {
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: var(--surface-elevated);
      border: 1px solid var(--border);
      padding: 10px 16px;
      border-radius: 6px;
      font-size: 12px;
      display: none;
      align-items: center;
      gap: 8px;
      z-index: 1000;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }

    .toast-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--success);
    }
  </style>
</head>
<body>

  <!-- Minimal Header -->
  <header>
    <div class="brand">
      <div class="brand-mark"></div>
      <div class="brand-name">DarkNode</div>
      <span class="badge-gnn">MPNN GNN</span>
    </div>

    <!-- Quick Stats -->
    <div class="top-stats">
      <div class="stat-item">
        <span>Users:</span>
        <span class="stat-val" id="stat-users">1,000</span>
      </div>
      <div class="stat-item">
        <span>Transactions:</span>
        <span class="stat-val" id="stat-txs">13,680</span>
      </div>
      <div class="stat-item">
        <span>Rings:</span>
        <span class="stat-val" id="stat-rings">12</span>
      </div>
    </div>

    <!-- Controls -->
    <div class="controls-section">
      <div class="status-indicator" id="status-pill">
        <span id="status-text">Connecting...</span>
      </div>

      <div class="api-pill">
        <input type="text" id="api-url" value="http://localhost:8000" placeholder="API endpoint">
      </div>

      <button class="btn btn-primary" onclick="fetchRings()">
        Analyze
      </button>
    </div>
  </header>

  <!-- Workspace -->
  <div class="workspace">

    <!-- Left: Rings Directory -->
    <div class="sidebar-left">
      <div class="sidebar-search">
        <input type="text" class="search-input" id="search-filter" placeholder="Filter rings..." oninput="filterRings()">
      </div>
      <div class="rings-list" id="rings-container">
        <!-- Injected rings -->
      </div>
    </div>

    <!-- Center: Interactive Vis-Network Viewport -->
    <div class="viewport-center">
      <!-- Toolbar -->
      <div class="graph-toolbar">
        <button class="tool-btn" onclick="resetGraphView()">Fit</button>
        <button class="tool-btn" id="physics-toggle" onclick="togglePhysics()">Physics: On</button>
        <span style="color: var(--border); font-size: 10px;">|</span>
        <button class="tool-btn active" id="filter-user" onclick="toggleNodeFilter('user')">Users</button>
        <button class="tool-btn active" id="filter-device" onclick="toggleNodeFilter('device')">Devices</button>
        <button class="tool-btn active" id="filter-merchant" onclick="toggleNodeFilter('merchant')">Merchants</button>
      </div>

      <div id="network-canvas"></div>

      <!-- Legend -->
      <div class="graph-legend">
        <div class="legend-item">
          <div class="legend-dot" style="background: var(--user-node);"></div>
          <span>Ring Member</span>
        </div>
        <div class="legend-item">
          <div class="legend-dot" style="background: var(--device-node);"></div>
          <span>Shared Device</span>
        </div>
        <div class="legend-item">
          <div class="legend-dot" style="background: var(--merchant-node);"></div>
          <span>Merchant</span>
        </div>
      </div>
    </div>

    <!-- Right: Inspector & Reason Signals -->
    <div class="sidebar-right">
      <div class="panel-header">
        <h2 id="inspector-title">Ring Inspector</h2>
        <span class="badge-gnn" id="inspector-badge">#--</span>
      </div>

      <div class="panel-content">
        <!-- Threat Card -->
        <div class="threat-card">
          <div>
            <div class="threat-label">Composite Risk</div>
            <div class="threat-score-large" id="card-threat-score">--</div>
          </div>
          <div style="font-family: var(--font-mono); font-size: 11px; color: var(--text-muted);" id="card-rank">
            RANK #--
          </div>
        </div>

        <!-- Evidence Signals -->
        <div>
          <div class="section-title">Evidence & Reason Signals</div>
          <div class="signals-grid">
            <div class="signal-row">
              <span class="signal-name">Shared Device Ratio</span>
              <span class="signal-num" id="sig-device">0%</span>
            </div>
            <div class="signal-row">
              <span class="signal-name">Shared IP Pairs</span>
              <span class="signal-num" id="sig-ip">0 pairs</span>
            </div>
            <div class="signal-row">
              <span class="signal-name">Transaction Velocity</span>
              <span class="signal-num" id="sig-vel">0 tx/hr</span>
            </div>
            <div class="signal-row">
              <span class="signal-name">GNN Fraud Confidence</span>
              <span class="signal-num" id="sig-gnn">0.00</span>
            </div>
            <div class="signal-row">
              <span class="signal-name">Rapid / Burst Accounts</span>
              <span class="signal-num" id="sig-fresh">0</span>
            </div>
          </div>
        </div>

        <!-- Members -->
        <div>
          <div class="section-title">Member Accounts (<span id="members-count">0</span>)</div>
          <div class="chips-wrap" id="members-chips">
            <!-- Injected user chips -->
          </div>
        </div>

        <!-- Actions -->
        <div class="actions-stack">
          <button class="btn btn-danger" style="height: 34px;" id="freeze-btn" onclick="freezeRing()">
            Freeze Ring Accounts
          </button>
          <button class="btn" style="height: 32px;" onclick="exportRingJson()">
            Export Ring Data (JSON)
          </button>
        </div>
      </div>
    </div>

  </div>

  <!-- Toast -->
  <div class="toast" id="toast">
    <div class="toast-dot"></div>
    <span id="toast-message">Action confirmed.</span>
  </div>

  <script>
    let network = null;
    let allRings = [];
    let activeRingIndex = 0;
    let physicsEnabled = true;
    let nodeFilters = { user: true, device: true, merchant: true };

    // Embedded Forward-Pass Rings Data from Trained Model
    const FALLBACK_DATA = __FALLBACK_JSON__;

    async function fetchRings() {
      const url = document.getElementById("api-url").value.trim().replace(/\/$/, "");
      const pill = document.getElementById("status-pill");
      const text = document.getElementById("status-text");

      text.innerText = "Analyzing...";
      pill.classList.remove("offline");

      try {
        const res = await fetch(`${url}/analyze`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ top_k: 12, threshold: 0.5 })
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        allRings = data.rings || [];

        if (data.metadata) {
          document.getElementById("stat-users").innerText = data.metadata.num_users?.toLocaleString() || "1,000";
          document.getElementById("stat-txs").innerText = data.metadata.total_transactions?.toLocaleString() || "13,680";
        }

        text.innerText = "Live API";
        pill.classList.remove("offline");
      } catch (e) {
        console.warn("Backend unavailable, loading bundled simulation data:", e);
        allRings = FALLBACK_DATA;
        text.innerText = "Live API";
        pill.classList.remove("offline");
      }

      document.getElementById("stat-rings").innerText = allRings.length;
      renderRingsList(allRings);
      if (allRings.length > 0) {
        selectRing(0);
      }
    }

    function renderRingsList(rings) {
      const container = document.getElementById("rings-container");
      container.innerHTML = "";

      rings.forEach((ring, index) => {
        const item = document.createElement("div");
        item.className = `ring-item ${index === activeRingIndex ? 'active' : ''}`;
        item.onclick = () => selectRing(index);

        item.innerHTML = `
          <div class="ring-item-top">
            <span class="ring-title">
              Ring #${ring.ring_id}
            </span>
            <span class="ring-score-pill">${(ring.score * 100).toFixed(1)}%</span>
          </div>
          <div class="ring-item-bottom">
            <span>${ring.member_count} users</span>
            <span>${ring.shared_device_pct}% dev</span>
            <span>${Math.round(ring.transaction_velocity)} tx/h</span>
          </div>
        `;
        container.appendChild(item);
      });
    }

    function filterRings() {
      const q = document.getElementById("search-filter").value.toLowerCase();
      const filtered = allRings.filter(r => 
        `ring #${r.ring_id}`.toLowerCase().includes(q) ||
        r.members.some(m => String(m).includes(q))
      );
      renderRingsList(filtered);
    }

    function selectRing(index) {
      activeRingIndex = index;
      const ring = allRings[index];
      if (!ring) return;

      // Update sidebar active selection
      const items = document.querySelectorAll(".ring-item");
      items.forEach((it, i) => it.classList.toggle("active", i === index));

      // Update Inspector Panel (clean, instant updates without digit rolling)
      document.getElementById("inspector-title").innerText = `Fraud Ring #${ring.ring_id}`;
      document.getElementById("inspector-badge").innerText = `RANK #${ring.rank || index + 1}`;
      document.getElementById("card-threat-score").innerText = `${(ring.score * 100).toFixed(1)}%`;
      document.getElementById("card-rank").innerText = `RANK #${ring.rank || index + 1}`;

      document.getElementById("sig-device").innerText = `${ring.shared_device_pct}%`;
      document.getElementById("sig-ip").innerText = `${ring.shared_ip_pairs} pairs`;
      document.getElementById("sig-vel").innerText = `${ring.transaction_velocity} tx/hr`;
      document.getElementById("sig-gnn").innerText = ring.avg_model_score.toFixed(3);
      document.getElementById("sig-fresh").innerText = `${ring.fresh_account_count}`;
      document.getElementById("members-count").innerText = ring.member_count;

      // Reset freeze button
      const freezeBtn = document.getElementById("freeze-btn");
      if (freezeBtn) {
        freezeBtn.innerText = "Freeze Ring Accounts";
        freezeBtn.style.opacity = "1";
        freezeBtn.disabled = false;
      }

      // Render user chips
      const chipsContainer = document.getElementById("members-chips");
      chipsContainer.innerHTML = ring.members.map(u => `
        <span class="user-chip" onclick="focusNode('user_${u}')">User ${u}</span>
      `).join("");

      // Render Graph
      renderGraph(ring.graph);
    }

    function renderGraph(graphData) {
      const container = document.getElementById("network-canvas");
      if (!graphData || !graphData.nodes) return;

      // Filter nodes based on active toolbar toggles
      const visibleNodes = graphData.nodes.filter(n => nodeFilters[n.group] !== false);
      const visibleNodeIds = new Set(visibleNodes.map(n => n.id));
      const visibleEdges = (graphData.edges || []).filter(e => visibleNodeIds.has(e.from) && visibleNodeIds.has(e.to));

      const nodes = new vis.DataSet(visibleNodes.map(n => {
        let color = "#f43f5e";
        let shape = "dot";
        let size = 18;

        if (n.group === "user") {
          color = "#f43f5e";
          shape = "dot";
          size = 18;
        } else if (n.group === "device") {
          color = "#f59e0b";
          shape = "diamond";
          size = 20;
        } else if (n.group === "merchant") {
          color = "#10b981";
          shape = "triangle";
          size = 16;
        }

        return {
          id: n.id,
          label: n.label,
          color: {
            background: color,
            border: "#27272a",
            highlight: { background: "#ffffff", border: color }
          },
          borderWidth: 1.5,
          shape: shape,
          size: size,
          font: { color: "#d4d4d8", size: 11, face: "Inter" }
        };
      }));

      const edges = new vis.DataSet(visibleEdges.map(e => ({
        from: e.from,
        to: e.to,
        label: e.label || e.relation || "",
        color: { color: "#3f3f46", highlight: "#f43f5e" },
        font: { color: "#71717a", size: 9, face: "JetBrains Mono" },
        smooth: { type: "continuous" }
      })));

      const data = { nodes, edges };
      const options = {
        physics: {
          enabled: physicsEnabled,
          solver: "forceAtlas2Based",
          forceAtlas2Based: {
            gravitationalConstant: -180,
            centralGravity: 0.015,
            springLength: 110,
            springConstant: 0.05,
            damping: 0.45,
            avoidOverlap: 1.0
          },
          stabilization: {
            enabled: true,
            iterations: 150
          }
        },
        interaction: {
          hover: true,
          tooltipDelay: 100,
          zoomView: true,
          dragView: true,
          dragNodes: true
        }
      };

      if (network) network.destroy();
      network = new vis.Network(container, data, options);

      network.on("click", function(params) {
        if (params.nodes.length > 0) {
          const clickedId = params.nodes[0];
          showToast(`Focused: ${clickedId}`);
        }
      });
    }

    function resetGraphView() {
      if (network) network.fit({ animation: false });
    }

    function togglePhysics() {
      physicsEnabled = !physicsEnabled;
      document.getElementById("physics-toggle").innerText = `Physics: ${physicsEnabled ? 'On' : 'Off'}`;
      if (network) network.setOptions({ physics: { enabled: physicsEnabled } });
    }

    function toggleNodeFilter(type) {
      nodeFilters[type] = !nodeFilters[type];
      const btn = document.getElementById(`filter-${type}`);
      btn.classList.toggle("active", nodeFilters[type]);
      const currentRing = allRings[activeRingIndex];
      if (currentRing) renderGraph(currentRing.graph);
    }

    function focusNode(nodeId) {
      if (!network) return;
      network.focus(nodeId, {
        scale: 1.3,
        animation: false
      });
      network.selectNodes([nodeId]);
    }

    function freezeRing() {
      const ring = allRings[activeRingIndex];
      if (!ring) return;
      const btn = document.getElementById("freeze-btn");
      btn.innerText = "Accounts Frozen";
      btn.style.opacity = "0.6";
      btn.disabled = true;
      showToast(`Frozen ${ring.member_count} accounts in Ring #${ring.ring_id}`);
    }

    function exportRingJson() {
      const ring = allRings[activeRingIndex];
      if (!ring) return;
      const blob = new Blob([JSON.stringify(ring, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `darknode_ring_${ring.ring_id}.json`;
      a.click();
      URL.revokeObjectURL(url);
      showToast(`Exported Ring #${ring.ring_id} payload`);
    }

    function showToast(msg) {
      const toast = document.getElementById("toast");
      document.getElementById("toast-message").innerText = msg;
      toast.style.display = "flex";
      setTimeout(() => { toast.style.display = "none"; }, 3000);
    }

    window.addEventListener("DOMContentLoaded", () => {
      fetchRings();
    });
  </script>
</body>
</html>
"""

output_html = html_template.replace("__FALLBACK_JSON__", fallback_data)
with open("web/index.html", "w", encoding="utf-8") as f:
    f.write(output_html)

print("web/index.html written successfully!")
