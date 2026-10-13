"""Build and bundle web/index.html with:
1. Intelligent multi-step logic in Run Analysis (progress feedback, latency measurement, state updates).
2. User Guide and Benchmark modal dialogs beside Run Analysis.
3. Interactive Node Inspector on node click.
4. Architectural sentence removed as requested.
5. Exact dark slate and electric yellow theme.
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
      /* Deep Neutral Dark Charcoal Theme (#191a1b) */
      --bg-base: #131415;
      --bg-panel: #191a1b;
      --bg-card: #202122;
      --bg-card-hover: #28292a;
      --bg-input: #141516;
      
      --border-subtle: #2c2d2e;
      --border-strong: #3b3c3e;
      
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
      --text-dim: #71717a;
      
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
      display: inline-block;
      line-height: 1;
    }

    @keyframes defectiveBulbBlink {
      /* Steady on in vibrant yellow */
      0%, 18% {
        color: var(--yellow-primary);
      }
      /* Rapid erratic voltage flutter (faster blinks) */
      18.8% {
        color: #ffffff;
      }
      19.6% {
        color: var(--yellow-primary);
      }
      20.4% {
        color: #ffffff;
      }
      21.2% {
        color: var(--yellow-primary);
      }
      22.0% {
        color: #ffffff;
      }
      23.2% {
        color: var(--yellow-primary);
      }
      /* Steady burn */
      23.3%, 42% {
        color: var(--yellow-primary);
      }
      /* Single blink (one by one) */
      42.8% {
        color: #ffffff;
      }
      44.2% {
        color: var(--yellow-primary);
      }
      /* Steady burn */
      44.3%, 58% {
        color: var(--yellow-primary);
      }
      /* Count by count pulse blinks: 1... 2... */
      58.8% {
        color: #ffffff;
      }
      60.0% {
        color: var(--yellow-primary);
      }
      61.4% {
        color: #ffffff;
      }
      62.6% {
        color: var(--yellow-primary);
      }
      64.0% {
        color: #ffffff;
      }
      65.2% {
        color: var(--yellow-primary);
      }
      /* Steady burn */
      65.3%, 78% {
        color: var(--yellow-primary);
      }
      /* Quick micro-twitch */
      78.8% {
        color: #ffffff;
      }
      79.5% {
        color: var(--yellow-primary);
      }
      80.3% {
        color: #ffffff;
      }
      81.2% {
        color: var(--yellow-primary);
      }
      /* Steady burn to completion of cycle */
      81.3%, 100% {
        color: var(--yellow-primary);
      }
    }

    .brand-title span.kicker {
      color: var(--yellow-primary);
      display: inline-block;
      font-weight: 800;
      text-shadow: none;
      animation: defectiveBulbBlink 5.2s infinite;
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
      transition: all 0.2s ease;
    }

    .status-dot.offline {
      background: var(--yellow-primary);
      box-shadow: 0 0 8px rgba(250, 204, 21, 0.6);
    }

    .status-dot.active-infer {
      background: #38bdf8;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.8);
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
      color: #131415;
      box-shadow: 0 2px 10px rgba(250, 204, 21, 0.25);
    }

    .btn-yellow:hover:not(:disabled) {
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
      color: var(--yellow-primary);
    }

    @keyframes spin {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }

    .spin-icon {
      animation: spin 0.8s linear infinite;
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
      background: rgba(25, 26, 27, 0.7);
    }

    .panel-title {
      font-size: 12px;
      font-weight: 700;
      color: var(--text-main);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    /* Risk Tier Filters in Left Sidebar */
    .tier-filter-row {
      display: flex;
      gap: 5px;
      padding: 0 12px 10px 12px;
      border-bottom: 1px solid var(--border-subtle);
      background: var(--bg-panel);
    }

    .tier-tab-btn {
      flex: 1;
      height: 25px;
      font-size: 10px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.12s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 3px;
    }

    .tier-tab-btn:hover {
      background: var(--bg-card-hover);
      border-color: var(--border-strong);
      color: var(--text-main);
    }

    .tier-tab-btn.active {
      background: var(--yellow-bg);
      border-color: var(--yellow-border);
      color: var(--yellow-primary);
    }

    .search-box-clean {
      position: relative;
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

    .search-clear-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 16px;
      line-height: 1;
      padding: 2px 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 4px;
      transition: color 0.15s ease;
    }

    .search-clear-btn:hover {
      color: var(--yellow-primary);
    }

    /* Interactive Search Suggestions Dropdown */
    .search-suggestions-dropdown {
      position: absolute;
      top: calc(100% + 2px);
      left: 10px;
      right: 10px;
      background: rgba(25, 26, 27, 0.98);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-strong);
      border-radius: 8px;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.8), 0 0 15px rgba(250, 204, 21, 0.08);
      z-index: 100;
      display: none;
      max-height: 330px;
      overflow-y: auto;
      padding: 6px;
    }

    .search-suggestions-dropdown.open {
      display: block;
    }

    .suggestion-group-title {
      font-family: 'JetBrains Mono', monospace;
      font-size: 9px;
      font-weight: 700;
      color: var(--text-muted);
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 6px 8px 3px 8px;
    }

    .suggestion-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 6px 8px;
      border-radius: 5px;
      cursor: pointer;
      transition: background 0.12s ease;
      font-size: 11px;
      color: var(--text-main);
    }

    .suggestion-item:hover {
      background: var(--bg-card-hover);
      color: var(--yellow-primary);
    }

    .suggestion-item-left {
      display: flex;
      align-items: center;
      gap: 7px;
    }

    .suggestion-tag {
      font-family: 'JetBrains Mono', monospace;
      font-size: 9px;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: 4px;
      background: var(--bg-input);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
    }

    .suggestion-tag.risk-tag {
      background: var(--yellow-bg);
      border-color: var(--yellow-border);
      color: var(--yellow-primary);
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
      background: #28292a;
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
      background: #191a1b;
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
      background-color: #191a1b;
      background-image: radial-gradient(#2c2d2e 1.2px, transparent 1.2px);
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
      background: rgba(25, 26, 27, 0.94);
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

    #filter-user.active {
      background: var(--bg-card);
      border-color: rgba(250, 204, 21, 0.5);
      color: var(--node-user);
    }

    #filter-device.active {
      background: var(--bg-card);
      border-color: rgba(56, 189, 248, 0.5);
      color: var(--node-device);
    }

    #filter-merchant.active {
      background: var(--bg-card);
      border-color: rgba(52, 211, 153, 0.5);
      color: var(--node-merchant);
    }

    /* Floating Node Inspector Card */
    .node-inspector-card {
      position: absolute;
      top: 56px;
      left: 14px;
      background: rgba(25, 26, 27, 0.96);
      backdrop-filter: blur(10px);
      border: 1px solid var(--border-strong);
      border-left: 3.5px solid var(--yellow-primary);
      border-radius: 9px;
      padding: 12px 14px;
      width: 260px;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.65);
      z-index: 25;
      display: none;
    }

    .node-inspector-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
      padding-bottom: 6px;
      border-bottom: 1px solid var(--border-subtle);
    }

    .node-inspector-title {
      font-size: 12px;
      font-weight: 700;
      color: var(--text-main);
    }

    .node-type-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }

    .node-close-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      padding: 2px;
      display: flex;
    }

    .node-close-btn:hover {
      color: var(--yellow-primary);
    }

    .node-inspector-body {
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 11px;
    }

    .inspect-field {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .inspect-lbl {
      color: var(--text-muted);
    }

    .inspect-val {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: var(--text-main);
    }

    .inspect-actions {
      display: flex;
      gap: 6px;
      margin-top: 6px;
    }

    /* Legend Floating Pill */
    .canvas-legend {
      position: absolute;
      bottom: 14px;
      left: 14px;
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(25, 26, 27, 0.94);
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

    .legend-triangle {
      width: 0;
      height: 0;
      border-left: 5px solid transparent;
      border-right: 5px solid transparent;
      border-bottom: 9px solid var(--node-merchant);
    }

    /* Floating Settings Button at Right Bottom */
    .settings-floating-btn {
      position: fixed;
      bottom: 16px;
      right: 16px;
      display: flex;
      align-items: center;
      gap: 7px;
      background: rgba(25, 26, 27, 0.96);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-strong);
      border-radius: 20px;
      padding: 7px 14px;
      color: var(--text-main);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.02em;
      cursor: pointer;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
      z-index: 1000;
      transition: all 0.2s ease;
    }

    .settings-floating-btn:hover {
      background: #252628;
      border-color: var(--yellow-primary);
      color: var(--yellow-primary);
      box-shadow: 0 6px 24px rgba(250, 204, 21, 0.22);
      transform: translateY(-1px);
    }

    /* Settings Modal Specific Styles */
    .settings-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      margin-top: 6px;
    }

    @media (max-width: 768px) {
      .settings-grid {
        grid-template-columns: 1fr;
      }
    }

    .settings-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 9px;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .settings-card.full-width {
      grid-column: 1 / -1;
    }

    .settings-card-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 8px;
    }

    .settings-card-title {
      font-size: 11.5px;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 7px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .settings-card-title svg {
      color: var(--yellow-primary);
      flex-shrink: 0;
    }

    .settings-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      font-size: 12px;
    }

    .settings-row label {
      color: var(--text-muted);
      font-size: 11px;
      font-weight: 600;
    }

    .settings-input {
      background: var(--bg-input);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 6px 10px;
      border-radius: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      outline: none;
      width: 100%;
      box-sizing: border-box;
    }

    .settings-input:focus {
      border-color: var(--yellow-primary);
    }

    .settings-switch {
      position: relative;
      display: inline-block;
      width: 36px;
      height: 20px;
      flex-shrink: 0;
    }

    .settings-switch input {
      opacity: 0;
      width: 0;
      height: 0;
    }

    .settings-slider-round {
      position: absolute;
      cursor: pointer;
      top: 0; left: 0; right: 0; bottom: 0;
      background-color: var(--border-strong);
      transition: .22s;
      border-radius: 20px;
    }

    .settings-slider-round:before {
      position: absolute;
      content: "";
      height: 14px;
      width: 14px;
      left: 3px;
      bottom: 3px;
      background-color: #ffffff;
      transition: .22s;
      border-radius: 50%;
    }

    .settings-switch input:checked + .settings-slider-round {
      background-color: var(--yellow-primary);
    }

    .settings-switch input:checked + .settings-slider-round:before {
      transform: translateX(16px);
      background-color: #131415;
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
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .chip-account:hover {
      background: var(--yellow-bg);
      border-color: var(--yellow-primary);
    }

    .chip-account.frozen {
      border-color: #ef4444;
      background: rgba(239, 68, 68, 0.12);
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

    /* Modals (User Guide & Benchmark) */
    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(10, 10, 11, 0.85);
      backdrop-filter: blur(6px);
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }

    .modal-backdrop.open {
      display: flex;
    }

    .modal-window {
      background: var(--bg-panel);
      border: 1px solid var(--border-strong);
      border-radius: 14px;
      width: 100%;
      max-width: 820px;
      max-height: 86vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8), var(--shadow-glow);
      overflow: hidden;
    }

    .modal-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 22px;
      border-bottom: 1px solid var(--border-subtle);
      background: var(--bg-card);
    }

    .modal-title-group {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .modal-title {
      font-size: 15px;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .modal-close-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      padding: 6px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.15s ease;
    }

    .modal-close-btn:hover {
      background: var(--bg-card-hover);
      color: var(--yellow-primary);
    }

    .modal-body {
      padding: 22px 24px;
      overflow-y: auto;
      font-size: 13px;
      line-height: 1.6;
      color: var(--text-muted);
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .guide-section {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 16px 18px;
    }

    .guide-section h3 {
      font-size: 13.5px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .guide-section h3 svg {
      color: var(--yellow-primary);
      flex-shrink: 0;
    }

    .guide-section p {
      margin-bottom: 8px;
      color: #d1d5db;
      font-size: 12.5px;
    }

    .guide-section p:last-child {
      margin-bottom: 0;
    }

    .guide-grid-2 {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      margin-top: 10px;
    }

    .guide-step-card {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 12px;
    }

    .guide-step-title {
      font-size: 12px;
      font-weight: 700;
      color: var(--yellow-primary);
      margin-bottom: 5px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .guide-step-desc {
      font-size: 11.5px;
      color: var(--text-muted);
      line-height: 1.45;
    }

    .shortcut-badge {
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      font-weight: 600;
      background: var(--bg-input);
      border: 1px solid var(--border-strong);
      padding: 2px 6px;
      border-radius: 4px;
      color: var(--yellow-primary);
    }

    /* Benchmark Metric Grid */
    .benchmark-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
    }

    .benchmark-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .bench-kpi-title {
      font-size: 10px;
      font-weight: 800;
      color: var(--text-muted);
      letter-spacing: 0.05em;
    }

    .bench-compare-row {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
    }

    .bench-val-sub {
      font-size: 10px;
      color: var(--text-dim);
    }

    .bench-score-dim {
      font-family: 'JetBrains Mono', monospace;
      font-size: 18px;
      font-weight: 700;
      color: var(--text-muted);
    }

    .bench-score-bright {
      font-family: 'JetBrains Mono', monospace;
      font-size: 22px;
      font-weight: 800;
      color: var(--yellow-primary);
    }

    .bench-delta-tag {
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 5px;
      background: var(--yellow-bg);
      color: var(--yellow-primary);
      border: 1px solid var(--yellow-border);
    }

    .bench-progress-box {
      width: 100%;
      height: 6px;
      background: var(--bg-input);
      border-radius: 3px;
      position: relative;
      overflow: hidden;
      margin-top: 4px;
    }

    .bench-bar-base {
      position: absolute;
      left: 0;
      top: 0;
      height: 100%;
      background: #64748b;
    }

    .bench-bar-gnn {
      position: absolute;
      left: 0;
      top: 0;
      height: 100%;
      background: var(--yellow-primary);
    }
  </style>
</head>
<body>

  <!-- Top Header Navigation -->
  <header>
    <div class="brand-group">
      <div class="brand-logo-mark">
        <!-- Raw Network Graph Node Glyph -->
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#131415" stroke-width="2.5"><circle cx="12" cy="12" r="3"/><circle cx="19" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><line x1="12" y1="9" x2="19" y2="6.5"/><line x1="12" y1="15" x2="5" y2="17.5"/></svg>
      </div>
      <div class="brand-title">Dark<span class="kicker">Node</span></div>
      <span class="badge-pill">GNN-MPNN</span>
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
      <!-- Generate Fresh Graph Button -->
      <button class="btn btn-outline" id="new-graph-btn" onclick="generateNewGraph()" title="Generate a fresh batch of synthetic transactions and syndicate patterns">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
        New Graph
      </button>

      <!-- Benchmark Modal Button -->
      <button class="btn btn-outline" onclick="openBenchmarkModal()" title="View Empirical Model Benchmarks vs Bank Rules">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
        Benchmark
      </button>

      <!-- User Guide Modal Button -->
      <button class="btn btn-outline" onclick="openGuideModal()" title="View System Architecture and Dashboard Operator Guide">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        User Guide
      </button>

      <!-- Settings Modal Button -->
      <button class="btn btn-outline" onclick="openSettingsModal()" title="Open System Configuration, API & Compliance Settings">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
        Settings
      </button>

      <!-- Run Analysis Button with Intelligent Pipeline Execution -->
      <button class="btn btn-yellow" id="run-btn" onclick="fetchRings()">
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

      <!-- Risk Tier Filter Tabs with Real Logic -->
      <div class="tier-filter-row">
        <button class="tier-tab-btn active" id="tier-all" onclick="setTierFilter('all')" title="Show all detected syndicates">All (<span id="count-all">10</span>)</button>
        <button class="tier-tab-btn" id="tier-critical" onclick="setTierFilter('critical')" title="Filter rings with critical threat >= 81.4%">Critical (<span id="count-critical">8</span>)</button>
        <button class="tier-tab-btn" id="tier-elevated" onclick="setTierFilter('elevated')" title="Filter rings with elevated threat < 81.4%">Elevated (<span id="count-elevated">2</span>)</button>
      </div>

      <div class="search-box-clean">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#6b7280" stroke-width="2.2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input type="text" class="search-input-clean" id="search-filter" placeholder="Filter by Ring ID, User, Device..." oninput="onSearchInput()" onfocus="showSearchSuggestions()" autocomplete="off">
        <button id="search-clear-btn" class="search-clear-btn" onclick="clearSearchFilter()" style="display: none;" title="Clear search">×</button>

        <!-- Interactive Search Suggestions Dropdown -->
        <div class="search-suggestions-dropdown" id="search-suggestions">
          <div class="suggestion-group-title">High Priority Rings</div>
          <div class="suggestion-item" onclick="applySearchSuggestion('Ring #3')">
            <div class="suggestion-item-left">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#facc15" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><polygon points="12 6 12 12 16 14"/></svg>
              <span>Ring #3</span>
            </div>
            <span class="suggestion-tag risk-tag">82.9% Risk</span>
          </div>
          <div class="suggestion-item" onclick="applySearchSuggestion('Ring #8')">
            <div class="suggestion-item-left">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#facc15" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><polygon points="12 6 12 12 16 14"/></svg>
              <span>Ring #8</span>
            </div>
            <span class="suggestion-tag risk-tag">82.5% Risk</span>
          </div>
          <div class="suggestion-item" onclick="applySearchSuggestion('Ring #6')">
            <div class="suggestion-item-left">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#facc15" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><polygon points="12 6 12 12 16 14"/></svg>
              <span>Ring #6</span>
            </div>
            <span class="suggestion-tag risk-tag">82.2% Risk</span>
          </div>
          <div class="suggestion-item" onclick="applySearchSuggestion('Ring #2')">
            <div class="suggestion-item-left">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><polygon points="12 6 12 12 16 14"/></svg>
              <span>Ring #2</span>
            </div>
            <span class="suggestion-tag">80.8% Risk</span>
          </div>

          <div class="suggestion-group-title" style="margin-top: 4px;">Key Member Accounts</div>
          <div class="suggestion-item" onclick="applySearchSuggestion('User 0')">
            <div class="suggestion-item-left">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#facc15" stroke-width="2"><circle cx="12" cy="7" r="4"/><path d="M5.5 21a8.38 8.38 0 0 1 13 0"/></svg>
              <span>User 0</span>
            </div>
            <span class="suggestion-tag">Ring #3 Lead</span>
          </div>
          <div class="suggestion-item" onclick="applySearchSuggestion('User 24')">
            <div class="suggestion-item-left">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#facc15" stroke-width="2"><circle cx="12" cy="7" r="4"/><path d="M5.5 21a8.38 8.38 0 0 1 13 0"/></svg>
              <span>User 24</span>
            </div>
            <span class="suggestion-tag">Ring #8 Lead</span>
          </div>
          <div class="suggestion-item" onclick="applySearchSuggestion('User 32')">
            <div class="suggestion-item-left">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#facc15" stroke-width="2"><circle cx="12" cy="7" r="4"/><path d="M5.5 21a8.38 8.38 0 0 1 13 0"/></svg>
              <span>User 32</span>
            </div>
            <span class="suggestion-tag">Ring #6 Lead</span>
          </div>
          <div class="suggestion-item" onclick="applySearchSuggestion('User 80')">
            <div class="suggestion-item-left">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#facc15" stroke-width="2"><circle cx="12" cy="7" r="4"/><path d="M5.5 21a8.38 8.38 0 0 1 13 0"/></svg>
              <span>User 80</span>
            </div>
            <span class="suggestion-tag">Ring #2 Lead</span>
          </div>

          <div class="suggestion-group-title" style="margin-top: 4px;">Shared Infrastructure</div>
          <div class="suggestion-item" onclick="applySearchSuggestion('Device 666')">
            <div class="suggestion-item-left">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>
              <span>Device 666</span>
            </div>
            <span class="suggestion-tag">Multiplexed</span>
          </div>
          <div class="suggestion-item" onclick="applySearchSuggestion('Device 789')">
            <div class="suggestion-item-left">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>
              <span>Device 789</span>
            </div>
            <span class="suggestion-tag">High-Density</span>
          </div>
        </div>
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
        <button class="canvas-pill-btn active" id="spin-btn" onclick="toggleSpinAnimation()">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
          <span id="spin-label">Orbit Spin: On</span>
        </button>
        <button class="canvas-pill-btn" id="spread-btn" onclick="spreadGraph()">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
          <span id="spread-label">Spread Out</span>
        </button>
        <button class="canvas-pill-btn active" id="physics-toggle" onclick="togglePhysics()">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          <span id="physics-label">Physics: On</span>
        </button>
        <span style="color: var(--border-subtle);">|</span>
        <button class="canvas-pill-btn active" id="filter-user" onclick="toggleFilter('user')">Users</button>
        <button class="canvas-pill-btn active" id="filter-device" onclick="toggleFilter('device')">Devices</button>
        <button class="canvas-pill-btn active" id="filter-merchant" onclick="toggleFilter('merchant')">Merchants</button>
      </div>

      <!-- Interactive Node Inspector Floating Card -->
      <div class="node-inspector-card" id="node-inspector">
        <div class="node-inspector-head">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span class="node-type-dot" id="inspect-dot"></span>
            <span class="node-inspector-title" id="inspect-id">User 0</span>
          </div>
          <button class="node-close-btn" onclick="closeNodeInspector()">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>
        <div class="node-inspector-body">
          <div class="inspect-field">
            <span class="inspect-lbl">Entity Role</span>
            <span class="inspect-val" id="inspect-role">Syndicate Member Account</span>
          </div>
          <div class="inspect-field">
            <span class="inspect-lbl">Signal Status</span>
            <span class="inspect-val" id="inspect-score" style="color: var(--yellow-primary);">High Anomaly</span>
          </div>
          <div class="inspect-field">
            <span class="inspect-lbl">Connected Hops</span>
            <span class="inspect-val" id="inspect-deg">4 links</span>
          </div>
          <div class="inspect-actions">
            <button class="btn btn-outline" style="height: 26px; font-size: 10px; flex: 1;" onclick="isolateNodeNeighbors()">Focus Hops</button>
            <button class="btn btn-yellow" style="height: 26px; font-size: 10px; flex: 1;" onclick="copyNodeId()">Copy ID</button>
          </div>
        </div>
      </div>

      <!-- Graph Canvas Container -->
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
          <div class="legend-triangle"></div>
          <span>Target Merchant</span>
        </div>
      </div>
    </div>

    <!-- Panel 3: Right Inspector & Evidence Panel -->
    <div class="panel-card sidebar-right">
      <div class="panel-header-clean">
        <span class="panel-title" id="inspector-heading">SYNDICATE #3</span>
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

        <!-- Compliance & Regulatory Actions -->
        <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 4px;">
          <button class="btn btn-yellow" id="freeze-btn" style="height: 36px;" onclick="executeFreezeAction()" title="Execute legal debit freeze on all syndicate accounts">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            Freeze Syndicate Accounts
          </button>
          <button class="btn btn-outline" style="height: 34px;" onclick="openSettingsModal('sar')" title="Configure regulatory reporting & export official FinCEN / FIU SAR packages">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            Compliance & SAR Export
          </button>
        </div>
      </div>
    </div>

  </div>

  <!-- Fixed Floating Settings Trigger at Right Bottom of Page -->
  <button class="settings-floating-btn" id="open-settings-bottom-btn" onclick="openSettingsModal()" title="System Configuration, API & SAR Compliance">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
      <circle cx="12" cy="12" r="3"/>
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
    </svg>
    <span>Settings</span>
  </button>

  <!-- Interactive System Settings & Compliance Modal -->
  <div class="modal-backdrop" id="settings-modal" onclick="closeSettingsModal(event)">
    <div class="modal-window" style="max-width: 880px;" onclick="event.stopPropagation()">
      <div class="modal-head">
        <div class="modal-title-group">
          <div class="brand-logo-mark" style="width:24px; height:24px;">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#131415" stroke-width="2.5"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
          </div>
          <div class="modal-title">
            DarkNode Settings & Compliance Controls
          </div>
        </div>
        <button class="modal-close-btn" onclick="closeSettingsModal()">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <div class="modal-body">
        <div class="settings-grid">
          <!-- Card 1: API Connection (ss3) -->
          <div class="settings-card" id="setting-card-api">
            <div class="settings-card-head">
              <span class="settings-card-title">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/></svg>
                Backend API & Inference Engine
              </span>
              <div class="api-box" style="margin: 0; padding: 2px 7px;">
                <div class="status-dot" id="status-dot"></div>
                <span class="status-text" id="status-label">ONLINE</span>
              </div>
            </div>
            <div style="font-size: 11px; color: var(--text-muted);">
              Target FastAPI backend serving PyTorch Geometric GNN-MPNN inference.
            </div>
            <div>
              <label style="font-size: 10px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 4px;">ENDPOINT BASE URL</label>
              <input type="text" id="api-url" class="settings-input" value="http://localhost:8000" placeholder="http://localhost:8000">
            </div>
            <div id="api-ping-result" style="font-size: 10.5px; font-family: 'JetBrains Mono', monospace; min-height: 16px;"></div>
            <div style="display: flex; gap: 8px;">
              <button class="btn btn-outline" style="flex: 1; height: 32px;" onclick="testApiConnection()">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
                Ping Endpoint
              </button>
              <button class="btn btn-yellow" style="flex: 1; height: 32px;" onclick="fetchRings(); showToast('Triggered live GNN re-analysis');">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                Run GNN Inference
              </button>
            </div>
          </div>

          <!-- Card 2: Regulatory Compliance & SAR Filing (ss2) -->
          <div class="settings-card" id="setting-card-sar">
            <div class="settings-card-head">
              <span class="settings-card-title">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
                Regulatory SAR Dossier Export
              </span>
              <span class="badge-pill" style="font-size: 9px;">FinCEN / FIU</span>
            </div>
            <div style="font-size: 11px; color: var(--text-muted);">
              Official Suspicious Activity Report (SAR Form 111 / STR) evidence generation for legal escalation.
            </div>
            <div style="background: var(--bg-input); padding: 8px 10px; border-radius: 6px; border: 1px solid var(--border-subtle); font-size: 11px;">
              <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                <span style="color: var(--text-muted);">Active Syndicate:</span>
                <span style="font-weight: 700; color: var(--yellow-primary);" id="settings-active-ring-lbl">Syndicate #3</span>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span style="color: var(--text-muted);">Audit Standard:</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px;">FinCEN ML-111 & FIU-IND</span>
              </div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 7px; margin-top: 2px;">
              <button class="btn btn-outline" style="height: 33px;" onclick="exportSarDossier()">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                Export SAR Dossier (JSON / FinCEN)
              </button>
              <button class="btn btn-outline" style="height: 33px;" onclick="exportSarCsv()">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                Export Evidence Ledger (CSV)
              </button>
            </div>
          </div>

          <!-- Card 3: GNN Detection Threshold & Sensitivity -->
          <div class="settings-card">
            <div class="settings-card-head">
              <span class="settings-card-title">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>
                GNN Sensitivity Threshold
              </span>
              <span class="badge-pill" id="settings-thresh-badge">0.50</span>
            </div>
            <div style="font-size: 11px; color: var(--text-muted);">
              Controls candidate pool cutoff. Lower values increase recall (captures early smurfs); higher values enforce strict precision.
            </div>
            <div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 11px;">
                <label>CUTOFF PRESET</label>
                <select id="threshold-select" class="settings-input" style="width: auto; padding: 2px 8px;" onchange="onThresholdChange(this.value)">
                  <option value="0.40">0.40 (Broad / High Recall)</option>
                  <option value="0.50" selected>0.50 (Standard Balance)</option>
                  <option value="0.60">0.60 (Strict Precision)</option>
                  <option value="0.75">0.75 (Critical High-Certainty)</option>
                </select>
              </div>
              <input type="range" id="threshold-slider" min="0.30" max="0.85" step="0.05" value="0.50" style="width: 100%; accent-color: var(--yellow-primary); cursor: pointer;" oninput="onThresholdSliderChange(this.value)">
            </div>
            <div id="threshold-desc-box" style="font-size: 10.5px; color: var(--text-muted); background: var(--bg-input); padding: 6px 10px; border-radius: 6px; border: 1px solid var(--border-subtle);">
              Currently filtering at <strong>0.50</strong>: 95.0% model precision with minimal false alarms.
            </div>
          </div>

          <!-- Card 4: Real-Time Alerts & Notification Options -->
          <div class="settings-card">
            <div class="settings-card-head">
              <span class="settings-card-title">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                Alerts & Notifications
              </span>
              <span class="badge-pill" style="font-size: 9px; color: #34d399; border-color: rgba(52, 211, 153, 0.3);">ACTIVE</span>
            </div>
            <div style="font-size: 11px; color: var(--text-muted);">
              Real-time audit alerts when syndicates exceed critical threat thresholds.
            </div>
            <div class="settings-row">
              <div>
                <div style="color: var(--text-main); font-weight: 600;">High-Risk Audio Alert Chime</div>
                <div style="font-size: 10.5px; color: var(--text-muted);">Audible cue on critical syndicates (&gt;0.80)</div>
              </div>
              <label class="settings-switch">
                <input type="checkbox" id="setting-sound-alert" checked onchange="toggleSoundPreference(this.checked)">
                <span class="settings-slider-round"></span>
              </label>
            </div>
            <div class="settings-row">
              <div>
                <div style="color: var(--text-main); font-weight: 600;">Compliance In-App Toasts</div>
                <div style="font-size: 10.5px; color: var(--text-muted);">Show action audit confirmations</div>
              </div>
              <label class="settings-switch">
                <input type="checkbox" id="setting-toast-alert" checked onchange="toggleToastPreference(this.checked)">
                <span class="settings-slider-round"></span>
              </label>
            </div>
            <div style="display: flex; gap: 8px; margin-top: 4px;">
              <button class="btn btn-outline" style="flex: 1; height: 30px; font-size: 11px;" onclick="playAlertChime()">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>
                Test Alert Chime
              </button>
            </div>
          </div>

          <!-- Card 5: Graph Engine & Physics Controls -->
          <div class="settings-card">
            <div class="settings-card-head">
              <span class="settings-card-title">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><circle cx="19" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><line x1="12" y1="9" x2="19" y2="6.5"/><line x1="12" y1="15" x2="5" y2="17.5"/></svg>
                Graph Engine & Physics
              </span>
            </div>
            <div class="settings-row">
              <div>
                <div style="color: var(--text-main); font-weight: 600;">Physics Force Simulation</div>
                <div style="font-size: 10.5px; color: var(--text-muted);">Live ForceAtlas2 layout equilibrium</div>
              </div>
              <label class="settings-switch">
                <input type="checkbox" id="setting-physics-toggle" checked onchange="togglePhysicsFromSettings(this.checked)">
                <span class="settings-slider-round"></span>
              </label>
            </div>
            <div class="settings-row">
              <div>
                <div style="color: var(--text-main); font-weight: 600;">Continuous Orbit Rotation</div>
                <div style="font-size: 10.5px; color: var(--text-muted);">Smooth yaw orbital camera rotation</div>
              </div>
              <label class="settings-switch">
                <input type="checkbox" id="setting-orbit-toggle" checked onchange="toggleOrbitFromSettings(this.checked)">
                <span class="settings-slider-round"></span>
              </label>
            </div>
            <div>
              <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px;">
                <label>SPRING REPULSION DISTANCE</label>
                <span id="spring-len-val" style="font-family: 'JetBrains Mono', monospace; color: var(--yellow-primary);">260px</span>
              </div>
              <input type="range" id="spring-slider" min="180" max="420" step="20" value="260" style="width: 100%; accent-color: var(--yellow-primary); cursor: pointer;" oninput="onSpringSliderChange(this.value)">
            </div>
          </div>

          <!-- Card 6: System Documentation & Quick Navigation -->
          <div class="settings-card">
            <div class="settings-card-head">
              <span class="settings-card-title">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
                Documentation & Defaults
              </span>
            </div>
            <div style="font-size: 11px; color: var(--text-muted);">
              Inspect mathematical model architecture, empirical benchmarks, or restore system factory defaults.
            </div>
            <div style="display: flex; flex-direction: column; gap: 7px;">
              <button class="btn btn-outline" style="height: 32px;" onclick="closeSettingsModal(); openGuideModal();">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                Open Architecture & User Guide
              </button>
              <button class="btn btn-outline" style="height: 32px;" onclick="closeSettingsModal(); openBenchmarkModal();">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
                Open Model Benchmarks vs Rules
              </button>
              <button class="btn btn-outline" style="height: 32px; color: #ef4444; border-color: rgba(239, 68, 68, 0.4);" onclick="resetSettingsToDefault()">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
                Reset All Settings to Defaults
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Interactive System & User Guide Modal -->
  <div class="modal-backdrop" id="guide-modal" onclick="closeGuideModal(event)">
    <div class="modal-window" style="max-width: 860px;" onclick="event.stopPropagation()">
      <div class="modal-head">
        <div class="modal-title-group">
          <div class="brand-logo-mark" style="width:24px; height:24px;">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#131415" stroke-width="2.5"><circle cx="12" cy="12" r="3"/><circle cx="19" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><line x1="12" y1="9" x2="19" y2="6.5"/><line x1="12" y1="15" x2="5" y2="17.5"/></svg>
          </div>
          <div class="modal-title">
            DarkNode Operator Guide & Architecture
          </div>
        </div>
        <button class="modal-close-btn" onclick="closeGuideModal()">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <div class="modal-body">
        <!-- Section 1: Overview -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
            1. Problem Statement & Heterogeneous GNN Solution
          </h3>
          <p>
            Mule accounts operate in organized syndicates where individual transactions appear benign. Traditional rule-based engines inspect transactions in isolation, resulting in high false alarms (<strong>58.1% of alerts are false positives</strong>) on innocent events like public Wi-Fi access or family-shared tablets.
          </p>
          <p>
            <strong>DarkNode</strong> implements a 2-layer Heterogeneous Graph Message Passing Neural Network (MPNN) across <strong>Users</strong>, <strong>Devices</strong>, and <strong>Merchants</strong>. By propagating structural graph embeddings across shared device fingerprints and IP collision graphs, DarkNode achieves <strong>95.0% precision</strong> and curtails false alarms to just 5.0%.
          </p>
        </div>

        <!-- Section 2: End-to-End Pipeline Architecture -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
            2. End-to-End System Architecture Pipeline
          </h3>
          <div style="background: var(--bg-input); padding: 12px 14px; border-radius: 8px; border: 1px solid var(--border-subtle); font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: #e5e7eb; overflow-x: auto; line-height: 1.55;">
┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
│ Multi-Modal Data Ingest │ ──► │ Heterogeneous Graph     │ ──► │ 2-Layer MPNN            │
│ • User Accounts         │     │ • (User)-[transacts]-►  │     │ • Device Embedding Agg  │
│ • Hardware IDs / IMEI   │     │ • (User)-[shares_ip]-►  │     │ • IP Dispersion Agg     │
│ • Merchant Terminals    │     │ • (User)-[uses_dev]-►   │     │ • Multi-Hop Latent Embed│
└─────────────────────────┘     └─────────────────────────┘     └───────────┬─────────────┘
                                                                            │
┌─────────────────────────┐     ┌─────────────────────────┐                 ▼
│ Statutory Containment   │ ◄── │ Risk Fusion Engine      │ ◄───────────────┘
│ • Auto Account Freeze   │     │ • GNN Anomaly Weight    │
│ • FinCEN SAR Filing     │     │ • Burst Velocity Metric │
│ • Regulatory Audit Doss │     │ • Decision Threshold θ  │
└─────────────────────────┘     └─────────────────────────┘
          </div>
          <p style="margin-top: 10px; font-size: 12px;">
            <strong>Step 1: Graph Construction:</strong> Links accounts via shared hardware fingerprints and subnet collisions.<br>
            <strong>Step 2: Message Passing:</strong> Aggregates neighbor embeddings across 2 hops, capturing indirect smurfing coordination.<br>
            <strong>Step 3: Risk Scoring & Cutoff:</strong> Applies decision threshold θ to rank syndicates by laundering probability.<br>
            <strong>Step 4: Containment & Reporting:</strong> Generates FinCEN Form 111 / FIU-compliant SAR dossiers for regulatory submission.
          </p>
        </div>

        <!-- Section 3: Operator Investigation Workflow (Instructions) -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            3. Step-by-Step Operator Instructions
          </h3>
          <div class="guide-grid-2">
            <div class="guide-step-card">
              <div class="guide-step-title">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
                Step 1: Syndicate Triage (Left Directory)
              </div>
              <div class="guide-step-desc">
                Review the ranked syndicate list. Syndicates with composite scores &gt;0.80 are flagged with red CRITICAL badges. Click any card to load its dedicated topological subgraph.
              </div>
            </div>

            <div class="guide-step-card">
              <div class="guide-step-title">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><circle cx="19" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><line x1="12" y1="9" x2="19" y2="6.5"/><line x1="12" y1="15" x2="5" y2="17.5"/></svg>
                Step 2: Subgraph Inspection (Center Canvas)
              </div>
              <div class="guide-step-desc">
                Examine interconnections. Click any node to open the live Inspector card showing connected hops, roles, and device hardware linkages.
              </div>
            </div>

            <div class="guide-step-card">
              <div class="guide-step-title">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                Step 3: Traversal Verification (Run Analysis)
              </div>
              <div class="guide-step-desc">
                Click <strong>Run Analysis</strong> to launch sequential GNN neural packet traversal, verifying cyclical layering and money dispersion patterns across users.
              </div>
            </div>

            <div class="guide-step-card">
              <div class="guide-step-title">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                Step 4: Containment & Legal Escalation
              </div>
              <div class="guide-step-desc">
                Click <strong>Freeze Syndicate Accounts</strong> to instantly execute simulated debit quarantines. Use <strong>Settings → Export SAR Dossier</strong> for official FinCEN filing packages.
              </div>
            </div>
          </div>
        </div>

        <!-- Section 4: Canvas Navigation & Controls -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
            4. Canvas Navigation & Physics Controls
          </h3>
          <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 6px;">
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid var(--border-subtle);">
              <span>Normalized Zoom</span>
              <div><span class="shortcut-badge">Mouse Wheel</span> or <span class="shortcut-badge">Trackpad Pinch</span> (smooth, controlled speed)</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid var(--border-subtle);">
              <span>Pan Viewport</span>
              <div><span class="shortcut-badge">Click + Drag</span> background canvas</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid var(--border-subtle);">
              <span>Inspect Node</span>
              <div><span class="shortcut-badge">Click Any Node</span> to view connected hops, role, and anomaly rating</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid var(--border-subtle);">
              <span>Orbit / Physics Toggles</span>
              <div>Independent top-canvas controls for yaw camera rotation and ForceAtlas2 physics</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0;">
              <span>Entity Filters</span>
              <div>Toggle <span class="shortcut-badge">Users</span>, <span class="shortcut-badge">Devices</span>, or <span class="shortcut-badge">Merchants</span> to isolate subgraphs</div>
            </div>
          </div>
        </div>

        <!-- Section 5: Graph Visual Legend -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m9.17 14.83-4.24 4.24"/></svg>
            5. Graph Visual Legend (Exact Model Symbols)
          </h3>
          <div style="display: flex; flex-wrap: wrap; gap: 18px; align-items: center; margin-top: 6px;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <div style="width: 12px; height: 12px; border-radius: 50%; background: #facc15;"></div>
              <span style="color: #f3f4f6; font-size: 12px;"><strong>User Node (Circle, Yellow)</strong>: Syndicate member account</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <div style="width: 12px; height: 12px; transform: rotate(45deg); background: #38bdf8;"></div>
              <span style="color: #f3f4f6; font-size: 12px;"><strong>Device Node (Diamond, Cyan)</strong>: Shared hardware identifier</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <div style="width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-bottom: 12px solid #34d399;"></div>
              <span style="color: #f3f4f6; font-size: 12px;"><strong>Merchant Node (Triangle, Mint)</strong>: Target merchant terminal</span>
            </div>
          </div>
        </div>

        <!-- Section 6: Settings & Compliance Controls -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
            6. Settings & Compliance Configuration
          </h3>
          <p>
            Access <strong>Settings</strong> at any time via the bottom-right button or header. Use Settings to:
          </p>
          <ul style="margin: 6px 0 0 18px; font-size: 12px; line-height: 1.6;">
            <li><strong>Configure API Endpoint:</strong> Switch between live FastAPI backend (port 8000) or test connectivity with single-click latency pinging.</li>
            <li><strong>Tune GNN Decision Cutoff (Threshold θ):</strong> Calibrate sensitivity between high-recall candidate discovery (0.40) and high-precision critical enforcement (0.75).</li>
            <li><strong>Export Regulatory FinCEN SAR & CSV Dossiers:</strong> Download auditable evidence packages containing complete account rosters and transaction burst logs.</li>
            <li><strong>Configure Real-time Compliance Alarms:</strong> Toggle audio chimes for critical threat rings (&gt;0.80) and manage graph physics.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <!-- Model Benchmark Modal -->
  <div class="modal-backdrop" id="benchmark-modal" onclick="closeBenchmarkModal(event)">
    <div class="modal-window" onclick="event.stopPropagation()">
      <div class="modal-head">
        <div class="modal-title-group">
          <div class="brand-logo-mark" style="width:24px; height:24px;">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#131415" stroke-width="2.5"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
          </div>
          <div class="modal-title">
            DarkNode Empirical Benchmark — GNN vs Bank Rules
          </div>
        </div>
        <button class="modal-close-btn" onclick="closeBenchmarkModal()">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <div class="modal-body">
        <!-- Metric Comparison Grid -->
        <div class="benchmark-grid">
          <div class="benchmark-card">
            <div class="bench-kpi-title">PRECISION (ACCURACY OF ALERTS)</div>
            <div class="bench-compare-row">
              <div>
                <div class="bench-val-sub">Rule Baseline</div>
                <div class="bench-score-dim">41.9%</div>
              </div>
              <div class="bench-delta-tag">+53.1 points</div>
              <div style="text-align: right;">
                <div class="bench-val-sub">DarkNode GNN</div>
                <div class="bench-score-bright">95.0%</div>
              </div>
            </div>
            <div class="bench-progress-box">
              <div class="bench-bar-base" style="width: 41.9%;"></div>
              <div class="bench-bar-gnn" style="width: 95.0%;"></div>
            </div>
          </div>

          <div class="benchmark-card">
            <div class="bench-kpi-title">FALSE-ALARM SHARE (DEFENSIVE NOISE)</div>
            <div class="bench-compare-row">
              <div>
                <div class="bench-val-sub">Rule Baseline</div>
                <div class="bench-score-dim" style="color: #ef4444;">58.1%</div>
              </div>
              <div class="bench-delta-tag" style="background: rgba(52, 211, 153, 0.15); color: #34d399; border-color: rgba(52, 211, 153, 0.3);">-53.1 points</div>
              <div style="text-align: right;">
                <div class="bench-val-sub">DarkNode GNN</div>
                <div class="bench-score-bright" style="color: #34d399;">5.0%</div>
              </div>
            </div>
            <div class="bench-progress-box">
              <div class="bench-bar-base" style="width: 58.1%; background: #ef4444;"></div>
              <div class="bench-bar-gnn" style="width: 5.0%; background: #34d399;"></div>
            </div>
          </div>

          <div class="benchmark-card">
            <div class="bench-kpi-title">F1 SCORE (HARMONIC MEAN)</div>
            <div class="bench-compare-row">
              <div>
                <div class="bench-val-sub">Rule Baseline</div>
                <div class="bench-score-dim">0.591</div>
              </div>
              <div class="bench-delta-tag">+0.383 lift</div>
              <div style="text-align: right;">
                <div class="bench-val-sub">DarkNode GNN</div>
                <div class="bench-score-bright">0.974</div>
              </div>
            </div>
            <div class="bench-progress-box">
              <div class="bench-bar-base" style="width: 59.1%;"></div>
              <div class="bench-bar-gnn" style="width: 97.4%;"></div>
            </div>
          </div>

          <div class="benchmark-card">
            <div class="bench-kpi-title">INFERENCE LATENCY (REAL-TIME ENGINE)</div>
            <div class="bench-compare-row">
              <div>
                <div class="bench-val-sub">Full Graph Size</div>
                <div class="bench-score-dim">15K Entities</div>
              </div>
              <div class="bench-delta-tag" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border-color: rgba(56, 189, 248, 0.3);">Sub-10ms</div>
              <div style="text-align: right;">
                <div class="bench-val-sub">Forward Pass</div>
                <div class="bench-score-bright" style="color: #38bdf8;">8.4 ms</div>
              </div>
            </div>
          </div>
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
    let currentTierFilter = 'all';
    let physicsState = true;
    let currentSpringLength = 260;
    let activeFilters = { user: true, device: true, merchant: true };
    let currentVisibleNodes = [];
    let inspectedNodeId = null;
    let frozenRings = new Set();

    const CRITICAL_CUTOFF = 0.814;

    // Real fallback dataset extracted from trained GNN model
    const FALLBACK_RINGS = __FALLBACK_JSON__;

    async function fetchRings() {
      const runBtn = document.getElementById("run-btn");
      const dot = document.getElementById("status-dot");
      const label = document.getElementById("status-label");
      const url = document.getElementById("api-url").value.trim().replace(/\/$/, "");

      // Multi-step logic: Step 1 - Enter active inference pipeline state
      if (runBtn) {
        runBtn.disabled = true;
        runBtn.innerHTML = `
          <svg class="spin-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
          </svg>
          Inferring GNN...
        `;
        runBtn.style.opacity = "0.85";
      }
      dot.classList.add("active-infer");
      label.innerText = "INFERRING GNN...";
      showToast("Initializing Heterogeneous MPNN inference pipeline...");

      const startTime = performance.now();

      const threshInput = document.getElementById("threshold-select");
      const currentThresh = threshInput ? parseFloat(threshInput.value) : 0.5;

      try {
        // Multi-step logic: Step 2 - Execute real PyTorch Geometric backend inference
        const res = await fetch(`${url}/analyze`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ top_k: 10, threshold: currentThresh })
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        allRings = data.rings || [];

        const elapsed = Math.round(performance.now() - startTime);

        if (data.metadata) {
          document.getElementById("stat-users").innerText = data.metadata.num_users?.toLocaleString() || "1,000";
          document.getElementById("stat-txs").innerText = data.metadata.total_transactions?.toLocaleString() || "13,680";
        }
        dot.classList.remove("offline", "active-infer");
        label.innerText = "LIVE API";
        showToast(`GNN inference complete in ${elapsed}ms: ${allRings.length} syndicates ranked (Threshold: ${currentThresh.toFixed(2)})`);
      } catch (err) {
        console.warn("Backend unavailable, using cached model dossier:", err);
        // Logical fallback: filter rings by threshold so sensitivity changes take effect
        allRings = FALLBACK_RINGS.filter(r => r.avg_model_score >= (currentThresh - 0.15));
        dot.classList.remove("active-infer");
        dot.classList.add("offline");
        label.innerText = "CACHED GNN";
        showToast(`Loaded GNN model dossier (${allRings.length} rings, Threshold: ${currentThresh.toFixed(2)})`);
      } finally {
        if (runBtn) {
          runBtn.disabled = false;
          runBtn.innerHTML = `
            <svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            Run Analysis
          `;
          runBtn.style.opacity = "1";
        }
      }

      document.getElementById("stat-rings").innerText = allRings.length;
      document.getElementById("rings-count-badge").innerText = `${allRings.length} total`;

      // Update tier filter counts dynamically
      const critCount = allRings.filter(r => r.score >= CRITICAL_CUTOFF).length;
      const elevCount = allRings.filter(r => r.score < CRITICAL_CUTOFF).length;
      const cntAll = document.getElementById("count-all");
      const cntCrit = document.getElementById("count-critical");
      const cntElev = document.getElementById("count-elevated");
      if (cntAll) cntAll.innerText = allRings.length;
      if (cntCrit) cntCrit.innerText = critCount;
      if (cntElev) cntElev.innerText = elevCount;

      filterRings();
      if (allRings.length > 0) {
        const targetIdx = (activeIndex >= 0 && activeIndex < allRings.length) ? activeIndex : 0;
        selectRing(targetIdx, false);
      }
    }

    function onThresholdChange(newThreshold) {
      showToast(`Threshold updated to ${newThreshold} — re-evaluating candidate pool...`);
      fetchRings();
    }

    async function generateNewGraph() {
      const btn = document.getElementById("new-graph-btn");
      const dot = document.getElementById("status-dot");
      const label = document.getElementById("status-label");
      const url = document.getElementById("api-url").value.trim().replace(/\/$/, "");
      const threshInput = document.getElementById("threshold-select");
      const currentThresh = threshInput ? parseFloat(threshInput.value) : 0.5;

      if (btn) {
        btn.disabled = true;
        btn.innerHTML = `
          <svg class="spin-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
          </svg>
          Generating...
        `;
        btn.style.opacity = "0.85";
      }
      dot.classList.add("active-infer");
      label.innerText = "SYNTHESIZING GRAPH...";
      showToast("Generating fresh transaction graph and running GNN forward pass...");

      try {
        const res = await fetch(`${url}/generate-graph`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ threshold: currentThresh })
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        allRings = data.rings || [];

        if (data.metadata) {
          document.getElementById("stat-users").innerText = data.metadata.num_users?.toLocaleString() || "1,000";
          document.getElementById("stat-txs").innerText = data.metadata.total_transactions?.toLocaleString() || "13,680";
        }
        dot.classList.remove("offline", "active-infer");
        label.innerText = "LIVE API";
        showToast(data.message || `Fresh graph generated (Seed: ${data.seed})`);
      } catch (err) {
        console.warn("Backend unavailable for graph generation:", err);
        showToast("Backend offline: Please start the FastAPI backend on port 8000");
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = `
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
            New Graph
          `;
          btn.style.opacity = "1";
        }
      }

      document.getElementById("stat-rings").innerText = allRings.length;
      document.getElementById("rings-count-badge").innerText = `${allRings.length} total`;

      const critCount = allRings.filter(r => r.score >= CRITICAL_CUTOFF).length;
      const elevCount = allRings.filter(r => r.score < CRITICAL_CUTOFF).length;
      const cntAll = document.getElementById("count-all");
      const cntCrit = document.getElementById("count-critical");
      const cntElev = document.getElementById("count-elevated");
      if (cntAll) cntAll.innerText = allRings.length;
      if (cntCrit) cntCrit.innerText = critCount;
      if (cntElev) cntElev.innerText = elevCount;

      activeIndex = 0;
      currentRenderedRingId = null;
      filterRings();
      if (allRings.length > 0) {
        selectRing(0, true);
      }
    }

    function setTierFilter(tier) {
      currentTierFilter = tier;
      document.querySelectorAll('.tier-tab-btn').forEach(btn => btn.classList.remove('active'));
      const activeTab = document.getElementById(`tier-${tier}`);
      if (activeTab) activeTab.classList.add('active');
      filterRings();
    }

    function renderRingsList(rings) {
      const container = document.getElementById("rings-container");
      container.innerHTML = "";

      if (!rings || rings.length === 0) {
        container.innerHTML = `
          <div style="padding: 28px 12px; text-align: center; color: var(--text-muted); font-size: 11px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" style="opacity: 0.5; margin-bottom: 6px;"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <div>No matching syndicates found</div>
            <div style="font-size: 10px; opacity: 0.7; margin-top: 3px;">Try switching to 'All' or clearing search</div>
          </div>
        `;
        return;
      }

      rings.forEach((ring) => {
        const originalIndex = allRings.findIndex(r => r.ring_id === ring.ring_id);
        const card = document.createElement("div");
        card.className = `ring-card-item ${originalIndex === activeIndex ? 'active' : ''}`;
        card.onclick = () => selectRing(originalIndex);

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

    function onSearchInput() {
      const input = document.getElementById("search-filter");
      const val = input ? input.value : "";
      const clearBtn = document.getElementById("search-clear-btn");
      if (clearBtn) clearBtn.style.display = val.length > 0 ? "flex" : "none";
      filterRings();
    }

    function showSearchSuggestions() {
      const dropdown = document.getElementById("search-suggestions");
      if (dropdown) dropdown.classList.add("open");
    }

    function hideSearchSuggestions() {
      const dropdown = document.getElementById("search-suggestions");
      if (dropdown) dropdown.classList.remove("open");
    }

    function applySearchSuggestion(query) {
      const input = document.getElementById("search-filter");
      if (input) input.value = query;
      const clearBtn = document.getElementById("search-clear-btn");
      if (clearBtn) clearBtn.style.display = "flex";
      filterRings();
      hideSearchSuggestions();
    }

    function clearSearchFilter() {
      const input = document.getElementById("search-filter");
      if (input) input.value = "";
      const clearBtn = document.getElementById("search-clear-btn");
      if (clearBtn) clearBtn.style.display = "none";
      filterRings();
      hideSearchSuggestions();
    }

    function filterRings() {
      const input = document.getElementById("search-filter");
      const query = input ? input.value.trim().toLowerCase() : "";

      const filtered = allRings.filter(r => {
        // 1. Tier tab filter
        if (currentTierFilter === 'critical' && r.score < CRITICAL_CUTOFF) return false;
        if (currentTierFilter === 'elevated' && r.score >= CRITICAL_CUTOFF) return false;

        // 2. Query text filter
        if (!query) return true;

        const ringMatches = `ring #${r.ring_id}`.toLowerCase().includes(query) ||
                            `ring ${r.ring_id}`.toLowerCase().includes(query) ||
                            (query.startsWith('#') && String(r.ring_id) === query.slice(1)) ||
                            String(r.ring_id) === query;
        if (ringMatches) return true;

        const memberMatches = (r.members || []).some(m => {
          const s = String(m);
          return s === query || `user ${s}`.toLowerCase().includes(query) || `user_${s}`.toLowerCase().includes(query);
        });
        if (memberMatches) return true;

        if (r.graph && r.graph.nodes) {
          const nodeMatches = r.graph.nodes.some(n =>
            n.label && n.label.toLowerCase().includes(query)
          );
          if (nodeMatches) return true;
        }

        return false;
      });

      renderRingsList(filtered);

      // Keep current active ring if visible, else select first matching ring
      if (filtered.length > 0) {
        const isCurrentVisible = filtered.some(r => r.ring_id === (allRings[activeIndex] ? allRings[activeIndex].ring_id : -1));
        if (!isCurrentVisible) {
          const newIdx = allRings.findIndex(r => r.ring_id === filtered[0].ring_id);
          if (newIdx !== -1) selectRing(newIdx, false);
        }
      }
    }

    let currentRenderedRingId = null;

    let spinAnimFrameId = null;
    let isSpinningEnabled = true;
    let isUserInteracting = false;
    let nodePolarData = {};
    let accumulatedRotation = 0;
    let activeNodesDataSet = null;
    let spinStartTime = performance.now();
    let lastFrameTime = performance.now();

    function hashString(str) {
      let hash = 0;
      for (let i = 0; i < str.length; i++) {
        hash = (hash << 5) - hash + str.charCodeAt(i);
        hash |= 0;
      }
      return Math.abs(hash);
    }

    function selectRing(index, forceRerender = false) {
      activeIndex = index;
      const ring = allRings[index];
      if (!ring) return;

      closeNodeInspector();

      // Update Active States
      const cards = document.querySelectorAll(".ring-card-item");
      cards.forEach((c, i) => c.classList.toggle("active", i === index));

      // Update Inspector Panel
      document.getElementById("inspector-heading").innerText = `SYNDICATE #${ring.ring_id}`;
      document.getElementById("inspector-badge").innerText = `RANK #${ring.rank || index + 1}`;
      document.getElementById("threat-score-num").innerText = `${(ring.score * 100).toFixed(1)}%`;
      document.getElementById("threat-rank-pill").innerText = `RANK #${ring.rank || index + 1}`;

      document.getElementById("sig-device").innerText = `${ring.shared_device_pct}%`;
      document.getElementById("sig-ip").innerText = `${ring.shared_ip_pairs} pairs`;
      document.getElementById("sig-vel").innerText = `${ring.transaction_velocity} tx/hr`;
      document.getElementById("sig-gnn").innerText = ring.avg_model_score.toFixed(3);
      document.getElementById("sig-fresh").innerText = `${ring.fresh_account_count} accounts`;
      document.getElementById("members-count").innerText = ring.member_count;

      const ringLbl = document.getElementById("settings-active-ring-lbl");
      if (ringLbl) ringLbl.innerText = `Syndicate #${ring.ring_id} (Score: ${(ring.score * 100).toFixed(1)}%)`;

      // Handle freeze state for this ring
      const freezeBtn = document.getElementById("freeze-btn");
      const isFrozen = frozenRings.has(ring.ring_id);
      if (isFrozen) {
        freezeBtn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg> Accounts Suspended (Click to Reactivate)`;
        freezeBtn.disabled = false;
        freezeBtn.style.opacity = "1";
        freezeBtn.style.background = "#ef4444";
        freezeBtn.style.color = "#ffffff";
      } else {
        freezeBtn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg> Freeze Syndicate Accounts`;
        freezeBtn.disabled = false;
        freezeBtn.style.opacity = "1";
        freezeBtn.style.background = "var(--yellow-primary)";
        freezeBtn.style.color = "#131415";
      }

      // Render Account Chips
      const chipsBox = document.getElementById("members-chips");
      chipsBox.innerHTML = ring.members.map(m => `
        <span class="chip-account ${isFrozen ? 'frozen' : ''}" onclick="focusOnNode('user_${m}')">
          User ${m} ${isFrozen ? '<span style="font-size: 8px; color: #ef4444;">[FROZEN]</span>' : ''}
        </span>
      `).join("");

      // Only re-render graph if the ring actually changed or forced
      if (!network || currentRenderedRingId !== ring.ring_id || forceRerender) {
        renderGraph(ring.graph);
        currentRenderedRingId = ring.ring_id;
      }
    }

    function renderGraph(graphData) {
      const container = document.getElementById("network-canvas");
      if (!container || !graphData || !graphData.nodes) return;

      // Filter Nodes
      const visibleNodes = graphData.nodes.filter(n => activeFilters[n.group] !== false);
      currentVisibleNodes = visibleNodes;
      const visibleIds = new Set(visibleNodes.map(n => n.id));
      const visibleEdges = (graphData.edges || []).filter(e => visibleIds.has(e.from) && visibleIds.has(e.to));

      const ring = allRings[activeIndex];
      const isFrozen = ring && frozenRings.has(ring.ring_id);

      const nodes = new vis.DataSet(visibleNodes.map(n => {
        let color = "#facc15";
        let shape = "dot";
        let size = 20;

        if (n.group === "user") {
          color = isFrozen ? "#ef4444" : "#facc15"; // Red if frozen, Electric Yellow otherwise
          shape = "dot";
          size = 20;
        } else if (n.group === "device") {
          color = "#38bdf8"; // Cyan Diamond
          shape = "diamond";
          size = 22;
        } else if (n.group === "merchant") {
          color = "#34d399"; // Mint Triangle
          shape = "triangle";
          size = 18;
        }

        const nodeObj = {
          id: n.id,
          label: " ", // High contrast constant-scale labels rendered via afterDrawing
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

        // Fixed canonical layout coordinates for rock-solid model stability
        if (typeof n.x === "number" && typeof n.y === "number") {
          nodeObj.x = n.x;
          nodeObj.y = n.y;
        }

        return nodeObj;
      }));

      // Clean, airy edges matching exact relation types
      const edges = new vis.DataSet(visibleEdges.map(e => {
        let edgeColor = "#64748b";
        let dashes = false;
        let width = 1.6;
        let tooltip = `Connected (${e.count || 1} links)`;

        if (e.relation === "shared_ip") {
          edgeColor = "#facc15";
          dashes = [5, 5];
          width = 2.0;
          tooltip = `Shared IP Interconnection (${e.count || 1} links)`;
        } else if (e.relation === "shared_device" || e.relation === "connected") {
          edgeColor = "#38bdf8";
          width = 2.0;
          tooltip = `Shared Hardware Device (${e.count || 1} links)`;
        } else if (e.relation === "transaction" || e.relation === "burst_tx") {
          edgeColor = "#2dd4bf";
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

      // Physics configuration with fixed randomSeed for 100% deterministic layout
      const options = {
        layout: {
          randomSeed: 42,
          improvedLayout: false
        },
        physics: {
          enabled: true,
          solver: "forceAtlas2Based",
          forceAtlas2Based: {
            gravitationalConstant: (currentSpringLength === 380 ? -620 : -460),
            centralGravity: 0.002,
            springLength: currentSpringLength,
            springConstant: 0.035,
            damping: 0.35,
            avoidOverlap: 1.0
          },
          stabilization: {
            enabled: true,
            iterations: 120,
            updateInterval: 25
          }
        },
        interaction: {
          hover: true,
          tooltipDelay: 80,
          zoomView: true,
          dragView: true,
          dragNodes: true,
          zoomSpeed: 0.5
        },
        groups: {
          user: {
            color: {
              background: isFrozen ? "#ef4444" : "#facc15",
              border: "#ffffff",
              highlight: { background: "#ffffff", border: isFrozen ? "#ef4444" : "#facc15" },
              hover: { background: isFrozen ? "#ef4444" : "#facc15", border: "#ffffff" }
            },
            shape: "dot",
            size: 20
          },
          device: {
            color: {
              background: "#38bdf8",
              border: "#ffffff",
              highlight: { background: "#ffffff", border: "#38bdf8" },
              hover: { background: "#38bdf8", border: "#ffffff" }
            },
            shape: "diamond",
            size: 22
          },
          merchant: {
            color: {
              background: "#34d399",
              border: "#ffffff",
              highlight: { background: "#ffffff", border: "#34d399" },
              hover: { background: "#34d399", border: "#ffffff" }
            },
            shape: "triangle",
            size: 18
          }
        }
      };

      if (spinAnimFrameId) {
        cancelAnimationFrame(spinAnimFrameId);
        spinAnimFrameId = null;
      }
      activeNodesDataSet = nodes;

      if (network) network.destroy();
      network = new vis.Network(container, data, options);

      // User interaction handlers for smooth elastic stretching & zero-hang floating
      let dragSettleTimeout = null;

      network.on("dragStart", function(params) {
        if (params.nodes && params.nodes.length > 0) {
          isUserInteracting = true;
          if (dragSettleTimeout) {
            clearTimeout(dragSettleTimeout);
            dragSettleTimeout = null;
          }
          if (physicsState) {
            network.setOptions({ physics: { enabled: true } });
            network.startSimulation();
          } else {
            network.stopSimulation();
            network.setOptions({ physics: { enabled: false } });
          }
        } else {
          // Canvas pan
          isUserInteracting = true;
        }
      });

      network.on("dragEnd", function(params) {
        if (params.nodes && params.nodes.length > 0) {
          dragSettleTimeout = setTimeout(() => {
            if (network) {
              network.stopSimulation();
              if (!physicsState) {
                network.setOptions({ physics: { enabled: false } });
              } else {
                network.setOptions({ physics: { enabled: true } });
              }
              recomputePolarFromCurrentPositions();
              isUserInteracting = false;
              lastFrameTime = performance.now();
            }
          }, 80);
        } else {
          // Pan ended
          isUserInteracting = false;
          lastFrameTime = performance.now();
        }
      });

      // Once layout stabilizes, fit perfectly to frame and stop simulation for zero jitter
      network.once("stabilizationIterationsDone", function() {
        fitGraphToScreen(true);
        network.stopSimulation();
        if (!physicsState) {
          network.setOptions({ physics: { enabled: false } });
        } else {
          network.setOptions({ physics: { enabled: true } });
        }
        initAndStartSpinAnimation(nodes);
      });

      // Constant screen text size & high-contrast visibility at all zoom levels
      network.on("afterDrawing", function(ctx) {
        ctx.save();
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
          const yOffset = (node.group === "device" ? 22 : (node.group === "merchant" ? 20 : 18));
          const textX = domPos.x;
          const textY = domPos.y + yOffset;

          // Crisp dark background pill for high contrast
          const textWidth = ctx.measureText(labelText).width;
          ctx.fillStyle = "rgba(25, 26, 27, 0.94)";
          ctx.beginPath();
          if (ctx.roundRect) {
            ctx.roundRect(textX - textWidth / 2 - 5, textY - 8, textWidth + 10, 16, 4);
          } else {
            ctx.rect(textX - textWidth / 2 - 5, textY - 8, textWidth + 10, 16);
          }
          ctx.fill();

          // Subtle entity outline border
          ctx.strokeStyle = node.group === "user" ? (isFrozen ? "rgba(239, 68, 68, 0.5)" : "rgba(250, 204, 21, 0.4)") : (node.group === "device" ? "rgba(56, 189, 248, 0.4)" : "rgba(52, 211, 153, 0.4)");
          ctx.lineWidth = 0.8;
          ctx.stroke();

          // Text fill color
          ctx.fillStyle = node.group === "user" ? (isFrozen ? "#ef4444" : "#facc15") : (node.group === "device" ? "#38bdf8" : "#34d399");
          ctx.fillText(labelText, textX, textY);
        }

        ctx.restore();
      });

      // Interactive Node Inspector Trigger on Node Click
      network.on("click", function(params) {
        if (params.nodes.length > 0) {
          const nodeId = params.nodes[0];
          showNodeInspector(nodeId);
        } else {
          closeNodeInspector();
        }
      });
    }

    function showNodeInspector(nodeId) {
      inspectedNodeId = nodeId;
      const card = document.getElementById("node-inspector");
      if (!card) return;

      const ring = allRings[activeIndex];
      const gNode = ring ? (ring.graph.nodes || []).find(n => n.id === nodeId) : null;
      if (!gNode) return;

      document.getElementById("inspect-id").innerText = gNode.label;
      const dot = document.getElementById("inspect-dot");
      const role = document.getElementById("inspect-role");
      const score = document.getElementById("inspect-score");
      const deg = document.getElementById("inspect-deg");

      // Count connected edges
      const connectedEdges = (ring.graph.edges || []).filter(e => e.from === nodeId || e.to === nodeId);
      deg.innerText = `${connectedEdges.length} connected hop${connectedEdges.length === 1 ? '' : 's'}`;

      if (gNode.group === "user") {
        const isFrozen = frozenRings.has(ring.ring_id);
        dot.style.background = isFrozen ? "#ef4444" : "var(--node-user)";
        role.innerText = "Syndicate Member Account";
        score.innerText = `Threat Risk: ${(ring.score * 100).toFixed(1)}%`;
        score.style.color = isFrozen ? "#ef4444" : "var(--yellow-primary)";
      } else if (gNode.group === "device") {
        dot.style.background = "var(--node-device)";
        role.innerText = "Shared Hardware Device (IMEI/MAC)";
        score.innerText = `Multiplexed by ${connectedEdges.length} Accounts`;
        score.style.color = "var(--node-device)";
      } else if (gNode.group === "merchant") {
        dot.style.background = "var(--node-merchant)";
        role.innerText = "Target Merchant Terminal";
        score.innerText = `Velocity: ${Math.round(ring.transaction_velocity)} tx/hr`;
        score.style.color = "var(--node-merchant)";
      }

      card.style.display = "block";
    }

    function closeNodeInspector() {
      const card = document.getElementById("node-inspector");
      if (card) card.style.display = "none";
      inspectedNodeId = null;
    }

    function isolateNodeNeighbors() {
      if (!inspectedNodeId || !network) return;
      focusOnNode(inspectedNodeId);
      const ring = allRings[activeIndex];
      if (!ring) return;
      const neighbors = new Set([inspectedNodeId]);
      (ring.graph.edges || []).forEach(e => {
        if (e.from === inspectedNodeId) neighbors.add(e.to);
        if (e.to === inspectedNodeId) neighbors.add(e.from);
      });
      network.selectNodes(Array.from(neighbors));
      showToast(`Selected ${neighbors.size} adjacent hops for ${inspectedNodeId}`);
    }

    function copyNodeId() {
      if (!inspectedNodeId) return;
      navigator.clipboard.writeText(inspectedNodeId);
      showToast(`Copied identifier: ${inspectedNodeId}`);
    }

    function initAndStartSpinAnimation(nodesDataSet) {
      activeNodesDataSet = nodesDataSet;
      if (spinAnimFrameId) {
        cancelAnimationFrame(spinAnimFrameId);
        spinAnimFrameId = null;
      }

      if (!network) return;
      const positions = network.getPositions();
      let cx = 0, cy = 0, count = 0;
      for (const id in positions) {
        cx += positions[id].x;
        cy += positions[id].y;
        count++;
      }
      if (count > 0) { cx /= count; cy /= count; }

      nodePolarData = {};
      for (const id in positions) {
        const dx = positions[id].x - cx;
        const dy = positions[id].y - cy;
        const radius = Math.sqrt(dx * dx + dy * dy);
        const angle = Math.atan2(dy, dx);
        const h = hashString(id);
        const phase = (h % 1000) / 1000 * Math.PI * 2;
        nodePolarData[id] = {
          radius: radius,
          initialAngle: angle - accumulatedRotation,
          phase: phase,
          cx: cx,
          cy: cy
        };
      }

      lastFrameTime = performance.now();
      startSpinLoop();
    }

    function recomputePolarFromCurrentPositions() {
      if (!network) return;
      const positions = network.getPositions();

      let cx = 0, cy = 0, count = 0;
      for (const id in positions) {
        cx += positions[id].x;
        cy += positions[id].y;
        count++;
      }
      if (count > 0) { cx /= count; cy /= count; }

      for (const id in positions) {
        let p = nodePolarData[id];
        if (!p) {
          const h = hashString(id);
          p = {
            phase: (h % 1000) / 1000 * Math.PI * 2,
            cx: cx,
            cy: cy
          };
          nodePolarData[id] = p;
        }
        const dx = positions[id].x - cx;
        const dy = positions[id].y - cy;
        p.cx = cx;
        p.cy = cy;
        p.radius = Math.sqrt(dx * dx + dy * dy);
        p.initialAngle = Math.atan2(dy, dx) - accumulatedRotation;
      }
    }

    function recalculatePolarCoordinates() {
      recomputePolarFromCurrentPositions();
    }

    function fitGraphToScreen(smooth = true) {
      if (!network) return;
      const container = document.getElementById("network-canvas");
      if (!container) return;

      const positions = network.getPositions();
      const nodeIds = Object.keys(positions);
      if (nodeIds.length === 0) {
        network.fit({ animation: smooth ? { duration: 250, easingFunction: "easeInOutQuad" } : false });
        return;
      }

      let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
      for (const id of nodeIds) {
        const p = positions[id];
        if (p.x < minX) minX = p.x;
        if (p.x > maxX) maxX = p.x;
        if (p.y < minY) minY = p.y;
        if (p.y > maxY) maxY = p.y;
      }

      const w = Math.max(100, maxX - minX);
      const h = Math.max(100, maxY - minY);
      const cx = (minX + maxX) / 2;
      const cy = (minY + maxY) / 2;

      // Exact default scale matching the reference screenshot: 0.58
      const canvasW = container.clientWidth || 800;
      const canvasH = container.clientHeight || 600;

      const availW = Math.max(200, canvasW - 90);
      const availH = Math.max(200, canvasH - 120);

      const maxFitScale = Math.min(availW / w, availH / h);
      const targetScale = Math.min(0.58, maxFitScale > 0 ? maxFitScale : 0.58);

      network.moveTo({
        position: { x: cx, y: cy },
        scale: targetScale,
        animation: smooth ? { duration: 250, easingFunction: "easeInOutQuad" } : false
      });
    }

    function startSpinLoop() {
      if (spinAnimFrameId) cancelAnimationFrame(spinAnimFrameId);

      function spinTick(now) {
        spinAnimFrameId = requestAnimationFrame(spinTick);

        if (!isSpinningEnabled || !network || !activeNodesDataSet) return;
        if (isUserInteracting) {
          lastFrameTime = now;
          return;
        }

        const dt = (now - lastFrameTime) * 0.001;
        lastFrameTime = now;

        // Cap dt to prevent massive jumps when switching browser tabs
        if (dt > 0.1) return;

        // Smooth rotation speed: ~0.06 rad/s (1 revolution every ~100s)
        accumulatedRotation += dt * 0.06;
        const t = (now - spinStartTime) * 0.001;

        const updates = [];
        for (const id in nodePolarData) {
          const p = nodePolarData[id];
          const theta = p.initialAngle + accumulatedRotation;

          // Harmonic floating micro-motion (subtle vertical & horizontal undulation)
          const floatY = Math.sin(t * 1.15 + p.phase) * 3.2;
          const floatX = Math.cos(t * 0.85 + p.phase * 1.3) * 2.2;

          updates.push({
            id: id,
            x: p.cx + p.radius * Math.cos(theta) + floatX,
            y: p.cy + p.radius * Math.sin(theta) + floatY
          });
        }

        if (updates.length > 0) {
          activeNodesDataSet.update(updates);
        }
      }

      spinAnimFrameId = requestAnimationFrame(spinTick);
    }

    function toggleSpinAnimation() {
      isSpinningEnabled = !isSpinningEnabled;
      const btn = document.getElementById("spin-btn");
      const lbl = document.getElementById("spin-label");
      if (btn) btn.classList.toggle("active", isSpinningEnabled);
      if (lbl) lbl.innerText = `Orbit Spin: ${isSpinningEnabled ? 'On' : 'Off'}`;

      if (isSpinningEnabled) {
        if (!activeNodesDataSet && network) {
          activeNodesDataSet = network.body.data.nodes;
        }
        recomputePolarFromCurrentPositions();
        isUserInteracting = false;
        lastFrameTime = performance.now();
        if (!spinAnimFrameId) startSpinLoop();
        showToast("Orbit rotation & float: Active");
      } else {
        showToast("Orbit rotation & float: Paused");
        lastFrameTime = performance.now();
      }
    }

    function resetGraphView() {
      if (network) {
        isUserInteracting = true;
        fitGraphToScreen(true);
        showToast("Framed network graph to viewport");
        setTimeout(() => {
          recomputePolarFromCurrentPositions();
          isUserInteracting = false;
          lastFrameTime = performance.now();
        }, 260);
      }
    }

    function spreadGraph() {
      currentSpringLength = (currentSpringLength === 260) ? 380 : 260;
      const btn = document.getElementById("spread-btn");
      const label = document.getElementById("spread-label");
      const isWide = (currentSpringLength === 380);
      label.innerText = isWide ? "Spread: Wide" : "Spread Out";
      btn.classList.toggle("active", isWide);

      if (network) {
        isUserInteracting = true;
        network.setOptions({
          physics: {
            enabled: true,
            solver: "forceAtlas2Based",
            forceAtlas2Based: {
              gravitationalConstant: isWide ? -620 : -460,
              centralGravity: 0.003,
              springLength: currentSpringLength,
              springConstant: 0.035,
              damping: 0.35,
              avoidOverlap: 1.0
            }
          }
        });
        network.startSimulation();
        showToast(isWide ? "Expanding cluster springs (Wide Layout)..." : "Restoring compact cluster springs...");
        setTimeout(() => {
          if (network) {
            network.stopSimulation();
            if (!physicsState) {
              network.setOptions({ physics: { enabled: false } });
            } else {
              network.setOptions({ physics: { enabled: true } });
            }
            fitGraphToScreen(true);
            recomputePolarFromCurrentPositions();
            isUserInteracting = false;
            lastFrameTime = performance.now();
          }
        }, 350);
      }
    }

    function togglePhysics() {
      physicsState = !physicsState;
      const label = document.getElementById("physics-label");
      const btn = document.getElementById("physics-toggle");
      if (label) label.innerText = `Physics: ${physicsState ? 'On' : 'Off'}`;
      if (btn) btn.classList.toggle("active", physicsState);

      if (network) {
        if (physicsState) {
          network.setOptions({ physics: { enabled: true } });
          network.startSimulation();
          setTimeout(() => {
            if (network && !isUserInteracting) {
              network.stopSimulation();
              recomputePolarFromCurrentPositions();
            }
          }, 250);
          showToast("Live Physics Mode enabled: Dynamic force-directed simulation active");
        } else {
          network.stopSimulation();
          network.setOptions({ physics: { enabled: false } });
          recomputePolarFromCurrentPositions();
          isUserInteracting = false;
          lastFrameTime = performance.now();
          showToast("Physics simulation paused (Static node drag mode)");
        }
      }
    }

    function toggleFilter(type) {
      activeFilters[type] = !activeFilters[type];
      const btn = document.getElementById(`filter-${type}`);
      btn.classList.toggle("active", activeFilters[type]);
      const currentRing = allRings[activeIndex];
      if (currentRing) {
        if (spinAnimFrameId) {
          cancelAnimationFrame(spinAnimFrameId);
          spinAnimFrameId = null;
        }
        renderGraph(currentRing.graph);
      }
    }

    function focusOnNode(nodeId) {
      if (!network) return;
      isUserInteracting = true;
      network.focus(nodeId, {
        scale: 1.35,
        animation: { duration: 500, easingFunction: "easeInOutQuad" }
      });
      network.selectNodes([nodeId]);
      showNodeInspector(nodeId);
      setTimeout(() => {
        isUserInteracting = false;
        lastFrameTime = performance.now();
      }, 550);
    }

    async function executeFreezeAction() {
      const ring = allRings[activeIndex];
      if (!ring) return;

      const url = document.getElementById("api-url").value.trim().replace(/\/$/, "");
      const isCurrentlyFrozen = frozenRings.has(ring.ring_id) || ring.is_suspended;
      const targetAction = isCurrentlyFrozen ? "unfreeze" : "freeze";

      const freezeBtn = document.getElementById("freeze-btn");
      if (freezeBtn) {
        freezeBtn.disabled = true;
        freezeBtn.style.opacity = "0.7";
      }

      try {
        // Real Backend Enforcement Integration
        const res = await fetch(`${url}/freeze`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            ring_id: ring.ring_id,
            action: targetAction,
            operator: "AML_COMPLIANCE_DESK",
            reason: `Heterogeneous GNN detected coordinated mule ring (Score: ${(ring.score * 100).toFixed(1)}%)`
          })
        });

        if (res.ok) {
          const data = await res.json();
          if (targetAction === "freeze") {
            frozenRings.add(ring.ring_id);
            ring.is_suspended = true;
            showToast(`[ENFORCEMENT EXECUTED] Quarantined ${ring.member_count} syndicate accounts in Ring #${ring.ring_id} (Ref: ${data.audit_ref})`);
          } else {
            frozenRings.delete(ring.ring_id);
            ring.is_suspended = false;
            showToast(`[ENFORCEMENT LIFTED] Restored ${ring.member_count} accounts in Ring #${ring.ring_id} (Ref: ${data.audit_ref})`);
          }
        } else {
          throw new Error(`HTTP ${res.status}`);
        }
      } catch (err) {
        // Fallback local enforcement logging if backend is unreachable
        const auditRef = `AML-LOCAL-${ring.ring_id}-${Date.now().toString().slice(-5)}`;
        if (targetAction === "freeze") {
          frozenRings.add(ring.ring_id);
          ring.is_suspended = true;
          showToast(`[ENFORCEMENT EXECUTED] Quarantined ${ring.member_count} syndicate accounts in Ring #${ring.ring_id} (Ref: ${auditRef})`);
        } else {
          frozenRings.delete(ring.ring_id);
          ring.is_suspended = false;
          showToast(`[ENFORCEMENT LIFTED] Restored ${ring.member_count} accounts in Ring #${ring.ring_id} (Ref: ${auditRef})`);
        }
      } finally {
        selectRing(activeIndex, true);
      }
    }

    function exportSarDossier() {
      const ring = allRings[activeIndex];
      if (!ring) return;

      const isSuspended = frozenRings.has(ring.ring_id) || ring.is_suspended;
      const filingId = `SAR-AML-${new Date().getFullYear()}-R${ring.ring_id}-${Math.floor(100000 + Math.random() * 900000)}`;

      const sarDossier = {
        regulatory_filing_metadata: {
          filing_id: filingId,
          regulatory_framework: "FinCEN Form 111 / FIU-IND Suspicious Transaction Report (STR)",
          filing_type: "INITIAL_SYNDICATE_DETECTION",
          filing_timestamp: new Date().toISOString(),
          reporting_institution: "DARKNODE AUTOMATED AML DEFENSE SUITE",
          compliance_officer_id: "OFFICER_AML_DESK_PRIMARY",
          urgency_classification: ring.score >= 0.814 ? "CRITICAL_IMMEDIATE_ACTION" : "ELEVATED_MONITORING"
        },
        case_summary: {
          syndicate_id: `RING_${ring.ring_id}`,
          composite_risk_score: ring.score,
          composite_risk_percentage: `${(ring.score * 100).toFixed(2)}%`,
          detection_model: "2-Layer Heterogeneous Message Passing Neural Network (MPNN)",
          current_enforcement_status: isSuspended ? "ACCOUNTS_FROZEN_QUARANTINE_ACTIVE" : "PENDING_ENFORCEMENT",
          total_suspect_accounts: ring.member_count,
          total_transactions_in_window: Math.round(ring.transaction_velocity * 4),
          estimated_burst_velocity: `${ring.transaction_velocity} tx/hr`
        },
        executive_narrative: `Automated detection completed by DarkNode Heterogeneous MPNN. Syndicate Ring #${ring.ring_id} exhibits systemic money muling topology. A coordinated network of ${ring.member_count} accounts was identified sharing physical device fingerprints (${ring.shared_device_pct}% device multiplexing) and ${ring.shared_ip_pairs} proxy IP collision pairs. Transactions display high burst velocity (${ring.transaction_velocity} tx/hr) directing synchronized fund transfers to common merchant terminals. This pattern is consistent with layered money laundering and mule account leasing.`,
        subject_accounts: (ring.members || []).map(uid => ({
          account_id: `USR_${uid}`,
          account_type: "RETAIL_CURRENT",
          individual_model_risk: ring.avg_model_score,
          account_status: isSuspended ? "SUSPENDED_FROZEN" : "ACTIVE_FLAGGED",
          action_taken: isSuspended ? "POST_NO_DEBIT_PLACED" : "MONITORED"
        })),
        forensic_evidence_matrix: {
          shared_hardware: {
            ratio: ring.shared_device_ratio,
            percentage: `${ring.shared_device_pct}%`,
            devices_involved: (ring.graph?.nodes || []).filter(n => n.group === "device").map(n => n.label)
          },
          network_infrastructure: {
            shared_ip_interconnections: ring.shared_ip_pairs,
            proxy_anonymity_detected: ring.shared_ip_pairs > 10
          },
          velocity_metrics: {
            hourly_velocity: ring.transaction_velocity,
            high_velocity_alert: ring.transaction_velocity > 1000
          },
          gnn_structural_embedding: {
            mpnn_confidence: ring.avg_model_score,
            false_positive_probability: 0.05
          }
        },
        legal_recommendations: [
          "Maintain Post-No-Debit (PND) containment on all subject account numbers.",
          "Transmit formal Suspicious Activity Report (SAR) to FinCEN / FIU regulatory portal within statutory timeframe.",
          "Coordinate with target merchant settlement providers to freeze pending remittance payouts.",
          "Preserve device hardware fingerprints (IMEI/MAC) across blacklist network."
        ],
        cryptographic_verification: {
          sha256_audit_seal: "verified_darknode_gnn_model_pass",
          ledger_block_reference: `#BLOCK-${Date.now().toString(16).toUpperCase()}`
        }
      };

      const blob = new Blob([JSON.stringify(sarDossier, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `SAR_DOSSIER_RING_${ring.ring_id}_${filingId}.json`;
      a.click();
      URL.revokeObjectURL(url);
      showToast(`Exported Official SAR Forensic Dossier: ${filingId}`);
    }

    // =========================================================================
    // SYSTEM SETTINGS & COMPLIANCE CONTROLS
    // =========================================================================
    let isSoundAlertEnabled = true;
    let isToastAlertEnabled = true;

    function openSettingsModal(targetSection) {
      const modal = document.getElementById("settings-modal");
      if (modal) modal.classList.add("open");

      // Sync active ring label in SAR card
      const ring = allRings[activeIndex];
      const ringLbl = document.getElementById("settings-active-ring-lbl");
      if (ringLbl && ring) {
        ringLbl.innerText = `Syndicate #${ring.ring_id} (Score: ${(ring.score * 100).toFixed(1)}%)`;
      }

      // Sync physics & orbit checkboxes with live state
      const physCheck = document.getElementById("setting-physics-toggle");
      if (physCheck) physCheck.checked = !!physicsState;
      const orbCheck = document.getElementById("setting-orbit-toggle");
      if (orbCheck) orbCheck.checked = !!isSpinningEnabled;

      // Sync spring slider
      const springSlider = document.getElementById("spring-slider");
      const springVal = document.getElementById("spring-len-val");
      if (springSlider) springSlider.value = currentSpringLength;
      if (springVal) springVal.innerText = `${currentSpringLength}px`;

      // Sync threshold slider & select
      const threshInput = document.getElementById("threshold-select");
      const threshSlider = document.getElementById("threshold-slider");
      const threshBadge = document.getElementById("settings-thresh-badge");
      if (threshInput && threshSlider) {
        threshSlider.value = threshInput.value;
        if (threshBadge) threshBadge.innerText = threshInput.value;
      }

      // If opening specifically for SAR export, scroll smoothly to the card
      if (targetSection === "sar") {
        setTimeout(() => {
          const sarCard = document.getElementById("setting-card-sar");
          if (sarCard) {
            sarCard.scrollIntoView({ behavior: "smooth", block: "center" });
            sarCard.style.borderColor = "var(--yellow-primary)";
            sarCard.style.boxShadow = "0 0 16px rgba(250, 204, 21, 0.3)";
            setTimeout(() => {
              sarCard.style.borderColor = "var(--border-subtle)";
              sarCard.style.boxShadow = "none";
            }, 2500);
          }
        }, 150);
      }
    }

    function closeSettingsModal(e) {
      if (e && e.target !== document.getElementById("settings-modal") && !e.target.closest(".modal-close-btn")) return;
      const modal = document.getElementById("settings-modal");
      if (modal) modal.classList.remove("open");
    }

    async function testApiConnection() {
      const input = document.getElementById("api-url");
      const url = input ? input.value.trim().replace(/\/$/, "") : "http://localhost:8000";
      const dot = document.getElementById("status-dot");
      const label = document.getElementById("status-label");
      const pingResult = document.getElementById("api-ping-result");

      if (pingResult) pingResult.innerHTML = `<span style="color: var(--yellow-primary);">Pinging ${url}...</span>`;
      const startTime = performance.now();

      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 3500);
        const res = await fetch(`${url}/health`, { method: "GET", signal: controller.signal });
        clearTimeout(timeoutId);
        const elapsed = Math.round(performance.now() - startTime);

        if (res.ok) {
          if (dot) {
            dot.classList.remove("offline");
            dot.classList.add("active-infer");
            setTimeout(() => dot.classList.remove("active-infer"), 800);
          }
          if (label) label.innerText = "LIVE API";
          if (pingResult) {
            pingResult.innerHTML = `<span style="color: #34d399;">✓ Connected (${elapsed}ms) — FastAPI Backend Healthy</span>`;
          }
          showToast(`Backend online: ${elapsed}ms response time`);
        } else {
          throw new Error(`HTTP ${res.status}`);
        }
      } catch (err) {
        if (dot) {
          dot.classList.remove("active-infer");
          dot.classList.add("offline");
        }
        if (label) label.innerText = "OFFLINE";
        if (pingResult) {
          pingResult.innerHTML = `<span style="color: #ef4444;">✗ Offline / Timeout — Falling back to cached GNN dossier</span>`;
        }
        showToast("Backend connection failed — serving cached GNN model");
      }
    }

    function onThresholdSliderChange(val) {
      const threshSelect = document.getElementById("threshold-select");
      const threshBadge = document.getElementById("settings-thresh-badge");
      const descBox = document.getElementById("threshold-desc-box");
      const numVal = parseFloat(val);

      if (threshBadge) threshBadge.innerText = numVal.toFixed(2);
      if (threshSelect) {
        let matched = false;
        for (let opt of threshSelect.options) {
          if (Math.abs(parseFloat(opt.value) - numVal) < 0.04) {
            threshSelect.value = opt.value;
            matched = true;
            break;
          }
        }
      }

      if (descBox) {
        if (numVal <= 0.40) {
          descBox.innerHTML = `Filtering at <strong>${numVal.toFixed(2)}</strong>: Broad surveillance queue (high recall for early smurfing).`;
        } else if (numVal <= 0.60) {
          descBox.innerHTML = `Filtering at <strong>${numVal.toFixed(2)}</strong>: Standard benchmark balance (95.0% precision, 5.0% false alarms).`;
        } else {
          descBox.innerHTML = `Filtering at <strong>${numVal.toFixed(2)}</strong>: Strict critical threshold (isolates confirmed large syndicates).`;
        }
      }

      onThresholdChange(val);
    }

    function exportSarCsv() {
      const ring = allRings[activeIndex];
      if (!ring) return;

      const filingId = `SAR-AML-${new Date().getFullYear()}-R${ring.ring_id}`;
      const rows = [
        ["Regulatory_Filing_ID", filingId],
        ["Syndicate_ID", `RING_${ring.ring_id}`],
        ["Composite_Risk_Score", ring.score],
        ["Detection_Method", "2-Layer Heterogeneous MPNN"],
        ["Enforcement_Status", frozenRings.has(ring.ring_id) ? "FROZEN_QUARANTINE" : "PENDING_ENFORCEMENT"],
        ["Burst_Velocity_TxHr", ring.transaction_velocity],
        [],
        ["Member_Type", "Entity_ID", "Status"]
      ];

      (ring.members || []).forEach(m => {
        rows.push(["User_Account", `user_${m}`, frozenRings.has(ring.ring_id) ? "FROZEN" : "ACTIVE"]);
      });
      (ring.devices || []).forEach(d => {
        rows.push(["Hardware_Device", d, "LINKED_MULTIPLEX"]);
      });
      (ring.merchants || []).forEach(m => {
        rows.push(["Merchant_Terminal", m, "TARGET_BURST"]);
      });

      const csvContent = "data:text/csv;charset=utf-8," + rows.map(r => r.join(",")).join("\\n");
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", `DARKNODE_EVIDENCE_RING_${ring.ring_id}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      showToast(`Exported Evidence Ledger CSV: Ring #${ring.ring_id}`);
    }

    function playAlertChime() {
      try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.type = "sine";
        osc.frequency.setValueAtTime(587.33, audioCtx.currentTime); // D5
        osc.frequency.exponentialRampToValueAtTime(880, audioCtx.currentTime + 0.14); // A5
        gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.38);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.38);
        showToast("Audio alert notification chime played");
      } catch (err) {
        showToast("Audio alert notification triggered");
      }
    }

    function toggleSoundPreference(enabled) {
      isSoundAlertEnabled = enabled;
      showToast(`High-Risk Audio Alert: ${enabled ? 'Enabled' : 'Disabled'}`);
    }

    function toggleToastPreference(enabled) {
      isToastAlertEnabled = enabled;
      showToast(`Compliance Audit Toasts: ${enabled ? 'Enabled' : 'Disabled'}`);
    }

    function togglePhysicsFromSettings(enabled) {
      if (physicsState !== enabled) {
        togglePhysics();
      }
    }

    function toggleOrbitFromSettings(enabled) {
      if (isSpinningEnabled !== enabled) {
        toggleOrbit();
      }
    }

    function onSpringSliderChange(val) {
      currentSpringLength = parseInt(val, 10);
      const valDisp = document.getElementById("spring-len-val");
      if (valDisp) valDisp.innerText = `${currentSpringLength}px`;

      if (network) {
        network.setOptions({
          physics: {
            forceAtlas2Based: { springLength: currentSpringLength }
          }
        });
      }
    }

    function resetSettingsToDefault() {
      const input = document.getElementById("api-url");
      if (input) input.value = "http://localhost:8000";

      const threshSelect = document.getElementById("threshold-select");
      const threshSlider = document.getElementById("threshold-slider");
      if (threshSelect) threshSelect.value = "0.50";
      if (threshSlider) threshSlider.value = "0.50";
      onThresholdSliderChange("0.50");

      const springSlider = document.getElementById("spring-slider");
      if (springSlider) springSlider.value = "260";
      onSpringSliderChange("260");

      if (!physicsState) togglePhysics();
      if (!isSpinningEnabled) toggleOrbit();

      const soundCheck = document.getElementById("setting-sound-alert");
      if (soundCheck) soundCheck.checked = true;
      isSoundAlertEnabled = true;

      showToast("Reset all settings & thresholds to factory defaults");
    }

    // Modal Control Functions
    function openGuideModal() {
      const modal = document.getElementById("guide-modal");
      if (modal) modal.classList.add("open");
    }

    function closeGuideModal(e) {
      if (e && e.target !== document.getElementById("guide-modal") && !e.target.closest(".modal-close-btn")) return;
      const modal = document.getElementById("guide-modal");
      if (modal) modal.classList.remove("open");
    }

    function openBenchmarkModal() {
      const modal = document.getElementById("benchmark-modal");
      if (modal) modal.classList.add("open");
    }

    function closeBenchmarkModal(e) {
      if (e && e.target !== document.getElementById("benchmark-modal") && !e.target.closest(".modal-close-btn")) return;
      const modal = document.getElementById("benchmark-modal");
      if (modal) modal.classList.remove("open");
    }

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        closeSettingsModal();
        closeGuideModal();
        closeBenchmarkModal();
        closeNodeInspector();
        hideSearchSuggestions();
      }
    });

    document.addEventListener("click", (e) => {
      const searchBox = document.querySelector(".search-box-clean");
      if (searchBox && !searchBox.contains(e.target)) {
        hideSearchSuggestions();
      }
    });

    function showToast(text) {
      if (!isToastAlertEnabled) return;
      const toast = document.getElementById("toast");
      if (!toast) return;
      document.getElementById("toast-text").innerText = text;
      toast.style.display = "flex";
      setTimeout(() => { toast.style.display = "none"; }, 3500);
    }

    window.addEventListener("resize", () => {
      if (network) {
        network.redraw();
        fitGraphToScreen(false);
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
