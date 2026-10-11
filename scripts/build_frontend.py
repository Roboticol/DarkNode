"""Build web/index.html with:
1. Always-visible constant-size screen text labels across all zoom levels.
2. Dynamic zoom-reactive physics animation:
   - Zoom out -> nodes smoothly pull closer together into a compact cluster.
   - Zoom in  -> nodes smoothly spread out freely with open spacing.
3. Clean, raw professional symbols/SVGs with all playful/AI emojis removed.
4. Embedded real forward-pass rings from trained model.
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
  <title>DarkNode — Fraud Syndicate Graph Intelligence</title>
  <!-- Vis-network CDN -->
  <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <!-- Plus Jakarta Sans & JetBrains Mono Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">

  <style>
    :root {
      /* Dark Grey Theme */
      --bg-base: #111215;
      --bg-panel: #18191e;
      --bg-card: #20222a;
      --bg-card-hover: #272a34;
      --bg-input: #141519;
      
      --border-subtle: #2b2e38;
      --border-strong: #3b3f4d;
      
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
      --text-dim: #6b7280;
      
      /* Vibrant Electric Yellow Accents */
      --yellow-primary: #facc15;
      --yellow-hover: #fde047;
      --yellow-dim: #ca8a04;
      --yellow-bg: rgba(250, 204, 21, 0.12);
      --yellow-border: rgba(250, 204, 21, 0.35);
      
      /* Node Entity Colors */
      --node-user: #facc15;
      --node-device: #38bdf8;
      --node-merchant: #34d399;
      
      --shadow-card: 0 4px 20px -2px rgba(0, 0, 0, 0.45);
      --shadow-glow: 0 0 16px rgba(250, 204, 21, 0.2);
      
      --radius: 12px;
      --radius-sm: 8px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg-base);
      color: var(--text-main);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      -webkit-font-smoothing: antialiased;
    }

    /* Top Navigation Bar */
    header {
      background: var(--bg-panel);
      border-bottom: 1px solid var(--border-subtle);
      height: 56px;
      padding: 0 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
      z-index: 50;
    }

    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-logo-mark {
      width: 28px;
      height: 28px;
      border-radius: 8px;
      background: var(--yellow-primary);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: var(--shadow-glow);
    }

    .brand-title {
      font-size: 17px;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .brand-title span.kicker {
      color: var(--yellow-primary);
    }

    .badge-pill {
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 6px;
      background: var(--bg-card);
      color: var(--yellow-primary);
      border: 1px solid var(--yellow-border);
    }

    /* Telemetry Stats */
    .header-stats {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .stat-pill {
      display: flex;
      align-items: center;
      gap: 6px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      padding: 5px 10px;
      border-radius: 7px;
      font-size: 11px;
      color: var(--text-muted);
    }

    .stat-val {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: var(--text-main);
    }

    /* Controls */
    .header-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .api-box {
      display: flex;
      align-items: center;
      background: var(--bg-input);
      border: 1px solid var(--border-subtle);
      border-radius: 7px;
      padding: 4px 10px;
      gap: 8px;
    }

    .api-box input {
      background: transparent;
      border: none;
      color: var(--text-main);
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      width: 160px;
      outline: none;
    }

    .status-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #34d399;
      box-shadow: 0 0 8px rgba(52, 211, 153, 0.6);
    }

    .status-dot.offline {
      background: var(--yellow-primary);
      box-shadow: 0 0 8px rgba(250, 204, 21, 0.6);
    }

    .status-text {
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      font-weight: 600;
      color: var(--text-muted);
      letter-spacing: 0.04em;
    }

    .btn {
      height: 32px;
      padding: 0 14px;
      border-radius: 7px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      border: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.15s ease;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .btn-yellow {
      background: var(--yellow-primary);
      color: #111215;
      box-shadow: 0 2px 10px rgba(250, 204, 21, 0.25);
    }

    .btn-yellow:hover {
      background: var(--yellow-hover);
      box-shadow: 0 4px 14px rgba(250, 204, 21, 0.35);
    }

    .btn-outline {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
    }

    .btn-outline:hover {
      background: var(--bg-card-hover);
      border-color: var(--border-strong);
    }

    /* Main Workspace */
    .workspace {
      display: flex;
      flex: 1;
      gap: 12px;
      padding: 12px 16px;
      height: calc(100vh - 56px);
      overflow: hidden;
      box-sizing: border-box;
    }

    /* Panels */
    .panel-card {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius);
      box-shadow: var(--shadow-card);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    /* Left Sidebar: Rings Directory */
    .sidebar-left {
      width: 320px;
      flex-shrink: 0;
      height: 100%;
    }

    .panel-header-clean {
      padding: 12px 16px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(24, 25, 30, 0.6);
    }

    .panel-title {
      font-size: 12px;
      font-weight: 700;
      color: var(--text-main);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .search-box-clean {
      padding: 10px 14px;
      border-bottom: 1px solid var(--border-subtle);
      background: var(--bg-panel);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .search-input-clean {
      width: 100%;
      background: var(--bg-input);
      border: 1px solid var(--border-subtle);
      border-radius: 7px;
      padding: 7px 10px;
      font-size: 11px;
      color: var(--text-main);
      outline: none;
      font-family: inherit;
    }

    .search-input-clean:focus {
      border-color: var(--yellow-primary);
    }

    .rings-list-scroll {
      flex: 1;
      overflow-y: auto;
      padding: 8px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    /* Ring Card Item */
    .ring-card-item {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 9px;
      padding: 10px 12px;
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      flex-direction: column;
      gap: 6px;
      position: relative;
    }

    .ring-card-item:hover {
      background: var(--bg-card-hover);
      border-color: var(--border-strong);
    }

    .ring-card-item.active {
      background: #252834;
      border-color: var(--yellow-primary);
      box-shadow: 0 2px 10px rgba(250, 204, 21, 0.15);
    }

    .ring-card-item.active::before {
      content: "";
      position: absolute;
      left: 0;
      top: 8px;
      bottom: 8px;
      width: 3.5px;
      border-radius: 0 4px 4px 0;
      background: var(--yellow-primary);
    }

    .ring-card-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .ring-label {
      font-size: 12px;
      font-weight: 700;
      color: var(--text-main);
    }

    .ring-risk-tag {
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 5px;
      background: var(--yellow-bg);
      color: var(--yellow-primary);
      border: 1px solid var(--yellow-border);
    }

    .ring-card-bottom {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 11px;
      color: var(--text-muted);
    }

    .raw-stat-pill {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .raw-stat-pill svg {
      opacity: 0.75;
    }

    /* Center Viewport: Spacious Graph */
    .viewport-center {
      flex: 1;
      min-width: 0;
      height: 100%;
      position: relative;
      background: #14151a;
      display: flex;
      flex-direction: column;
    }

    /* Fixed Canvas Wrapper */
    .canvas-outer {
      position: relative;
      flex: 1;
      width: 100%;
      height: 100%;
      min-height: 450px;
      overflow: hidden;
      background-color: #14151a;
      background-image: radial-gradient(#252834 1.2px, transparent 1.2px);
      background-size: 24px 24px;
    }

    #network-canvas {
      position: absolute;
      top: 0;
      left: 0;
      width: 100% !important;
      height: 100% !important;
    }

    /* Floating Graph Bar */
    .canvas-bar {
      position: absolute;
      top: 14px;
      left: 14px;
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(24, 25, 30, 0.94);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 5px 8px;
      box-shadow: var(--shadow-card);
      z-index: 10;
    }

    .canvas-pill-btn {
      height: 26px;
      padding: 0 10px;
      border-radius: 5px;
      border: 1px solid transparent;
      background: transparent;
      color: var(--text-muted);
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.12s ease;
      font-family: inherit;
    }

    .canvas-pill-btn:hover {
      background: var(--bg-card);
      color: var(--text-main);
    }

    .canvas-pill-btn.active {
      background: var(--bg-card);
      border-color: var(--border-strong);
      color: var(--yellow-primary);
    }

    /* Legend Floating Pill */
    .canvas-legend {
      position: absolute;
      bottom: 54px;
      left: 14px;
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(24, 25, 30, 0.94);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-subtle);
      border-radius: 7px;
      padding: 6px 12px;
      box-shadow: var(--shadow-card);
      font-size: 11px;
      font-weight: 600;
      color: var(--text-muted);
      z-index: 10;
    }

    .legend-indicator {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .legend-dot {
      width: 9px;
      height: 9px;
      border-radius: 50%;
    }

    .legend-diamond {
      width: 9px;
      height: 9px;
      transform: rotate(45deg);
    }

    /* Bottom Architecture Banner */
    .key-detail-banner {
      background: rgba(24, 25, 30, 0.95);
      border-top: 1px solid var(--border-subtle);
      padding: 8px 16px;
      font-size: 11px;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
      z-index: 5;
    }

    .key-detail-banner strong {
      font-weight: 700;
      color: var(--yellow-primary);
    }

    /* Right Sidebar: Evidence & Signals Panel */
    .sidebar-right {
      width: 340px;
      flex-shrink: 0;
      height: 100%;
      overflow-y: auto;
    }

    .inspector-content {
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    /* Hero Risk Box */
    .hero-risk-box {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-left: 4px solid var(--yellow-primary);
      border-radius: 9px;
      padding: 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .hero-score-val {
      font-family: 'JetBrains Mono', monospace;
      font-size: 30px;
      font-weight: 800;
      line-height: 1;
      color: var(--yellow-primary);
    }

    .hero-score-sub {
      font-size: 10px;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-top: 4px;
    }

    .hero-rank-badge {
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 5px;
      background: var(--yellow-bg);
      color: var(--yellow-primary);
      border: 1px solid var(--yellow-border);
    }

    .block-title {
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 8px;
    }

    /* Signals List */
    .signals-card-group {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 9px;
      overflow: hidden;
    }

    .signal-item-row {
      padding: 9px 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border-subtle);
      font-size: 11px;
    }

    .signal-item-row:last-child {
      border-bottom: none;
    }

    .signal-prefix-tag {
      font-family: 'JetBrains Mono', monospace;
      font-size: 9px;
      font-weight: 700;
      padding: 1px 4px;
      border-radius: 3px;
      background: var(--bg-panel);
      color: var(--yellow-primary);
      border: 1px solid var(--border-subtle);
      margin-right: 6px;
    }

    .signal-label-text {
      color: var(--text-muted);
      display: inline-flex;
      align-items: center;
    }

    .signal-metric-val {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: var(--text-main);
    }

    /* Account Chips Grid */
    .user-chips-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      max-height: 130px;
      overflow-y: auto;
      padding: 8px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 9px;
    }

    .chip-account {
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 5px;
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      color: var(--yellow-primary);
      cursor: pointer;
      transition: all 0.12s ease;
    }

    .chip-account:hover {
      background: var(--yellow-bg);
      border-color: var(--yellow-primary);
    }

    /* Toast Alert */
    .toast-popup {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--bg-card);
      border: 1px solid var(--border-strong);
      border-left: 4px solid var(--yellow-primary);
      border-radius: 8px;
      padding: 10px 16px;
      font-size: 12px;
      display: none;
      align-items: center;
      gap: 10px;
      z-index: 1000;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    .toast-dot-glow {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--yellow-primary);
      box-shadow: 0 0 8px rgba(250, 204, 21, 0.8);
    }
  </style>
</head>
<body>

  <!-- Top Header Navigation -->
  <header>
    <div class="brand-group">
      <div class="brand-logo-mark">
        <!-- Raw Network Graph Node Glyph -->
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#111215" stroke-width="2.5"><circle cx="12" cy="12" r="3"/><circle cx="19" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><line x1="12" y1="9" x2="19" y2="6.5"/><line x1="12" y1="15" x2="5" y2="17.5"/></svg>
      </div>
      <div class="brand-title">
        Dark<span class="kicker">Node</span>
        <span class="badge-pill">GNN-MPNN</span>
      </div>
    </div>

    <!-- Header Stats -->
    <div class="header-stats">
      <div class="stat-pill">
        <span>USR:</span>
        <span class="stat-val" id="stat-users">1,000</span>
      </div>
      <div class="stat-pill">
        <span>TXS:</span>
        <span class="stat-val" id="stat-txs">13,680</span>
      </div>
      <div class="stat-pill">
        <span>RINGS:</span>
        <span class="stat-val" id="stat-rings" style="color: var(--yellow-primary);">10</span>
      </div>
    </div>

    <!-- Controls -->
    <div class="header-actions">
      <div class="api-box">
        <div class="status-dot" id="status-dot"></div>
        <input type="text" id="api-url" value="http://localhost:8000" placeholder="http://localhost:8000">
        <span class="status-text" id="status-label">ONLINE</span>
      </div>

      <button class="btn btn-yellow" onclick="fetchRings()">
        <svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
        Run Analysis
      </button>
    </div>
  </header>

  <!-- Spacious Workspace (3 Floating Panels) -->
  <div class="workspace">

    <!-- Panel 1: Left Rings Directory -->
    <div class="panel-card sidebar-left">
      <div class="panel-header-clean">
        <span class="panel-title">Detected Syndicates</span>
        <span class="badge-pill" id="rings-count-badge">10 total</span>
      </div>
      <div class="search-box-clean">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#6b7280" stroke-width="2.2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input type="text" class="search-input-clean" id="search-filter" placeholder="Filter by Ring ID or User ID..." oninput="filterRings()">
      </div>
      <div class="rings-list-scroll" id="rings-container">
        <!-- Injected rings -->
      </div>
    </div>

    <!-- Panel 2: Center Viewport (Network Graph Canvas) -->
    <div class="panel-card viewport-center">
      <!-- Floating Toolbar -->
      <div class="canvas-bar">
        <button class="canvas-pill-btn active" onclick="resetGraphView()">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>
          Fit View
        </button>
        <button class="canvas-pill-btn" id="spread-btn" onclick="spreadGraph()">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
          <span id="spread-label">Spread Out</span>
        </button>
        <button class="canvas-pill-btn" id="physics-toggle" onclick="togglePhysics()">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          <span id="physics-label">Physics: On</span>
        </button>
        <span style="color: var(--border-subtle);">|</span>
        <button class="canvas-pill-btn active" id="filter-user" onclick="toggleFilter('user')">Users</button>
        <button class="canvas-pill-btn active" id="filter-device" onclick="toggleFilter('device')">Devices</button>
        <button class="canvas-pill-btn active" id="filter-merchant" onclick="toggleFilter('merchant')">Merchants</button>
      </div>

      <!-- Graph Canvas Container (Guaranteed non-collapsing) -->
      <div class="canvas-outer">
        <div id="network-canvas"></div>
      </div>

      <!-- Clean Floating Legend -->
      <div class="canvas-legend">
        <div class="legend-indicator">
          <div class="legend-dot" style="background: var(--node-user);"></div>
          <span>Syndicate Member</span>
        </div>
        <div class="legend-indicator">
          <div class="legend-diamond" style="background: var(--node-device);"></div>
          <span>Shared Device</span>
        </div>
        <div class="legend-indicator">
          <div class="legend-dot" style="background: var(--node-merchant); border-radius: 2px;"></div>
          <span>Target Merchant</span>
        </div>
      </div>

      <!-- Bottom Insight Banner -->
      <div class="key-detail-banner">
        <strong>Architectural Signal:</strong>
        <span>Heterogeneous Message Passing propagates embeddings across device, IP, and transaction hops to eliminate heuristic false alarms.</span>
      </div>
    </div>

    <!-- Panel 3: Right Inspector & Evidence Panel -->
    <div class="panel-card sidebar-right">
      <div class="panel-header-clean">
        <span class="panel-title" id="inspector-heading">Syndicate Dossier</span>
        <span class="badge-pill" id="inspector-badge">RANK #1</span>
      </div>

      <div class="inspector-content">
        <!-- Hero Threat Score Card -->
        <div class="hero-risk-box">
          <div>
            <div class="hero-score-val" id="threat-score-num">--</div>
            <div class="hero-score-sub">Threat Risk Score</div>
          </div>
          <div class="hero-rank-badge" id="threat-rank-pill">
            RANK #1
          </div>
        </div>

        <!-- Evidence Signals -->
        <div>
          <div class="block-title">Behavioral Reason Signals</div>
          <div class="signals-card-group">
            <div class="signal-item-row">
              <span class="signal-label-text"><span class="signal-prefix-tag">DEV</span>Shared Device Ratio</span>
              <span class="signal-metric-val" id="sig-device">0%</span>
            </div>
            <div class="signal-item-row">
              <span class="signal-label-text"><span class="signal-prefix-tag">NET</span>Shared IP Pairs</span>
              <span class="signal-metric-val" id="sig-ip">0 pairs</span>
            </div>
            <div class="signal-item-row">
              <span class="signal-label-text"><span class="signal-prefix-tag">VEL</span>Burst Velocity</span>
              <span class="signal-metric-val" id="sig-vel">0 tx/hr</span>
            </div>
            <div class="signal-item-row">
              <span class="signal-label-text"><span class="signal-prefix-tag">GNN</span>Model Confidence</span>
              <span class="signal-metric-val" id="sig-gnn">0.00</span>
            </div>
            <div class="signal-item-row">
              <span class="signal-label-text"><span class="signal-prefix-tag">NEW</span>New Accounts Ratio</span>
              <span class="signal-metric-val" id="sig-fresh">0</span>
            </div>
          </div>
        </div>

        <!-- Member Accounts -->
        <div>
          <div class="block-title">Syndicate Accounts (<span id="members-count">0</span>)</div>
          <div class="user-chips-grid" id="members-chips">
            <!-- Account Chips -->
          </div>
        </div>

        <!-- Compliance & Export Actions -->
        <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 4px;">
          <button class="btn btn-yellow" id="freeze-btn" style="height: 36px;" onclick="simulateFreeze()">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            Freeze Ring Accounts (Simulation)
          </button>
          <button class="btn btn-outline" style="height: 34px;" onclick="exportJson()">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            Export Ring Dossier (JSON)
          </button>
        </div>
      </div>
    </div>

  </div>

  <!-- Toast Alert -->
  <div class="toast-popup" id="toast">
    <div class="toast-dot-glow"></div>
    <span id="toast-text">Action executed.</span>
  </div>

  <script>
    let network = null;
    let allRings = [];
    let activeIndex = 0;
    let physicsState = true;
    let currentSpringLength = 260;
    let activeFilters = { user: true, device: true, merchant: true };
    let currentVisibleNodes = [];

    // Real fallback dataset extracted from trained GNN model
    const FALLBACK_RINGS = __FALLBACK_JSON__;

    async function fetchRings() {
      const url = document.getElementById("api-url").value.trim().replace(/\\/$/, "");
      const dot = document.getElementById("status-dot");
      const label = document.getElementById("status-label");

      try {
        const res = await fetch(`${url}/analyze`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ top_k: 10, threshold: 0.5 })
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        allRings = data.rings || [];

        if (data.metadata) {
          document.getElementById("stat-users").innerText = data.metadata.num_users?.toLocaleString() || "1,000";
          document.getElementById("stat-txs").innerText = data.metadata.total_transactions?.toLocaleString() || "13,680";
        }
        dot.classList.remove("offline");
        label.innerText = "LIVE API";
        showToast("Connected to DarkNode GNN backend");
      } catch (err) {
        console.warn("Backend unavailable, using cached model dossier:", err);
        allRings = FALLBACK_RINGS;
        dot.classList.add("offline");
        label.innerText = "CACHED GNN";
      }

      document.getElementById("stat-rings").innerText = allRings.length;
      document.getElementById("rings-count-badge").innerText = `${allRings.length} total`;
      renderRingsList(allRings);
      if (allRings.length > 0) {
        selectRing(0);
      }
    }

    function renderRingsList(rings) {
      const container = document.getElementById("rings-container");
      container.innerHTML = "";

      rings.forEach((ring, index) => {
        const card = document.createElement("div");
        card.className = `ring-card-item ${index === activeIndex ? 'active' : ''}`;
        card.onclick = () => selectRing(index);

        card.innerHTML = `
          <div class="ring-card-top">
            <span class="ring-label">Syndicate Ring #${ring.ring_id}</span>
            <span class="ring-risk-tag">${(ring.score * 100).toFixed(1)}% RISK</span>
          </div>
          <div class="ring-card-bottom">
            <span class="raw-stat-pill">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
              ${ring.member_count} USR
            </span>
            <span class="raw-stat-pill">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>
              ${ring.shared_device_pct}% DEV
            </span>
            <span class="raw-stat-pill">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
              ${Math.round(ring.transaction_velocity)} TX/H
            </span>
          </div>
        `;
        container.appendChild(card);
      });
    }

    function filterRings() {
      const query = document.getElementById("search-filter").value.toLowerCase();
      const filtered = allRings.filter(r => 
        `ring #${r.ring_id}`.toLowerCase().includes(query) ||
        r.members.some(m => String(m).includes(query))
      );
      renderRingsList(filtered);
    }

    function selectRing(index) {
      activeIndex = index;
      const ring = allRings[index];
      if (!ring) return;

      // Update Active States
      const cards = document.querySelectorAll(".ring-card-item");
      cards.forEach((c, i) => c.classList.toggle("active", i === index));

      // Update Inspector Panel
      document.getElementById("inspector-heading").innerText = `Syndicate #${ring.ring_id}`;
      document.getElementById("inspector-badge").innerText = `RANK #${ring.rank || index + 1}`;
      document.getElementById("threat-score-num").innerText = `${(ring.score * 100).toFixed(1)}%`;
      document.getElementById("threat-rank-pill").innerText = `RANK #${ring.rank || index + 1}`;

      document.getElementById("sig-device").innerText = `${ring.shared_device_pct}%`;
      document.getElementById("sig-ip").innerText = `${ring.shared_ip_pairs} pairs`;
      document.getElementById("sig-vel").innerText = `${ring.transaction_velocity} tx/hr`;
      document.getElementById("sig-gnn").innerText = ring.avg_model_score.toFixed(3);
      document.getElementById("sig-fresh").innerText = `${ring.fresh_account_count} accounts`;
      document.getElementById("members-count").innerText = ring.member_count;

      // Reset freeze button
      const freezeBtn = document.getElementById("freeze-btn");
      freezeBtn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg> Freeze Ring Accounts (Simulation)`;
      freezeBtn.disabled = false;
      freezeBtn.style.opacity = "1";

      // Render Account Chips
      const chipsBox = document.getElementById("members-chips");
      chipsBox.innerHTML = ring.members.map(m => `
        <span class="chip-account" onclick="focusOnNode('user_${m}')">User ${m}</span>
      `).join("");

      // Render Graph
      renderGraph(ring.graph);
    }

    function renderGraph(graphData) {
      const container = document.getElementById("network-canvas");
      if (!container || !graphData || !graphData.nodes) return;

      // Filter Nodes
      const visibleNodes = graphData.nodes.filter(n => activeFilters[n.group] !== false);
      currentVisibleNodes = visibleNodes;
      const visibleIds = new Set(visibleNodes.map(n => n.id));
      const visibleEdges = (graphData.edges || []).filter(e => visibleIds.has(e.from) && visibleIds.has(e.to));

      const nodes = new vis.DataSet(visibleNodes.map(n => {
        let color = "#facc15";
        let shape = "dot";
        let size = 20;

        if (n.group === "user") {
          color = "#facc15"; // Electric Yellow
          shape = "dot";
          size = 20;
        } else if (n.group === "device") {
          color = "#38bdf8"; // Cyan
          shape = "diamond";
          size = 22;
        } else if (n.group === "merchant") {
          color = "#34d399"; // Mint
          shape = "triangle";
          size = 18;
        }

        return {
          id: n.id,
          label: " ", // We use afterDrawing canvas overlay for constant-size crisp labels!
          actualLabel: n.label,
          group: n.group,
          color: {
            background: color,
            border: "#ffffff",
            highlight: { background: "#ffffff", border: color }
          },
          borderWidth: 2,
          shape: shape,
          size: size,
          shadow: { enabled: true, color: "rgba(0, 0, 0, 0.6)", size: 6, x: 0, y: 3 }
        };
      }));

      // Clean, airy edges with hover tooltips
      const edges = new vis.DataSet(visibleEdges.map(e => {
        let edgeColor = "#64748b";
        let dashes = false;
        let width = 1.6;
        let tooltip = `Connected (${e.count || 1} links)`;

        if (e.relation === "shared_ip") {
          edgeColor = "#facc15";
          dashes = [5, 5];
          width = 2.2;
          tooltip = `Shared IP Interconnection (${e.count || 1} links)`;
        } else if (e.relation === "shared_device" || e.relation === "connected") {
          edgeColor = "#38bdf8";
          width = 2.2;
          tooltip = `Shared Hardware Device (${e.count || 1} links)`;
        } else if (e.relation === "transaction" || e.relation === "burst_tx") {
          edgeColor = "#475569";
          width = 1.4;
          tooltip = `Merchant Transaction Burst (${e.count || 1} txs)`;
        }

        return {
          from: e.from,
          to: e.to,
          color: { color: edgeColor, highlight: "#facc15", hover: "#facc15" },
          dashes: dashes,
          width: width,
          title: tooltip,
          smooth: { type: "continuous", roundness: 0.25 }
        };
      }));

      const data = { nodes, edges };

      // Physics configuration
      const options = {
        physics: {
          enabled: physicsState,
          solver: "forceAtlas2Based",
          forceAtlas2Based: {
            gravitationalConstant: -460,
            centralGravity: 0.002,
            springLength: currentSpringLength,
            springConstant: 0.035,
            damping: 0.28,
            avoidOverlap: 1.0
          },
          stabilization: { iterations: 180 }
        },
        interaction: {
          hover: true,
          tooltipDelay: 80,
          zoomView: true,
          dragView: true
        }
      };

      if (network) network.destroy();
      network = new vis.Network(container, data, options);

      network.once("stabilizationIterationsDone", function() {
        network.fit({ animation: { duration: 400, easingFunction: "easeInOutQuad" } });
      });

      // =========================================================================
      // 1. CONSTANT SCREEN TEXT SIZE & VISIBILITY AT ALL ZOOM LEVELS
      // =========================================================================
      // Rendered directly in native 1:1 screen pixel coordinates via afterDrawing.
      // Text size stays precisely 11px on screen whether zoomed in or zoomed out!
      network.on("afterDrawing", function(ctx) {
        ctx.save();
        // Reset canvas matrix to 1:1 screen device pixels
        ctx.setTransform(1, 0, 0, 1, 0, 0);

        const positions = network.getPositions();
        ctx.font = "600 11px 'JetBrains Mono', monospace";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";

        for (const node of currentVisibleNodes) {
          const pos = positions[node.id];
          if (!pos) continue;
          const domPos = network.canvasToDOM({ x: pos.x, y: pos.y });

          // Skip drawing if outside viewport
          if (domPos.x < -60 || domPos.x > container.clientWidth + 60 ||
              domPos.y < -60 || domPos.y > container.clientHeight + 60) {
            continue;
          }

          const labelText = node.label;
          const yOffset = (node.group === "device" ? 22 : 18);
          const textX = domPos.x;
          const textY = domPos.y + yOffset;

          // Crisp dark background pill for high contrast
          const textWidth = ctx.measureText(labelText).width;
          ctx.fillStyle = "rgba(17, 18, 22, 0.92)";
          ctx.beginPath();
          ctx.roundRect(textX - textWidth / 2 - 5, textY - 8, textWidth + 10, 16, 4);
          ctx.fill();

          // Subtle entity outline border
          ctx.strokeStyle = node.group === "user" ? "rgba(250, 204, 21, 0.4)" : (node.group === "device" ? "rgba(56, 189, 248, 0.4)" : "rgba(52, 211, 153, 0.4)");
          ctx.lineWidth = 0.8;
          ctx.stroke();

          // Text fill color
          ctx.fillStyle = node.group === "user" ? "#facc15" : (node.group === "device" ? "#38bdf8" : "#34d399");
          ctx.fillText(labelText, textX, textY);
        }

        ctx.restore();
      });

      // =========================================================================
      // 2. DYNAMIC ZOOM ANIMATION
      // =========================================================================
      // When Zoom Out: springs contract, central gravity gently pulls in -> nodes smoothly group together!
      // When Zoom In:  springs expand, strong repulsion pushes out -> nodes freely spread out!
      network.on("zoom", function(params) {
        if (!physicsState) return;
        const s = params.scale;

        let targetSpring, targetGravity, targetCentral;

        if (s < 1.0) {
          // Zoomed Out: cluster smoothly contracts together
          const t = Math.max(0, (s - 0.25) / 0.75); // 0 at s=0.25, 1 at s=1.0
          targetSpring = Math.round(110 + (260 - 110) * t);
          targetGravity = Math.round(-150 + (-460 - -150) * t);
          targetCentral = 0.022 + (0.002 - 0.022) * t;
        } else {
          // Zoomed In: cluster smoothly spreads freely apart
          const t = Math.min(1.5, s - 1.0);
          targetSpring = Math.round(260 + 120 * t);
          targetGravity = Math.round(-460 - 180 * t);
          targetCentral = Math.max(0.0005, 0.002 - 0.001 * t);
        }

        network.setOptions({
          physics: {
            forceAtlas2Based: {
              springLength: targetSpring,
              gravitationalConstant: targetGravity,
              centralGravity: targetCentral
            }
          }
        });

        // Trigger dynamic animation step
        network.startSimulation();
      });

      // Click node to focus
      network.on("click", function(params) {
        if (params.nodes.length > 0) {
          showToast(`Focused: ${params.nodes[0]}`);
        }
      });
    }

    function resetGraphView() {
      if (network) network.fit({ animation: { duration: 400, easingFunction: "easeInOutQuad" } });
    }

    function spreadGraph() {
      currentSpringLength = (currentSpringLength === 260) ? 380 : 260;
      const btn = document.getElementById("spread-btn");
      const label = document.getElementById("spread-label");
      label.innerText = currentSpringLength === 380 ? "Spread: Wide" : "Spread Out";
      btn.classList.toggle("active", currentSpringLength === 380);

      if (network) {
        network.setOptions({
          physics: {
            forceAtlas2Based: { springLength: currentSpringLength, gravitationalConstant: currentSpringLength === 380 ? -620 : -460 }
          }
        });
        network.startSimulation();
      }
    }

    function togglePhysics() {
      physicsState = !physicsState;
      const label = document.getElementById("physics-label");
      label.innerText = `Physics: ${physicsState ? 'On' : 'Off'}`;
      if (network) network.setOptions({ physics: { enabled: physicsState } });
    }

    function toggleFilter(type) {
      activeFilters[type] = !activeFilters[type];
      const btn = document.getElementById(`filter-${type}`);
      btn.classList.toggle("active", activeFilters[type]);
      const currentRing = allRings[activeIndex];
      if (currentRing) renderGraph(currentRing.graph);
    }

    function focusOnNode(nodeId) {
      if (!network) return;
      network.focus(nodeId, {
        scale: 1.3,
        animation: { duration: 500, easingFunction: "easeInOutQuad" }
      });
      network.selectNodes([nodeId]);
    }

    function simulateFreeze() {
      const ring = allRings[activeIndex];
      if (!ring) return;
      const btn = document.getElementById("freeze-btn");
      btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg> Accounts Suspended (Simulation)`;
      btn.disabled = true;
      btn.style.opacity = "0.7";
      showToast(`Simulation: Suspended ${ring.member_count} syndicate accounts in Ring #${ring.ring_id}`);
    }

    function exportJson() {
      const ring = allRings[activeIndex];
      if (!ring) return;
      const blob = new Blob([JSON.stringify(ring, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `darknode_syndicate_${ring.ring_id}.json`;
      a.click();
      URL.revokeObjectURL(url);
      showToast(`Exported Ring #${ring.ring_id} dossier.`);
    }

    function showToast(text) {
      const toast = document.getElementById("toast");
      document.getElementById("toast-text").innerText = text;
      toast.style.display = "flex";
      setTimeout(() => { toast.style.display = "none"; }, 3500);
    }

    window.addEventListener("resize", () => {
      if (network) {
        network.redraw();
        network.fit();
      }
    });

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
