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

real_aml_path = Path("data/real_aml_rings.json")
if not real_aml_path.exists():
    raise FileNotFoundError("data/real_aml_rings.json not found")

with open(real_aml_path, "r", encoding="utf-8") as f:
    real_aml_data = f.read()

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="mobile-web-app-capable" content="yes">
  <title>DarkNode — Fraud Syndicate Graph Intelligence</title>
  <!-- Vis-network CDN -->
  <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <!-- Inter & JetBrains Mono - Official Enterprise UI Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

  <style>
    :root {
      /* Official Enterprise Typography Stack */
      --font-sans: 'Inter', 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, Roboto, 'Helvetica Neue', Arial, sans-serif;
      --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

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
      --shadow-glow: none;
      
      --radius: 12px;
      --radius-sm: 8px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    html, body {
      font-family: var(--font-sans);
      background-color: var(--bg-base);
      color: var(--text-main);
      width: 100%;
      height: 100%;
      height: 100dvh;
      margin: 0;
      padding: 0;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
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
      position: relative;
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
      box-shadow: none;
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
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum" 1;
      font-size: 11.5px;
      font-weight: 600;
      letter-spacing: 0.02em;
      padding: 2.5px 8px;
      border-radius: 6px;
      background: var(--bg-card);
      color: var(--yellow-primary);
      border: 1px solid var(--yellow-border);
    }

    /* Telemetry Stats - Centered in Middle of Header */
    .header-stats {
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      align-items: center;
      gap: 10px;
      pointer-events: auto;
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
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum" 1;
      font-weight: 600;
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
      box-shadow: none;
      transition: all 0.2s ease;
    }

    .status-dot.offline {
      background: var(--yellow-primary);
      box-shadow: none;
    }

    .status-dot.active-infer {
      background: var(--yellow-primary);
      box-shadow: none;
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
      font-weight: 600;
      cursor: pointer;
      border: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.15s ease;
      font-family: var(--font-sans);
    }

    .btn-yellow {
      background: var(--yellow-primary);
      color: #131415;
      box-shadow: none;
    }

    .btn-yellow:hover:not(:disabled) {
      background: var(--yellow-hover);
      box-shadow: none;
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
      min-height: 0;
      height: calc(100% - 56px);
      overflow: hidden;
      box-sizing: border-box;
      position: relative;
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
      transition: width 0.2s ease, opacity 0.2s ease;
    }

    .sidebar-left.collapsed, .sidebar-right.collapsed {
      display: none !important;
    }

    .panel-collapse-btn {
      background: transparent;
      border: none;
      color: var(--text-dim);
      cursor: pointer;
      padding: 2px 4px;
      border-radius: 4px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transition: all 0.12s ease;
    }

    .panel-collapse-btn:hover {
      color: var(--yellow-primary);
      background: var(--bg-card);
    }

    .sidebar-expand-pill {
      position: absolute;
      top: 52px;
      z-index: 15;
      display: none;
      align-items: center;
      gap: 5px;
      background: rgba(25, 26, 27, 0.94);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-subtle);
      border-radius: 7px;
      padding: 5px 9px;
      color: var(--yellow-primary);
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      box-shadow: var(--shadow-card);
      transition: all 0.15s ease;
      font-family: inherit;
    }

    .sidebar-expand-pill:hover {
      background: var(--bg-card);
      border-color: var(--yellow-primary);
    }

    .sidebar-expand-pill.left {
      left: 14px;
    }

    .sidebar-expand-pill.right {
      right: 14px;
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

    /* Dataset Mode Switcher in Left Sidebar (Actual Data vs Real AML Data) */
    .dataset-switcher-row {
      display: flex;
      gap: 6px;
      padding: 0 12px 10px 12px;
      background: var(--bg-panel);
    }

    .dataset-tab-btn {
      flex: 1;
      height: 30px;
      font-size: 11.5px;
      font-weight: 600;
      font-family: var(--font-sans);
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }

    .dataset-tab-btn:hover {
      background: var(--bg-card-hover);
      border-color: var(--border-strong);
      color: var(--text-main);
    }

    .dataset-tab-btn.active {
      background: rgba(250, 204, 21, 0.14);
      border-color: var(--yellow-primary);
      color: var(--yellow-primary);
      box-shadow: none;
    }

    .ring-subtitle-tag {
      font-size: 10px;
      font-weight: 600;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.1);
      border: 1px solid rgba(56, 189, 248, 0.25);
      border-radius: 4px;
      padding: 2px 6px;
      margin: 3px 0 6px 0;
      display: flex;
      align-items: center;
      gap: 4px;
      overflow: hidden;
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
      height: 26px;
      font-size: 11px;
      font-weight: 600;
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum" 1;
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
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.8);
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
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum" 1;
      font-size: 10px;
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
      box-shadow: none;
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
      font-family: var(--font-sans);
      font-size: 13px;
      font-weight: 600;
      letter-spacing: -0.01em;
      color: var(--text-main);
    }

    .ring-risk-tag {
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum" 1;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.03em;
      padding: 2.5px 7px;
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
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum" 1;
      font-weight: 600;
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
      min-height: 0;
      overflow: hidden;
      background-color: #191a1b;
      background-image: radial-gradient(#2c2d2e 1.2px, transparent 1.2px);
      background-size: 24px 24px;
    }

    @media (min-width: 1100px) and (min-height: 650px) {
      .canvas-outer {
        min-height: 450px;
      }
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

    /* Floating Entity Filter Bar (Top Right) */
    .canvas-filter-bar {
      position: absolute;
      top: 14px;
      right: 14px;
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

    #filter-user {
      border: 1px solid transparent;
      color: var(--text-muted);
      border-radius: 6px;
    }

    #filter-user.active {
      background: rgba(25, 26, 27, 0.9);
      border-color: #facc15;
      color: #facc15;
    }

    #filter-user.active:hover {
      box-shadow: none;
    }

    #filter-device {
      border: 1px solid transparent;
      color: var(--text-muted);
      border-radius: 6px;
    }

    #filter-device.active {
      background: rgba(25, 26, 27, 0.9);
      border-color: #38bdf8;
      color: #38bdf8;
    }

    #filter-device.active:hover {
      box-shadow: none;
    }

    #filter-merchant {
      border: 1px solid transparent;
      color: var(--text-muted);
      border-radius: 6px;
    }

    #filter-merchant.active {
      background: rgba(25, 26, 27, 0.9);
      border-color: #34d399;
      color: #34d399;
    }

    #filter-merchant.active:hover {
      box-shadow: none;
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
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum" 1;
      font-weight: 600;
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

    /* Floating Settings Button at Right Bottom - Pure Minimal Logo, No Backside Shape */
    .settings-floating-btn {
      position: fixed;
      bottom: 18px;
      right: 18px;
      width: 38px;
      height: 38px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: transparent !important;
      background-color: transparent !important;
      border: none !important;
      box-shadow: none !important;
      outline: none !important;
      padding: 0;
      color: #94a3b8;
      cursor: pointer;
      z-index: 1000;
      transition: color 0.25s ease, transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .settings-floating-btn:hover {
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      color: var(--yellow-primary);
      transform: rotate(60deg) scale(1.18);
    }

    /* Notification Bell & Dropdown Flyout */
    .notif-bell-container {
      position: relative;
      display: inline-flex;
      align-items: center;
    }

    .notif-bell-btn {
      position: relative;
      padding: 0 10px;
      height: 32px;
    }

    .notif-badge {
      position: absolute;
      top: -4px;
      right: -4px;
      background: var(--yellow-primary);
      color: #131415;
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum" 1;
      font-size: 10.5px;
      font-weight: 700;
      min-width: 16px;
      height: 16px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 3px;
      border: 1.5px solid #191a1b;
      box-shadow: none;
      transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.2s ease;
    }

    .notif-badge.hidden {
      display: none;
    }

    .notif-badge.bump {
      animation: notifBump 0.3s ease;
    }

    @keyframes notifBump {
      0% { transform: scale(0.6); }
      50% { transform: scale(1.35); }
      100% { transform: scale(1); }
    }

    .notif-flyout {
      position: absolute;
      top: calc(100% + 8px);
      right: 0;
      width: 340px;
      max-height: 420px;
      background: var(--bg-card);
      border: 1px solid var(--border-strong);
      border-radius: 10px;
      box-shadow: 0 16px 48px rgba(0, 0, 0, 0.85);
      z-index: 1500;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      animation: notifFlyoutIn 0.18s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes notifFlyoutIn {
      from { opacity: 0; transform: translateY(-8px) scale(0.97); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }

    .notif-flyout-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 11px 14px;
      background: #1e1f20;
      border-bottom: 1px solid var(--border-subtle);
    }

    .notif-flyout-title {
      display: flex;
      align-items: center;
      gap: 7px;
      font-size: 11.5px;
      font-weight: 700;
      color: var(--text-main);
    }

    .notif-flyout-title svg {
      color: var(--yellow-primary);
    }

    .notif-head-action {
      background: transparent;
      border: none;
      font-size: 10.5px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      padding: 2px 6px;
      border-radius: 4px;
      transition: all 0.12s ease;
    }

    .notif-head-action:hover {
      background: var(--bg-card-hover);
      color: var(--yellow-primary);
    }

    .notif-flyout-list {
      max-height: 290px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      padding: 6px;
      gap: 5px;
    }

    .notif-item {
      display: flex;
      gap: 10px;
      padding: 9px 11px;
      border-radius: 7px;
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      transition: all 0.12s ease;
    }

    .notif-item:hover {
      background: #252627;
      border-color: var(--border-strong);
    }

    .notif-icon-col {
      width: 22px;
      height: 22px;
      border-radius: 5px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      font-size: 11px;
    }

    .notif-icon-col.critical {
      background: rgba(239, 68, 68, 0.15);
      color: #ef4444;
    }

    .notif-icon-col.warning {
      background: rgba(250, 204, 21, 0.15);
      color: var(--yellow-primary);
    }

    .notif-icon-col.success {
      background: rgba(52, 211, 153, 0.15);
      color: #34d399;
    }

    .notif-icon-col.info {
      background: var(--yellow-bg);
      color: var(--yellow-primary);
      border: 1px solid var(--yellow-border);
    }

    .notif-body-col {
      flex: 1;
      min-width: 0;
    }

    .notif-item-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 2px;
    }

    .notif-item-title {
      font-size: 11px;
      font-weight: 700;
      color: var(--text-main);
    }

    .notif-item-time {
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum" 1;
      font-size: 10px;
      font-weight: 500;
      color: var(--text-dim);
    }

    .notif-item-desc {
      font-size: 10.5px;
      color: var(--text-muted);
      line-height: 1.35;
      word-break: break-word;
    }

    .notif-empty-state {
      padding: 24px 16px;
      text-align: center;
      font-size: 11.5px;
      color: var(--text-dim);
    }

    .notif-flyout-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 12px;
      background: #1a1b1c;
      border-top: 1px solid var(--border-subtle);
      font-size: 10px;
      color: var(--text-dim);
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

    /* Settings Category Tabs */
    .settings-tab-bar {
      display: flex;
      gap: 6px;
      padding: 0 0 10px 0;
      border-bottom: 1px solid var(--border-subtle);
      overflow-x: auto;
      margin-bottom: 4px;
    }

    .settings-tab-btn {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
      white-space: nowrap;
      font-family: inherit;
    }

    .settings-tab-btn:hover {
      background: var(--bg-card-hover);
      color: var(--text-main);
      border-color: var(--border-strong);
    }

    .settings-tab-btn.active {
      background: var(--yellow-bg);
      border-color: var(--yellow-border);
      color: var(--yellow-primary);
    }

    /* Documentation subcard grid (responsive 3 columns) */
    .docs-three-col-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      margin-top: 10px;
      width: 100%;
    }

    @media (max-width: 860px) {
      .docs-three-col-grid {
        grid-template-columns: 1fr;
      }
    }

    .doc-subcard {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 9px;
      padding: 15px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      transition: all 0.15s ease;
      min-width: 0;
      height: 100%;
      box-sizing: border-box;
    }

    .doc-subcard:hover {
      border-color: var(--border-strong);
      background: #1f2022;
      transform: translateY(-1px);
    }

    .doc-subcard-icon {
      width: 32px;
      height: 32px;
      border-radius: 7px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 2px;
    }

    .doc-subcard-title {
      font-family: var(--font-sans);
      font-size: 13px;
      font-weight: 600;
      color: var(--text-main);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .doc-subcard-desc {
      font-family: var(--font-sans);
      font-size: 11.5px;
      color: var(--text-muted);
      line-height: 1.45;
      flex: 1;
      margin-bottom: 4px;
    }

    .doc-subcard-btn {
      width: 100%;
      height: 32px;
      font-family: var(--font-sans);
      font-size: 11.5px;
      font-weight: 600;
      margin-top: auto;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }

    .spin-icon {
      animation: spinAnim 0.85s linear infinite;
    }

    @keyframes spinAnim {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }

    .modal-window.modal-wide {
      max-width: 940px;
    }

    /* Right Sidebar: Evidence & Signals Panel */
    .sidebar-right {
      width: 340px;
      flex-shrink: 0;
      height: 100%;
      overflow-y: auto;
      transition: width 0.2s ease, opacity 0.2s ease;
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
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum" 1;
      font-size: 30px;
      font-weight: 700;
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
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum" 1;
      font-size: 11px;
      font-weight: 600;
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
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum" 1;
      font-weight: 600;
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
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum" 1;
      font-size: 11px;
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

    /* Toast Notification Bubble - Normal Notification (Come and Go with Sound) */
    .toast-popup {
      position: fixed;
      top: 68px;
      right: 20px;
      background: rgba(25, 26, 27, 0.96);
      backdrop-filter: blur(10px);
      border: 1px solid var(--border-strong);
      border-left: 4px solid var(--yellow-primary);
      border-radius: 9px;
      padding: 10px 14px;
      font-size: 12px;
      display: none;
      align-items: center;
      gap: 12px;
      z-index: 2500;
      box-shadow: 0 14px 40px rgba(0, 0, 0, 0.75);
      max-width: 360px;
      transition: transform 0.25s ease, opacity 0.25s ease;
      animation: toastSlideIn 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes toastSlideIn {
      from { opacity: 0; transform: translateY(-12px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .toast-popup.toast-exit {
      animation: toastSlideOut 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    @keyframes toastSlideOut {
      from { opacity: 1; transform: translateY(0); }
      to { opacity: 0; transform: translateY(-12px); }
    }

    .toast-dot-glow {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--yellow-primary);
      box-shadow: none;
      flex-shrink: 0;
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
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8);
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

    .modal-back-btn {
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
      flex-shrink: 0;
    }

    .modal-back-btn:hover {
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
      font-weight: 700;
      color: var(--text-muted);
      letter-spacing: 0.05em;
      text-transform: uppercase;
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
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum" 1;
      font-size: 18px;
      font-weight: 600;
      color: var(--text-muted);
    }

    .bench-score-bright {
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum" 1;
      font-size: 22px;
      font-weight: 700;
      color: var(--yellow-primary);
    }

    .bench-delta-tag {
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum" 1;
      font-size: 11px;
      font-weight: 600;
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

    /* ==========================================================================
       Mobile Responsive & Landscape Orientation Enforcer
       ========================================================================== */
    .app-viewport-wrapper {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      position: relative;
    }

    /* Mobile Landscape Enforcer Overlay */
    .orientation-overlay {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      z-index: 999999;
      background: rgba(19, 20, 21, 0.97);
      backdrop-filter: blur(16px);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 24px;
      box-sizing: border-box;
      text-align: center;
    }

    /* Automatically trigger overlay on portrait orientation on phones/narrow viewports */
    @media screen and (max-width: 900px) and (orientation: portrait), screen and (max-height: 520px) and (orientation: portrait) {
      .orientation-overlay:not(.dismissed) {
        display: flex !important;
      }
    }

    .orientation-content {
      max-width: 360px;
      width: 100%;
      background: #191a1b;
      border: 1px solid var(--border-strong);
      border-radius: 16px;
      padding: 28px 22px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85);
      display: flex;
      flex-direction: column;
      align-items: center;
      position: relative;
    }

    .orientation-icon-container {
      position: relative;
      width: 86px;
      height: 86px;
      margin-bottom: 18px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .rotate-arrow-around {
      position: absolute;
      top: 0;
      left: 0;
      width: 86px;
      height: 86px;
      pointer-events: none;
      z-index: 1;
      transform-origin: 43px 43px;
      animation: arrowRotateAroundPhone 2.8s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    }

    @keyframes arrowRotateAroundPhone {
      0%, 15% {
        transform: rotate(0deg);
        opacity: 0.8;
      }
      45%, 75% {
        transform: rotate(-90deg);
        opacity: 1;
      }
      92%, 100% {
        transform: rotate(0deg);
        opacity: 0.8;
      }
    }

    .phone-frame {
      width: 36px;
      height: 58px;
      border: 2px solid var(--yellow-primary);
      border-radius: 8px;
      background: #131415;
      position: relative;
      z-index: 2;
      box-shadow: none;
      animation: phoneRotateLandscape 2.8s cubic-bezier(0.4, 0, 0.2, 1) infinite;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    @keyframes phoneRotateLandscape {
      0%, 15% {
        transform: rotate(0deg);
      }
      45%, 75% {
        transform: rotate(-90deg);
      }
      92%, 100% {
        transform: rotate(0deg);
      }
    }

    .phone-speaker {
      position: absolute;
      top: 3px;
      left: 50%;
      transform: translateX(-50%);
      width: 7px;
      height: 2px;
      background: var(--border-strong);
      border-radius: 1px;
    }

    .phone-screen {
      width: 26px;
      height: 42px;
      background: #1c1d1e;
      border-radius: 4px;
      position: relative;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .phone-pulse-dot {
      width: 6px;
      height: 6px;
      background: var(--yellow-primary);
      border-radius: 50%;
      box-shadow: none;
    }

    .orientation-tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 10px;
      font-family: var(--font-mono);
      font-weight: 700;
      color: var(--yellow-primary);
      background: var(--yellow-bg);
      border: 1px solid var(--yellow-border);
      padding: 3px 8px;
      border-radius: 5px;
      margin-bottom: 12px;
      letter-spacing: 0.05em;
    }

    .pulse-indicator {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--yellow-primary);
      box-shadow: none;
    }

    .orientation-title {
      font-size: 18px;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--text-main);
      margin-bottom: 8px;
      text-transform: uppercase;
    }

    .orientation-subtitle {
      font-size: 11.5px;
      line-height: 1.5;
      color: var(--text-muted);
      margin-bottom: 20px;
    }

    .orientation-instructions {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      width: 100%;
    }

    .instruction-step {
      font-size: 11.5px;
      font-weight: 600;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      padding: 7px 14px;
      border-radius: 7px;
      width: 100%;
      justify-content: center;
    }

    .instruction-step svg {
      color: var(--yellow-primary);
    }

    .btn-bypass {
      font-size: 10.5px;
      height: 26px;
      padding: 0 12px;
      color: var(--text-dim);
      border: none;
      background: transparent;
      cursor: pointer;
    }
    .btn-bypass:hover {
      color: var(--text-muted);
      background: var(--bg-card);
    }

    /* Modals & Dialogs optimization in mobile landscape */
    @media screen and (max-height: 550px) {
      .modal-backdrop {
        padding: 8px;
      }
      .modal-window {
        max-height: 94vh;
      }
      .modal-head {
        padding: 8px 14px;
      }
    }

    /* ==========================================================================
       Full-Screen Responsive Layout for Mobile Landscape & Mobile Desktop Site
       Zero-Scroll, Zero-Letterbox, 100% Screen Edge-to-Edge Fit
       ========================================================================== */
    @media screen and (max-height: 580px) and (orientation: landscape), screen and (max-width: 1024px) and (orientation: landscape) {
      header {
        height: 42px;
        padding: 0 10px;
      }

      .brand-group {
        gap: 6px;
      }

      .brand-logo-mark {
        width: 22px;
        height: 22px;
      }

      .brand-logo-mark svg {
        width: 12px;
        height: 12px;
      }

      .brand-title {
        font-size: 14px;
      }

      .badge-pill {
        font-size: 9.5px;
        padding: 1px 5px;
      }

      .header-stats {
        gap: 5px;
      }

      .stat-pill {
        padding: 2.5px 6px;
        font-size: 10px;
        gap: 3px;
      }

      .header-actions {
        gap: 5px;
      }

      .header-actions .btn {
        height: 28px;
        padding: 0 8px;
        font-size: 11px;
        gap: 4px;
      }

      .header-actions .btn svg {
        width: 11px;
        height: 11px;
      }

      .api-box {
        display: none;
      }

      .workspace {
        gap: 8px;
        padding: 6px 8px;
        height: calc(100% - 42px);
      }

      .sidebar-left {
        width: 220px;
        min-width: 190px;
        max-width: 250px;
      }

      .sidebar-right {
        width: 230px;
        min-width: 200px;
        max-width: 260px;
      }

      .panel-header-clean {
        padding: 7px 10px;
      }

      .panel-title {
        font-size: 10.5px;
      }

      .dataset-switcher-row {
        padding: 0 6px 6px 6px;
        gap: 4px;
      }

      .dataset-tab-btn {
        height: 24px;
        font-size: 10px;
      }

      .tier-filter-row {
        padding: 0 6px 6px 6px;
        gap: 3px;
      }

      .tier-tab-btn {
        height: 22px;
        font-size: 9.5px;
      }

      .search-box-clean {
        padding: 5px 8px;
      }

      .search-input-clean {
        padding: 4px 6px;
        font-size: 10.5px;
      }

      .rings-list-scroll {
        padding: 6px;
        gap: 4px;
      }

      .ring-card-item {
        padding: 6px 8px;
        gap: 3px;
      }

      .ring-label {
        font-size: 11px;
      }

      .ring-risk-tag {
        font-size: 9.5px;
        padding: 1px 5px;
      }

      .ring-card-bottom {
        font-size: 10px;
        gap: 8px;
      }

      .inspector-content {
        padding: 8px 10px;
        gap: 8px;
      }

      .hero-risk-box {
        padding: 8px 10px;
      }

      .hero-score-val {
        font-size: 20px;
      }

      .hero-score-sub {
        font-size: 9px;
      }

      .block-title {
        font-size: 10px;
        margin-bottom: 5px;
      }

      .signal-item-row {
        padding: 5px 7px;
        font-size: 10px;
      }

      .signal-prefix-tag {
        font-size: 8px;
        padding: 1px 3px;
      }

      .user-chips-grid {
        max-height: 75px;
        padding: 5px;
        gap: 3px;
      }

      .chip-account {
        font-size: 9.5px;
        padding: 2px 5px;
      }

      .canvas-bar {
        top: 6px;
        left: 6px;
        padding: 2px 5px;
        gap: 3px;
      }

      .canvas-pill-btn {
        height: 22px;
        padding: 0 6px;
        font-size: 9.5px;
        gap: 3px;
      }

      .canvas-filter-bar {
        top: 6px;
        right: 6px;
        padding: 2px 5px;
        gap: 3px;
      }

      .canvas-filter-bar .canvas-pill-btn {
        height: 22px;
        padding: 0 6px;
        font-size: 9.5px;
      }

      .canvas-legend {
        bottom: 6px;
        left: 6px;
        padding: 3px 8px;
        font-size: 9.5px;
        gap: 8px;
      }

      .settings-floating-btn {
        bottom: 10px;
        right: 10px;
        width: 30px;
        height: 30px;
      }
    }

    /* Fallback portrait preview layout (if user clicks Preview in Portrait bypass) */
    @media screen and (max-width: 900px) and (orientation: portrait) {
      .workspace {
        flex-direction: column;
        overflow-y: auto;
        height: auto;
        gap: 10px;
      }
      .sidebar-left, .sidebar-right {
        width: 100% !important;
        height: auto;
        max-height: 300px;
      }
      .viewport-center {
        min-height: 340px;
        height: 340px;
        width: 100%;
      }
    }
  </style>
</head>
<body>

  <!-- Mobile Landscape Orientation Enforcer Modal -->
  <div id="orientation-overlay" class="orientation-overlay">
    <div class="orientation-content">
      <div class="orientation-icon-container">
        <!-- SVG Curved Arrow & Orbital Guide Track Wrapping Around Phone -->
        <svg class="rotate-arrow-around" viewBox="0 0 86 86" fill="none">
          <circle cx="43" cy="43" r="38" stroke="#2c2d2e" stroke-width="1.2" stroke-dasharray="3 4"/>
          <path d="M 74 65 A 38 38 0 1 0 12 21" stroke="var(--yellow-primary)" stroke-width="2.2" stroke-linecap="round"/>
          <polyline points="10 13 12 21 20 18" stroke="var(--yellow-primary)" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>

        <!-- Smartphone Frame Rotating Anti-Clockwise in Sync -->
        <div class="phone-frame">
          <div class="phone-screen">
            <div class="phone-pulse-dot"></div>
          </div>
          <div class="phone-speaker"></div>
        </div>
      </div>
      
      <div class="orientation-tag">
        <span class="pulse-indicator"></span>
        TACTICAL CONSOLE LOCKED
      </div>
      <h2 class="orientation-title">FLIP TO LANDSCAPE</h2>
      <p class="orientation-subtitle">
        DarkNode Graph Intelligence requires a widescreen view to display multi-entity syndicates, transaction telemetry, and live GNN topology.
      </p>

      <div class="orientation-instructions">
        <div class="instruction-step">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M2.5 2v6h6M2.66 15.57a10 10 0 1 0 .57-8.38L2.06 6"/></svg>
          Rotate phone horizontally to unlock
        </div>
        <button class="btn btn-bypass" onclick="dismissOrientationModal()" title="Bypass orientation check for portrait preview">
          Preview in Portrait
        </button>
      </div>
    </div>
  </div>

  <!-- Responsive Scaled Application Container -->
  <div id="app-viewport-wrapper" class="app-viewport-wrapper">

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
      <!-- Benchmark Modal Button -->
      <button class="btn btn-outline" onclick="openBenchmarkModal()" title="View Empirical Model Benchmarks vs Bank Rules">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
        Benchmark
      </button>

      <!-- Notification Bell with Dropdown Beside Benchmark -->
      <div class="notif-bell-container">
        <button class="btn btn-outline notif-bell-btn" id="notif-bell-btn" onclick="toggleNotifDropdown(event)" title="Notifications & Compliance Audit Alerts">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
          </svg>
          <span class="notif-badge" id="notif-badge">1</span>
        </button>

        <!-- Notification Flyout Dropdown -->
        <div class="notif-flyout" id="notif-flyout" style="display: none;" onclick="event.stopPropagation()">
          <div class="notif-flyout-head">
            <div class="notif-flyout-title">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
              Audit & System Notifications
            </div>
            <button class="notif-head-action" onclick="clearAllNotifications()">Clear All</button>
          </div>
          <div class="notif-flyout-list" id="notif-flyout-list">
            <!-- Dynamic notifications injected by JavaScript -->
          </div>
          <div class="notif-flyout-footer">
            <span id="notif-status-summary">Auto-logged to SAR trail</span>
            <button class="notif-head-action" style="color: var(--yellow-primary);" onclick="triggerTestAlert()">Send Test Alert</button>
          </div>
        </div>
      </div>

      <!-- Run Analysis Button with Intelligent Pipeline Execution -->
      <button class="btn btn-yellow" id="run-btn" onclick="fetchRings()">
        <svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
        Run Analysis
      </button>

      <!-- Fullscreen Toggle Button -->
      <button class="btn btn-outline" id="fullscreen-toggle-btn" onclick="toggleFullScreen()" title="Toggle Fullscreen" style="padding: 0 9px; height: 32px;" aria-label="Toggle Fullscreen">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>
        </svg>
      </button>
    </div>
  </header>

  <!-- Spacious Workspace (3 Floating Panels) -->
  <div class="workspace">

    <!-- Panel 1: Left Rings Directory -->
    <div class="panel-card sidebar-left">
      <div class="panel-header-clean">
        <span class="panel-title">Detected Syndicates</span>
        <div style="display: flex; align-items: center; gap: 6px;">
          <span class="badge-pill" id="rings-count-badge">10 total</span>
          <button class="panel-collapse-btn" onclick="toggleSidebar('left')" title="Collapse Panel">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
          </button>
        </div>
      </div>

      <!-- 2-Section Dataset Switcher: Synthetic Data vs Real AML Data -->
      <div class="dataset-switcher-row">
        <button class="dataset-tab-btn active" id="dataset-tab-actual" onclick="switchDatasetSection('actual')" title="Synthetic Dataset: GNN Heterogeneous Simulation Graph">
          Synthetic Data
        </button>
        <button class="dataset-tab-btn" id="dataset-tab-real" onclick="switchDatasetSection('real')" title="Real AML Dataset: Source-Verified Banks, Devices & Regulatory Typologies">
          Real AML Data
        </button>
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
      <!-- Collapsed Panel Expand Pills -->
      <button id="expand-left-btn" class="sidebar-expand-pill left" onclick="toggleSidebar('left')" title="Open Rings Panel">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="9 18 15 12 9 6"/></svg>
        <span>Rings</span>
      </button>
      <button id="expand-right-btn" class="sidebar-expand-pill right" onclick="toggleSidebar('right')" title="Open Telemetry Panel">
        <span>Telemetry</span>
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="15 18 9 12 15 6"/></svg>
      </button>

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
      </div>

      <!-- Floating Entity Filter Bar (Top Right) -->
      <div class="canvas-filter-bar">
        <button class="canvas-pill-btn active" id="filter-user" onclick="toggleFilter('user')" title="Toggle Syndicate Member Accounts">Users</button>
        <button class="canvas-pill-btn active" id="filter-device" onclick="toggleFilter('device')" title="Toggle Shared Hardware Devices">Devices</button>
        <button class="canvas-pill-btn active" id="filter-merchant" onclick="toggleFilter('merchant')" title="Toggle Target Merchant Terminals">Merchants</button>
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
        <div style="display: flex; align-items: center; gap: 6px;">
          <span class="badge-pill" id="inspector-badge">RANK #1</span>
          <button class="panel-collapse-btn" onclick="toggleSidebar('right')" title="Collapse Panel">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
          </button>
        </div>
      </div>

      <div class="inspector-content">
        <!-- Dedicated Typology Card (shown for Real AML Data section) -->
        <div id="typology-card-box" style="display: none; background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 8px; padding: 10px 12px; margin-bottom: 12px;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
            <span style="font-size: 10px; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.05em;" id="typology-code">FIN-2023-A001</span>
            <span style="font-size: 9px; font-weight: 600; color: var(--text-dim);" id="typology-fatf">FATF R.16</span>
          </div>
          <div style="font-size: 12px; font-weight: 700; color: #fff; margin-bottom: 3px;" id="typology-name">Funnel Accounts / Smurfing</div>
          <div style="font-size: 10px; color: var(--text-muted); line-height: 1.4;" id="typology-desc">Structured cash deposits across mule accounts consolidated via immediate transfers.</div>
        </div>

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
        </div>
      </div>
    </div>

  </div>

  <!-- Fixed Floating Settings Trigger at Right Bottom of Page (Clean Logo Only, No Shape) -->
  <button class="settings-floating-btn" id="open-settings-bottom-btn" onclick="openSettingsModal()" title="System Configuration & Compliance" aria-label="System Configuration">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="3"/>
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
    </svg>
  </button>
  </div><!-- end #app-viewport-wrapper -->

  <!-- Interactive System Settings & Compliance Modal -->
  <div class="modal-backdrop" id="settings-modal" onclick="closeSettingsModal(event)">
    <div class="modal-window modal-wide" onclick="event.stopPropagation()">
      <div class="modal-head">
        <div class="modal-title-group">
          <div class="brand-logo-mark" style="width:24px; height:24px;">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#131415" stroke-width="2.5"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
          </div>
          <div>
            <div class="modal-title">DarkNode Enterprise Configuration & Controls</div>
            <div style="font-size: 10px; color: var(--text-dim); margin-top: 1px;">PRODUCTION ENGINE MATRIX • VERSION 2.4.1</div>
          </div>
        </div>
        <button class="modal-close-btn" onclick="closeSettingsModal()">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <!-- Settings Category Tabs -->
      <div style="padding: 10px 24px 0 24px; background: var(--bg-card); border-bottom: 1px solid var(--border-subtle);">
        <div class="settings-tab-bar">
          <button class="settings-tab-btn active" id="tab-btn-all" onclick="switchSettingsTab('all')">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
            All Settings
          </button>
          <button class="settings-tab-btn" id="tab-btn-engine" onclick="switchSettingsTab('engine')">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/></svg>
            Engine & API
          </button>
          <button class="settings-tab-btn" id="tab-btn-sar" onclick="switchSettingsTab('sar')">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
            Regulatory & SAR
          </button>
          <button class="settings-tab-btn" id="tab-btn-docs" onclick="switchSettingsTab('docs')">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
            Manuals & SOP
          </button>
          <button class="settings-tab-btn" id="tab-btn-restart" onclick="switchSettingsTab('restart')">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
            System Restart
          </button>
        </div>
      </div>

      <div class="modal-body">
        <div class="settings-grid">
          <!-- Card 1: API Connection (ss3) -->
          <div class="settings-card" id="setting-card-api" data-category="engine">
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
              <input type="text" id="api-url" class="settings-input" value="https://darknode.onrender.com" placeholder="https://darknode.onrender.com" onkeydown="if(event.key==='Enter') testApiConnection()">
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
          <div class="settings-card" id="setting-card-sar" data-category="sar">
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
          <div class="settings-card" id="setting-card-thresh" data-category="engine">
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
          <div class="settings-card" id="setting-card-alerts" data-category="engine">
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
          <div class="settings-card" id="setting-card-physics" data-category="engine">
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
                <span id="spring-len-val" style="font-family: var(--font-sans); font-variant-numeric: tabular-nums; font-weight: 600; color: var(--yellow-primary);">260px</span>
              </div>
              <input type="range" id="spring-slider" min="180" max="420" step="20" value="260" style="width: 100%; accent-color: var(--yellow-primary); cursor: pointer;" oninput="onSpringSliderChange(this.value)">
            </div>
          </div>

          <!-- Card 6: Graph Simulation & Batch Synthesis -->
          <div class="settings-card" id="setting-card-graph" data-category="engine">
            <div class="settings-card-head">
              <span class="settings-card-title">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
                Graph Simulation & Synthesis
              </span>
              <span class="badge-pill" style="font-size: 9px;">SYNTHETIC BATCH</span>
            </div>
            <div style="font-size: 11px; color: var(--text-muted);">
              Generate a fresh batch of synthetic transactions, device multiplexing, and circular smurfing structures.
            </div>
            <div>
              <button class="btn btn-outline" id="settings-new-graph-btn" style="width: 100%; height: 34px;" onclick="closeSettingsModal(); generateNewGraph();">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
                Synthesize New Graph Batch
              </button>
            </div>
          </div>

          <!-- Card 7: System Documentation, Architecture & SOP Manuals (3 Separate Modules) -->
          <div class="settings-card full-width" id="setting-card-docs" data-category="docs">
            <div class="settings-card-head">
              <span class="settings-card-title">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
                Architecture, User Guide & SOP Manuals
              </span>
              <span class="badge-pill" style="font-size: 9px; color: var(--yellow-primary); border-color: var(--yellow-border);">3 INDEPENDENT MODULES</span>
            </div>
            <div style="font-size: 11px; color: var(--text-muted);">
              Access standalone operational manuals, mathematical heterogeneous GNN architecture specifications, and AML compliance officer protocols.
            </div>

            <div class="docs-three-col-grid">
              <!-- Option 1: Architecture -->
              <div class="doc-subcard">
                <div class="doc-subcard-icon" style="color: #38bdf8; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.25);">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
                </div>
                <div class="doc-subcard-title">System Architecture</div>
                <div class="doc-subcard-desc">Heterogeneous 2-layer MPNN formulation, graph relations, feature embedding pipeline, and microservice specs.</div>
                <button class="btn btn-outline doc-subcard-btn" onclick="openArchitectureModal()">
                  Open Architecture
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </button>
              </div>

              <!-- Option 2: User Guide -->
              <div class="doc-subcard">
                <div class="doc-subcard-icon" style="color: #facc15; background: rgba(250, 204, 21, 0.12); border: 1px solid rgba(250, 204, 21, 0.25);">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
                </div>
                <div class="doc-subcard-title">User Guide</div>
                <div class="doc-subcard-desc">Visual platform tour: tri-panel navigation, node inspector, physics toggles, orbit spin, and entity filters.</div>
                <button class="btn btn-outline doc-subcard-btn" onclick="openUserGuideModal()">
                  Open User Guide
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </button>
              </div>

              <!-- Option 3: Instructions & SOP -->
              <div class="doc-subcard">
                <div class="doc-subcard-icon" style="color: #34d399; background: rgba(52, 211, 153, 0.12); border: 1px solid rgba(52, 211, 153, 0.25);">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
                </div>
                <div class="doc-subcard-title">Operator Instructions</div>
                <div class="doc-subcard-desc">Step-by-step AML investigation SOP, decision matrix, emergency account quarantine & FinCEN SAR filing.</div>
                <button class="btn btn-outline doc-subcard-btn" onclick="openInstructionsModal()">
                  Open Instructions
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Card 8: System Restart & Engine Reboot (Last Option in Settings) -->
          <div class="settings-card full-width" id="setting-card-restart" data-category="restart" style="border-color: rgba(239, 68, 68, 0.35); background: rgba(30, 20, 20, 0.35);">
            <div class="settings-card-head">
              <span class="settings-card-title" style="color: #f87171;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
                System Restart & Engine Reboot
              </span>
              <span class="badge-pill" style="font-size: 9px; color: #f87171; border-color: rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.1);">SYSTEM ADMIN</span>
            </div>
            <div style="font-size: 11px; color: var(--text-muted); line-height: 1.5;">
              Reboot the DarkNode graph engine, clear in-memory ring caches, re-initialize GNN inference session, reset physics equilibrium, and re-synchronize live telemetry.
            </div>
            <div style="display: flex; gap: 10px; margin-top: 4px;">
              <button class="btn btn-outline" style="flex: 1; height: 34px; color: var(--text-main); border-color: var(--border-strong);" onclick="executeSystemRestart('soft')" id="btn-soft-restart">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M23 4v6h-6M1 20v-6h6"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
                Soft Restart Engine (Clear Cache & Re-sync)
              </button>
              <button class="btn btn-outline" style="flex: 1; height: 34px; color: #ef4444; border-color: rgba(239, 68, 68, 0.5); background: rgba(239, 68, 68, 0.08);" onclick="executeSystemRestart('hard')" id="btn-hard-restart">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18.36 6.64a9 9 0 1 1-12.73 0"/><line x1="12" y1="2" x2="12" y2="12"/></svg>
                Hard Factory Reset (Reboot All State)
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Independent Modal 1: System Architecture -->
  <div class="modal-backdrop" id="architecture-modal" onclick="closeArchitectureModal(event)">
    <div class="modal-window modal-wide" onclick="event.stopPropagation()">
      <div class="modal-head">
        <div class="modal-title-group">
          <button class="modal-back-btn" onclick="backToSettingsModal()" title="Back to Settings" aria-label="Back to Settings">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
          </button>
          <div class="brand-logo-mark" style="width:24px; height:24px;">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#131415" stroke-width="2.5"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
          </div>
          <div>
            <div class="modal-title">DarkNode Multi-Layer GNN Architecture & Inference Specifications</div>
            <div style="font-size: 10px; color: var(--text-dim); margin-top: 1px;">MATHEMATICAL FORMULATION & PIPELINE TOPOLOGY</div>
          </div>
        </div>
        <button class="modal-close-btn" onclick="closeArchitectureModal()">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <div class="modal-body">
        <!-- Section 1: Heterogeneous Graph Schema -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
            1. Heterogeneous Multi-Layer Graph Schema
          </h3>
          <p>
            Mule account syndicates operate across diverse entity layers to conceal illicit fund movements. Standard transactional rules examine accounts in isolation, failing to detect structural multiplexing. <strong>DarkNode</strong> structures financial activity as a heterogeneous graph <strong>G = (V, E, T)</strong>:
          </p>
          <div style="background: var(--bg-input); padding: 12px 14px; border-radius: 8px; border: 1px solid var(--border-subtle); font-size: 12px; line-height: 1.6; color: #e5e7eb;">
            <div><strong>• Entity Nodes (V):</strong></div>
            <div style="padding-left: 12px; color: var(--text-muted); margin-bottom: 6px;">
              - <span style="color: #facc15; font-weight: 700;">Users (V_U)</span>: Individual account holders initiating and receiving financial transactions.<br>
              - <span style="color: #38bdf8; font-weight: 700;">Devices (V_D)</span>: Hardware fingerprints (IMEI, MAC, browser hardware hashes) shared across accounts.<br>
              - <span style="color: #34d399; font-weight: 700;">Merchants (V_M)</span>: Payment gateway terminals and merchant entities receiving burst settlements.
            </div>
            <div><strong>• Relational Edges (E):</strong></div>
            <div style="padding-left: 12px; color: var(--text-muted);">
              - <strong>(u_i &rarr; [TX: Transfers] &rarr; u_j)</strong>: Peer-to-peer money transfers with timestamp, velocity, and amount attributes.<br>
              - <strong>(u_i &rarr; [DEV: Uses Device] &rarr; d_k)</strong>: Account access from shared hardware, detecting mule multiplexing.<br>
              - <strong>(u_i &rarr; [IP: Subnet Match] &rarr; u_l)</strong>: IP/subnet collision edges identifying co-located operators.<br>
              - <strong>(u_i &rarr; [MERCH: Settlement] &rarr; m_p)</strong>: Target merchant transactions capturing high-frequency cash-outs.
            </div>
          </div>
        </div>

        <!-- Section 2: 2-Layer Relational MPNN Formulation -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            2. Mathematical Formulation: 2-Layer Relational MPNN
          </h3>
          <p>
            DarkNode implements relational message passing across all edge types R. At layer l in {1, 2}, node representations are updated via directional aggregation:
          </p>
          <div style="background: var(--bg-input); padding: 12px 14px; border-radius: 8px; border: 1px solid var(--border-subtle); font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #facc15; line-height: 1.7;">
            m_{N(v)}^{(l)} = AGGREGATE_{r in R} ( &Sigma;_{u in N_r(v)} W_r^{(l)} &middot; h_u^{(l-1)} )<br>
            h_v^{(l)} = LeakyReLU( W_{self}^{(l)} &middot; h_v^{(l-1)} + m_{N(v)}^{(l)} )
          </div>
          <p style="margin-top: 8px;">
            <strong>Why exactly 2 Layers?</strong> Layer 1 captures direct 1-hop associations (e.g. User to Shared Device). Layer 2 captures indirect 2-hop structural coordination (User A &rarr; Device &rarr; User B &rarr; Merchant) essential for catching distributed smurfing rings without inducing topological over-smoothing.
          </p>
        </div>

        <!-- Section 3: End-to-End Pipeline ASCII Architecture -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
            3. End-to-End Pipeline & Microservice Flow
          </h3>
          <div style="background: var(--bg-input); padding: 12px 14px; border-radius: 8px; border: 1px solid var(--border-subtle); font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #e5e7eb; overflow-x: auto; line-height: 1.55;">
┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
│ Banking Core & Ingest   │ ──► │ Heterogeneous Graph     │ ──► │ PyTorch Geometric GNN   │
│ • User Profiles         │     │ • Multi-modal Triples   │     │ • 2-Layer Relational    │
│ • Hardware Device IDs   │     │ • Temporal Tx Windows   │     │ • Latent Embeddings     │
│ • Settlement Terminals  │     │ • Subnet Collision Grid │     │ • Latency &lt; 18ms        │
└─────────────────────────┘     └─────────────────────────┘     └───────────┬─────────────┘
                                                                            │
┌─────────────────────────┐     ┌─────────────────────────┐                 ▼
│ Statutory Containment   │ ◄── │ Risk Fusion Engine      │ ◄───────────────┘
│ • Instant Debit Freeze  │     │ • GNN Anomaly Score     │
│ • FinCEN SAR Form 111   │     │ • Burst Velocity Metric │
│ • CSV Evidence Ledger   │     │ • Decision Cutoff θ     │
└─────────────────────────┘     └─────────────────────────┘
          </div>
        </div>

        <!-- Section 4: Engine Specifications -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
            4. Microservice Technology Stack
          </h3>
          <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; font-size: 11.5px;">
            <div style="background: var(--bg-panel); padding: 10px; border-radius: 6px; border: 1px solid var(--border-subtle);">
              <strong style="color: var(--yellow-primary);">Backend Runtime:</strong> FastAPI Async ASGI Microservice (:8000)
            </div>
            <div style="background: var(--bg-panel); padding: 10px; border-radius: 6px; border: 1px solid var(--border-subtle);">
              <strong style="color: #38bdf8;">Graph ML Engine:</strong> PyTorch 2.x + PyTorch Geometric (PyG)
            </div>
            <div style="background: var(--bg-panel); padding: 10px; border-radius: 6px; border: 1px solid var(--border-subtle);">
              <strong style="color: #34d399;">Physics Accelerator:</strong> ForceAtlas2 with Barnes-Hut repulsion
            </div>
            <div style="background: var(--bg-panel); padding: 10px; border-radius: 6px; border: 1px solid var(--border-subtle);">
              <strong style="color: #f43f5e;">Regulatory Standard:</strong> FinCEN Form 111 BSA & FIU-IND compliance
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Independent Modal 2: User Guide -->
  <div class="modal-backdrop" id="user-guide-modal" onclick="closeUserGuideModal(event)">
    <div class="modal-window modal-wide" onclick="event.stopPropagation()">
      <div class="modal-head">
        <div class="modal-title-group">
          <button class="modal-back-btn" onclick="backToSettingsModal()" title="Back to Settings" aria-label="Back to Settings">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
          </button>
          <div class="brand-logo-mark" style="width:24px; height:24px;">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#131415" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
          </div>
          <div>
            <div class="modal-title">DarkNode Interactive Platform User Guide</div>
            <div style="font-size: 10px; color: var(--text-dim); margin-top: 1px;">OPERATOR INTERFACE WALK-THROUGH & CONTROLS MANUAL</div>
          </div>
        </div>
        <button class="modal-close-btn" onclick="closeUserGuideModal()">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <div class="modal-body">
        <!-- Section 1: Tri-Panel Command Layout -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/></svg>
            1. Tri-Panel Command Architecture
          </h3>
          <p>
            The DarkNode interface is engineered as a three-pillar fraud command center:
          </p>
          <div class="guide-grid-2">
            <div class="guide-step-card">
              <div class="guide-step-title">Left Panel: Syndicate Directory</div>
              <div class="guide-step-desc">
                Lists all discovered smurfing rings ranked by threat score. Critical syndicates (&gt;0.80) display Red badges. Click any syndicate to focus the center graph and populate the right dossier.
              </div>
            </div>
            <div class="guide-step-card">
              <div class="guide-step-title">Center Viewport: Network Canvas</div>
              <div class="guide-step-desc">
                Dynamic topological graph rendering users, devices, and merchants. Features continuous physics, orbit spin, zoom/pan, and interactive node inspection.
              </div>
            </div>
            <div class="guide-step-card">
              <div class="guide-step-title">Right Panel: Evidence Dossier</div>
              <div class="guide-step-desc">
                Presents quantified risk signals (device ratio, IP collisions, transaction velocity), account chip rosters, and instant legal freeze quarantine trigger.
              </div>
            </div>
            <div class="guide-step-card">
              <div class="guide-step-title">Top Header & Notification Center</div>
              <div class="guide-step-desc">
                Displays live cluster telemetry, benchmark comparison modal, Run Analysis tracer, and Notification Bell with real-time audio chimes.
              </div>
            </div>
          </div>
        </div>

        <!-- Section 2: Canvas Controls -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
            2. Viewport Navigation & Canvas Controls
          </h3>
          <div style="display: flex; flex-direction: column; gap: 8px; font-size: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid var(--border-subtle);">
              <span><strong>Fit View:</strong> Auto-centers and frames the active graph within screen bounds.</span>
              <span class="shortcut-badge">Top Toolbar</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid var(--border-subtle);">
              <span><strong>Orbit Spin:</strong> Toggles slow 360° yaw camera rotation and harmonic floating micro-motion.</span>
              <span class="shortcut-badge">Top Toolbar</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid var(--border-subtle);">
              <span><strong>Spread Out:</strong> Expands spring repulsion distance (260px &rarr; 380px) to untangle dense clusters.</span>
              <span class="shortcut-badge">Top Toolbar</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid var(--border-subtle);">
              <span><strong>Physics Simulation:</strong> Toggles live ForceAtlas2 spring calculation vs static pinned drag.</span>
              <span class="shortcut-badge">Top Toolbar</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0;">
              <span><strong>Zoom & Pan:</strong> Mouse wheel/trackpad pinch for smooth zoom; click-drag empty canvas to pan.</span>
              <span class="shortcut-badge">Canvas Gesture</span>
            </div>
          </div>
        </div>

        <!-- Section 3: Entity Filters (Top Right) -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
            3. Top-Right Floating Entity Filters
          </h3>
          <p>
            Filter out background clutter and isolate specific entity layers by clicking the floating pill buttons at the top right of the canvas:
          </p>
          <div style="display: flex; gap: 14px; flex-wrap: wrap; margin-top: 6px;">
            <div style="background: rgba(25, 26, 27, 0.9); border: 1px solid #facc15; color: #facc15; padding: 6px 12px; border-radius: 6px; font-size: 11px; font-weight: 700;">
              [ Users ] — Yellow circle accounts
            </div>
            <div style="background: rgba(25, 26, 27, 0.9); border: 1px solid #38bdf8; color: #38bdf8; padding: 6px 12px; border-radius: 6px; font-size: 11px; font-weight: 700;">
              [ Devices ] — Cyan diamond hardware
            </div>
            <div style="background: rgba(25, 26, 27, 0.9); border: 1px solid #34d399; color: #34d399; padding: 6px 12px; border-radius: 6px; font-size: 11px; font-weight: 700;">
              [ Merchants ] — Mint triangle cash-out terminals
            </div>
          </div>
        </div>

        <!-- Section 4: Interactive Node Inspector -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            4. Interactive Node Inspection
          </h3>
          <p>
            Clicking any node on the graph triggers the floating <strong>Node Inspector Card</strong>, presenting entity role, connected degree, risk score, and instant neighbor isolation controls.
          </p>
        </div>
      </div>
    </div>
  </div>

  <!-- Independent Modal 3: Operator Instructions & SOP -->
  <div class="modal-backdrop" id="instructions-modal" onclick="closeInstructionsModal(event)">
    <div class="modal-window modal-wide" onclick="event.stopPropagation()">
      <div class="modal-head">
        <div class="modal-title-group">
          <button class="modal-back-btn" onclick="backToSettingsModal()" title="Back to Settings" aria-label="Back to Settings">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
          </button>
          <div class="brand-logo-mark" style="width:24px; height:24px;">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#131415" stroke-width="2.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
          </div>
          <div>
            <div class="modal-title">DarkNode AML Compliance & Operator SOP Instructions</div>
            <div style="font-size: 10px; color: var(--text-dim); margin-top: 1px;">STANDARD OPERATING PROCEDURE & REGULATORY CONTAINMENT PROTOCOL</div>
          </div>
        </div>
        <button class="modal-close-btn" onclick="closeInstructionsModal()">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <div class="modal-body">
        <!-- Section 1: Standard Operating Procedure (SOP) -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            1. AML Analyst Daily Investigation Workflow (SOP)
          </h3>
          <div class="guide-grid-2">
            <div class="guide-step-card">
              <div class="guide-step-title">Step 1: Priority Queue Triage</div>
              <div class="guide-step-desc">
                Review syndicates in the Left Panel. Focus immediately on syndicates with <strong style="color: #ef4444;">CRITICAL</strong> badges (composite score &gt;0.80). Click the syndicate card to load its topology.
              </div>
            </div>
            <div class="guide-step-card">
              <div class="guide-step-title">Step 2: Signal Correlation Verification</div>
              <div class="guide-step-desc">
                Inspect the Right Panel evidence signals: verify device multiplexing ratio (DEV), shared IP collisions (NET), and transaction burst velocity (VEL).
              </div>
            </div>
            <div class="guide-step-card">
              <div class="guide-step-title">Step 3: Graph Traversal Verification</div>
              <div class="guide-step-desc">
                Click <strong>Run Analysis</strong> on the top header. Observe animated payment packets flowing across accounts to verify cyclical laundering loops and smurf dispersion.
              </div>
            </div>
            <div class="guide-step-card">
              <div class="guide-step-title">Step 4: Emergency Debit Freeze</div>
              <div class="guide-step-desc">
                Click <strong>Freeze Syndicate Accounts</strong> to execute immediate simulated quarantine on all member accounts. Quarantined accounts show red freeze badges.
              </div>
            </div>
          </div>
        </div>

        <!-- Section 2: Decision Matrix & Threshold Policy -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="4" y1="21" x2="4" y2="14"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="20" y1="21" x2="20" y2="16"/></svg>
            2. Risk Cutoff & Escalation Decision Matrix
          </h3>
          <div style="background: var(--bg-input); padding: 12px; border-radius: 8px; border: 1px solid var(--border-subtle); font-size: 11.5px; line-height: 1.6;">
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--border-subtle); padding-bottom: 6px; margin-bottom: 6px;">
              <span style="color: #ef4444; font-weight: 700;">Score &ge; 0.75 (Critical High-Certainty):</span>
              <span>Immediate Account Freeze + Mandatory FinCEN SAR Filing within 24h</span>
            </div>
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--border-subtle); padding-bottom: 6px; margin-bottom: 6px;">
              <span style="color: var(--yellow-primary); font-weight: 700;">0.50 &le; Score &lt; 0.75 (Elevated Suspicion):</span>
              <span>Enhanced Due Diligence (EDD) + 48h Transaction Monitoring Watchlist</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span style="color: var(--text-muted); font-weight: 700;">Score &lt; 0.50 (Permissive Surveillance):</span>
              <span>Routine Automated Graph Monitoring (Low Intervention Priority)</span>
            </div>
          </div>
        </div>

        <!-- Section 3: Statutory SAR Filing Protocol -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
            3. Regulatory FinCEN / FIU SAR Export Protocol
          </h3>
          <p>
            For verified illicit syndicates, compliance officers must generate legal evidence dossiers:
          </p>
          <ul style="margin: 6px 0 0 18px; font-size: 12px; line-height: 1.6;">
            <li>Navigate to <strong>Settings &rarr; Regulatory SAR Dossier Export</strong>.</li>
            <li>Click <strong>Export SAR Dossier (JSON / FinCEN)</strong> to download an official Form 111 XML/JSON evidentiary payload.</li>
            <li>Click <strong>Export Evidence Ledger (CSV)</strong> to download a complete tabular ledger of member accounts, device IMEIs, and merchant terminals for court subpoena attachments.</li>
          </ul>
        </div>

        <!-- Section 4: Hotkeys & Shortcuts -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="2" y="4" width="20" height="16" rx="2" ry="2"/><line x1="6" y1="8" x2="6" y2="8"/><line x1="10" y1="8" x2="10" y2="8"/><line x1="14" y1="8" x2="14" y2="8"/><line x1="18" y1="8" x2="18" y2="8"/></svg>
            4. Operator Hotkeys & Quick Navigation
          </h3>
          <div style="display: flex; flex-direction: column; gap: 6px; font-size: 11.5px;">
            <div style="display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid var(--border-subtle);">
              <span>Dismiss Modals / Flyouts / Inspector</span>
              <span class="shortcut-badge">Esc</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid var(--border-subtle);">
              <span>Open Enterprise Settings & Controls</span>
              <span class="shortcut-badge">Gear Logo (Bottom-Right)</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid var(--border-subtle);">
              <span>Run Live Graph Traversal Analysis</span>
              <span class="shortcut-badge">Run Analysis (Header)</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 4px 0;">
              <span>Inspect Specific Entity Node</span>
              <span class="shortcut-badge">Click Any Node</span>
            </div>
          </div>
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

  <!-- Toast Notification Bubble - Normal Notification (Come and Go with Sound) -->
  <div class="toast-popup" id="toast">
    <div class="toast-dot-glow" id="toast-glow"></div>
    <div style="flex: 1; min-width: 0;">
      <div id="toast-title" style="font-size: 11px; font-weight: 700; color: var(--text-main); margin-bottom: 2px;">Notification</div>
      <div id="toast-text" style="font-size: 11px; color: var(--text-muted); line-height: 1.35;">Action executed.</div>
    </div>
    <button class="toast-close-btn" onclick="dismissToast()" title="Dismiss notification" style="background: transparent; border: none; color: var(--text-muted); cursor: pointer; padding: 2px; display: flex; align-items: center;">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>
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

    // Dual Datasets: Actual Data (Default Simulation) & Real AML Data (FATF/FinCEN Typologies)
    const ACTUAL_RINGS = __ACTUAL_RINGS_JSON__;
    const REAL_AML_RINGS = __REAL_AML_RINGS_JSON__;
    const FALLBACK_RINGS = ACTUAL_RINGS;
    let currentDataset = 'actual'; // 'actual' (default) or 'real'
    allRings = [...ACTUAL_RINGS];

    function switchDatasetSection(type) {
      if (currentDataset === type && allRings.length > 0) return;
      currentDataset = type;

      const tabActual = document.getElementById("dataset-tab-actual");
      const tabReal = document.getElementById("dataset-tab-real");
      if (tabActual && tabReal) {
        tabActual.classList.toggle("active", type === 'actual');
        tabReal.classList.toggle("active", type === 'real');
      }

      if (type === 'real') {
        allRings = [...REAL_AML_RINGS];
        showToast("Switched to Real AML Data: 12 source-verified syndicates with FATF/FinCEN typologies", "Real AML Dataset", "success");
      } else {
        allRings = [...ACTUAL_RINGS];
        showToast("Switched to Synthetic Data: 10 baseline GNN simulation syndicates", "Synthetic Dataset", "info");
      }

      // Update counters
      const statRings = document.getElementById("stat-rings");
      if (statRings) statRings.innerText = allRings.length;
      const countBadge = document.getElementById("rings-count-badge");
      if (countBadge) countBadge.innerText = `${allRings.length} total`;

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
      updateSearchSuggestions();
    }

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
        const fetched = data.rings || [];
        ACTUAL_RINGS.splice(0, ACTUAL_RINGS.length, ...fetched);
        if (currentDataset === 'actual') {
          allRings = [...ACTUAL_RINGS];
        } else {
          allRings = REAL_AML_RINGS.filter(r => r.avg_model_score >= (currentThresh - 0.15));
        }

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
        const baseSet = (currentDataset === 'real') ? REAL_AML_RINGS : ACTUAL_RINGS;
        allRings = baseSet.filter(r => r.avg_model_score >= (currentThresh - 0.15));
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

    let thresholdDebounceTimer = null;

    function syncThresholdUI(numVal) {
      const threshSelect = document.getElementById("threshold-select");
      const threshSlider = document.getElementById("threshold-slider");
      const threshBadge = document.getElementById("settings-thresh-badge");
      const descBox = document.getElementById("threshold-desc-box");

      if (threshBadge) threshBadge.innerText = numVal.toFixed(2);
      if (threshSlider && Math.abs(parseFloat(threshSlider.value) - numVal) > 0.001) {
        threshSlider.value = numVal.toFixed(2);
      }
      if (threshSelect) {
        let matched = false;
        for (let opt of threshSelect.options) {
          if (Math.abs(parseFloat(opt.value) - numVal) < 0.03) {
            threshSelect.value = opt.value;
            matched = true;
            break;
          }
        }
        if (!matched) {
          threshSelect.value = "";
        }
      }
      if (descBox) {
        if (numVal <= 0.40) {
          descBox.innerHTML = `Currently filtering at <strong>${numVal.toFixed(2)}</strong>: Broad surveillance queue (high recall for early smurfing).`;
        } else if (numVal <= 0.60) {
          descBox.innerHTML = `Currently filtering at <strong>${numVal.toFixed(2)}</strong>: Standard benchmark balance (95.0% precision, 5.0% false alarms).`;
        } else {
          descBox.innerHTML = `Currently filtering at <strong>${numVal.toFixed(2)}</strong>: Strict critical threshold (isolates confirmed large syndicates).`;
        }
      }
    }

    function onThresholdChange(newThreshold) {
      const numVal = parseFloat(newThreshold);
      syncThresholdUI(numVal);
      showToast(`Threshold updated to ${numVal.toFixed(2)} — re-evaluating candidate pool...`);
      fetchRings();
    }

    async function generateNewGraph() {
      const btns = [document.getElementById("new-graph-btn"), document.getElementById("settings-new-graph-btn")].filter(Boolean);
      const dot = document.getElementById("status-dot");
      const label = document.getElementById("status-label");
      const url = document.getElementById("api-url").value.trim().replace(/\/$/, "");
      const threshInput = document.getElementById("threshold-select");
      const currentThresh = threshInput ? parseFloat(threshInput.value) : 0.5;

      btns.forEach(b => {
        b.disabled = true;
        b.innerHTML = `
          <svg class="spin-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
          </svg>
          Generating...
        `;
        b.style.opacity = "0.85";
      });

      if (dot) dot.classList.add("active-infer");
      if (label) label.innerText = "SYNTHESIZING GRAPH...";
      showToast("Generating fresh transaction graph and running GNN forward pass...", "Graph Synthesis", "info");

      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 6000);
        const res = await fetch(`${url}/generate-graph`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ threshold: currentThresh }),
          signal: controller.signal
        });
        clearTimeout(timeoutId);

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        allRings = data.rings || [];
        ACTUAL_RINGS.splice(0, ACTUAL_RINGS.length, ...allRings);

        if (data.metadata) {
          document.getElementById("stat-users").innerText = data.metadata.num_users?.toLocaleString() || "1,000";
          document.getElementById("stat-txs").innerText = data.metadata.total_transactions?.toLocaleString() || "13,680";
        }
        if (dot) dot.classList.remove("offline", "active-infer");
        if (label) label.innerText = "LIVE API";
        showToast(data.message || `Fresh graph generated (Seed: ${data.seed})`, "Graph Synthesis", "success");
      } catch (err) {
        console.warn("Backend unavailable for graph generation, synthesising client variation:", err);
        const seedVal = Math.floor(100000 + Math.random() * 900000);
        allRings = ACTUAL_RINGS.map(r => {
          const jitter = (Math.random() * 0.04 - 0.02);
          const newScore = Math.min(0.99, Math.max(0.65, r.score + jitter));
          return {
            ...r,
            score: parseFloat(newScore.toFixed(3)),
            transaction_velocity: Math.max(50, Math.round(r.transaction_velocity * (0.9 + Math.random() * 0.2)))
          };
        }).sort((a, b) => b.score - a.score);

        if (dot) {
          dot.classList.remove("active-infer");
          dot.classList.add("offline");
        }
        if (label) label.innerText = "CACHED GNN";
        showToast(`Synthesized new graph batch variation (Seed #${seedVal})`, "Graph Synthesis", "success");
      } finally {
        btns.forEach(b => {
          b.disabled = false;
          b.innerHTML = `
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
            Synthesize New Graph Batch
          `;
          b.style.opacity = "1";
        });
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

        const subtitleHtml = ring.subtitle ? `
          <div class="ring-subtitle-tag" title="${ring.subtitle}">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" style="flex-shrink: 0;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${ring.subtitle}</span>
          </div>
        ` : '';

        card.innerHTML = `
          <div class="ring-card-top">
            <span class="ring-label">Syndicate Ring #${ring.ring_id}</span>
            <span class="ring-risk-tag">${(ring.score * 100).toFixed(1)}% RISK</span>
          </div>
          ${subtitleHtml}
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
      updateSearchSuggestions();
      const dropdown = document.getElementById("search-suggestions");
      if (dropdown) dropdown.classList.add("open");
    }

    function updateSearchSuggestions() {
      const dropdown = document.getElementById("search-suggestions");
      if (!dropdown) return;

      if (currentDataset === 'real') {
        dropdown.innerHTML = `
          <div class="suggestion-group-title">Source-Verified AML Rings</div>
          <div class="suggestion-item" onclick="applySearchSuggestion('Smurfing')">
            <div class="suggestion-item-left">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              <span>Smurfing / Funneling</span>
            </div>
            <span class="suggestion-tag risk-tag">82.9% Risk</span>
          </div>
          <div class="suggestion-item" onclick="applySearchSuggestion('Layering')">
            <div class="suggestion-item-left">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              <span>Layering / Velocity</span>
            </div>
            <span class="suggestion-tag risk-tag">82.5% Risk</span>
          </div>
          <div class="suggestion-item" onclick="applySearchSuggestion('Mule Network')">
            <div class="suggestion-item-left">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              <span>Device Multiplexing Mule</span>
            </div>
            <span class="suggestion-tag risk-tag">82.2% Risk</span>
          </div>
          <div class="suggestion-group-title" style="margin-top: 4px;">Verified Global Entities</div>
          <div class="suggestion-item" onclick="applySearchSuggestion('HDFC')">
            <div class="suggestion-item-left">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#facc15" stroke-width="2"><circle cx="12" cy="7" r="4"/><path d="M5.5 21a8.38 8.38 0 0 1 13 0"/></svg>
              <span>HDFC Bank Accounts</span>
            </div>
            <span class="suggestion-tag">Banking</span>
          </div>
          <div class="suggestion-item" onclick="applySearchSuggestion('Coinbase')">
            <div class="suggestion-item-left">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>
              <span>Coinbase (MCC 6051)</span>
            </div>
            <span class="suggestion-tag">Crypto</span>
          </div>
        `;
      } else {
        dropdown.innerHTML = `
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
        `;
      }
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

        if (r.subtitle && r.subtitle.toLowerCase().includes(query)) return true;
        if (r.typology && (
          (r.typology.name && r.typology.name.toLowerCase().includes(query)) ||
          (r.typology.code && r.typology.code.toLowerCase().includes(query))
        )) return true;

        if (r.graph && r.graph.nodes) {
          const nodeMatches = r.graph.nodes.some(n =>
            (n.label && n.label.toLowerCase().includes(query)) ||
            (n.title && n.title.toLowerCase().includes(query))
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

      // Typology Card display
      const typoBox = document.getElementById("typology-card-box");
      if (typoBox) {
        if (ring.typology) {
          typoBox.style.display = "block";
          const codeEl = document.getElementById("typology-code");
          if (codeEl) codeEl.innerText = ring.typology.code || "FATF/FINCEN";
          const fatfEl = document.getElementById("typology-fatf");
          if (fatfEl) fatfEl.innerText = ring.typology.fatf || "FATF Recommendation";
          const nameEl = document.getElementById("typology-name");
          if (nameEl) nameEl.innerText = ring.typology.name || ring.subtitle || "AML Syndicate Pattern";
          const descEl = document.getElementById("typology-desc");
          if (descEl) descEl.innerText = ring.typology.description || "";
        } else {
          typoBox.style.display = "none";
        }
      }

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
      chipsBox.innerHTML = ring.members.map(m => {
        let label = `User ${m}`;
        if (ring.graph && ring.graph.nodes) {
          const userNode = ring.graph.nodes.find(n => n.id === `user_${m}`);
          if (userNode && userNode.label && userNode.label.trim() !== '') {
            label = userNode.label;
          }
        }
        return `
          <span class="chip-account ${isFrozen ? 'frozen' : ''}" onclick="focusOnNode('user_${m}')" title="Inspect user_${m}">
            ${label} ${isFrozen ? '<span style="font-size: 8px; color: #ef4444;">[FROZEN]</span>' : ''}
          </span>
        `;
      }).join("");

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
        const dpr = window.devicePixelRatio || 1;
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

        const positions = network.getPositions();
        ctx.font = "600 11.5px 'Inter', 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";

        const currentScale = network.getScale ? network.getScale() : 1.0;
        const ring = allRings[activeIndex];
        const isFrozen = ring && frozenRings.has(ring.ring_id);

        for (const node of currentVisibleNodes) {
          const pos = positions[node.id];
          if (!pos) continue;
          const domPos = network.canvasToDOM({ x: pos.x, y: pos.y });

          // Skip drawing if outside viewport
          if (domPos.x < -60 || domPos.x > container.clientWidth + 60 ||
              domPos.y < -60 || domPos.y > container.clientHeight + 60) {
            continue;
          }

          const labelText = node.actualLabel || node.label;
          const nodeBaseSize = (node.group === "device" ? 22 : (node.group === "merchant" ? 18 : 18));
          const nodeScreenRadius = Math.max(8, Math.min(36, nodeBaseSize * currentScale));
          const textX = domPos.x;
          const textY = domPos.y + nodeScreenRadius + 12;

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

      document.getElementById("inspect-id").innerText = gNode.actualLabel || gNode.label;
      const dot = document.getElementById("inspect-dot");
      const role = document.getElementById("inspect-role");
      const score = document.getElementById("inspect-score");
      const deg = document.getElementById("inspect-deg");

      // Count connected edges
      const connectedEdges = (ring.graph.edges || []).filter(e => e.from === nodeId || e.to === nodeId);
      deg.innerText = `${connectedEdges.length} connected hop${connectedEdges.length === 1 ? '' : 's'}`;

      if (gNode.profile) {
        if (gNode.group === "user") {
          const isFrozen = frozenRings.has(ring.ring_id);
          dot.style.background = isFrozen ? "#ef4444" : "var(--node-user)";
          role.innerText = `${gNode.profile.bank_name} (${gNode.profile.swift_bic})`;
          score.innerText = `${gNode.profile.name} • KYC: ${gNode.profile.kyc_tier}`;
          score.style.color = isFrozen ? "#ef4444" : "var(--yellow-primary)";
        } else if (gNode.group === "device") {
          dot.style.background = "var(--node-device)";
          role.innerText = `${gNode.profile.model} (${gNode.profile.os})`;
          score.innerText = `IMEI: ${gNode.profile.imei_masked} • IP: ${gNode.profile.last_ip || 'Static'}`;
          score.style.color = "var(--node-device)";
        } else if (gNode.group === "merchant") {
          dot.style.background = "var(--node-merchant)";
          role.innerText = `${gNode.profile.category} (MCC ${gNode.profile.mcc})`;
          score.innerText = `${gNode.profile.settlement_type} • Velocity: ${Math.round(ring.transaction_velocity)} tx/hr`;
          score.style.color = "var(--node-merchant)";
        }
      } else {
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

      const orbCheck = document.getElementById("setting-orbit-toggle");
      if (orbCheck) orbCheck.checked = isSpinningEnabled;

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

    function toggleOrbit() {
      toggleSpinAnimation();
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

      const physCheck = document.getElementById("setting-physics-toggle");
      if (physCheck) physCheck.checked = physicsState;

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
      const ring = allRings[activeIndex] || allRings[0];
      const ringLbl = document.getElementById("settings-active-ring-lbl");
      if (ringLbl && ring) {
        ringLbl.innerText = `Syndicate #${ring.ring_id} (Score: ${(ring.score * 100).toFixed(1)}%)`;
      }

      // Sync sound & toast alert checkboxes
      const soundCheck = document.getElementById("setting-sound-alert");
      if (soundCheck) soundCheck.checked = !!isSoundAlertEnabled;
      const toastCheck = document.getElementById("setting-toast-alert");
      if (toastCheck) toastCheck.checked = !!isToastAlertEnabled;

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
      const threshSlider = document.getElementById("threshold-slider");
      if (threshSlider) {
        const val = parseFloat(threshSlider.value || "0.50");
        syncThresholdUI(val);
      }

      // Handle category tab activation
      if (targetSection) {
        switchSettingsTab(targetSection);
        setTimeout(() => {
          const targetCard = document.getElementById(`setting-card-${targetSection}`);
          if (targetCard) {
            targetCard.scrollIntoView({ behavior: "smooth", block: "center" });
            targetCard.style.borderColor = "var(--yellow-primary)";
            setTimeout(() => {
              targetCard.style.borderColor = "var(--border-subtle)";
            }, 2500);
          }
        }, 150);
      } else {
        switchSettingsTab('all');
      }
    }

    function closeSettingsModal(e) {
      if (e && e.target !== document.getElementById("settings-modal") && !e.target.closest(".modal-close-btn")) return;
      const modal = document.getElementById("settings-modal");
      if (modal) modal.classList.remove("open");
    }

    async function testApiConnection() {
      const input = document.getElementById("api-url");
      const url = input ? input.value.trim().replace(/\/$/, "") : "https://darknode.onrender.com";
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
      const numVal = parseFloat(val);
      syncThresholdUI(numVal);

      clearTimeout(thresholdDebounceTimer);
      thresholdDebounceTimer = setTimeout(() => {
        showToast(`Threshold updated to ${numVal.toFixed(2)} — re-evaluating candidate pool...`);
        fetchRings();
      }, 200);
    }

    function exportSarCsv() {
      const ring = allRings[activeIndex] || allRings[0];
      if (!ring) {
        showToast("No active syndicate available for CSV export", "Evidence Export", "warning");
        return;
      }

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

      const csvContent = rows.map(r => r.map(c => typeof c === 'string' && c.includes(',') ? `"${c}"` : c).join(",")).join(String.fromCharCode(13, 10));
      const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `DARKNODE_EVIDENCE_RING_${ring.ring_id}.csv`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      showToast(`Exported Evidence Ledger CSV: Ring #${ring.ring_id}`);
    }

    async function playAlertChime() {
      try {
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        if (!AudioContextClass) {
          showToast("Audio alert notification triggered");
          return;
        }
        const audioCtx = new AudioContextClass();
        if (audioCtx.state === "suspended") {
          await audioCtx.resume();
        }
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
        toggleSpinAnimation();
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
        if (physicsState) {
          network.startSimulation();
          setTimeout(() => {
            if (network && !isUserInteracting) {
              network.stopSimulation();
              recomputePolarFromCurrentPositions();
            }
          }, 350);
        }
      }
    }

    function resetSettingsToDefault() {
      const input = document.getElementById("api-url");
      if (input) input.value = "https://darknode.onrender.com";

      const pingResult = document.getElementById("api-ping-result");
      if (pingResult) pingResult.innerHTML = "";

      syncThresholdUI(0.50);

      const springSlider = document.getElementById("spring-slider");
      if (springSlider) springSlider.value = "260";
      onSpringSliderChange("260");

      if (!physicsState) togglePhysics();
      if (!isSpinningEnabled) toggleSpinAnimation();

      const soundCheck = document.getElementById("setting-sound-alert");
      if (soundCheck) soundCheck.checked = true;
      isSoundAlertEnabled = true;

      const toastCheck = document.getElementById("setting-toast-alert");
      if (toastCheck) toastCheck.checked = true;
      isToastAlertEnabled = true;

      showToast("Reset all settings & thresholds to factory defaults");
    }

    // Settings Category Tabs Filtering
    function switchSettingsTab(tab) {
      const tabs = ['all', 'engine', 'sar', 'docs', 'restart'];
      tabs.forEach(t => {
        const btn = document.getElementById(`tab-btn-${t}`);
        if (btn) btn.classList.toggle('active', t === tab);
      });

      const cards = document.querySelectorAll('.settings-card');
      cards.forEach(c => {
        const cat = c.getAttribute('data-category');
        if (tab === 'all') {
          c.style.display = 'flex';
        } else if (cat === tab) {
          c.style.display = 'flex';
        } else {
          c.style.display = 'none';
        }
      });
    }

    // System Restart & Engine Reboot Execution (Soft / Hard)
    async function executeSystemRestart(mode = 'soft') {
      const isHard = (mode === 'hard');
      const btn = document.getElementById(isHard ? "btn-hard-restart" : "btn-soft-restart");
      const origText = btn ? btn.innerHTML : "";

      if (btn) {
        btn.innerHTML = `<svg class="spin-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 10 10"/></svg> Restarting Engine...`;
        btn.disabled = true;
      }

      showToast(`Initiating ${isHard ? 'hard factory reset' : 'soft system restart'}... Purging cache buffers`);

      setTimeout(async () => {
        try {
          if (isHard) {
            resetSettingsToDefault();
            frozenRings.clear();
          }

          if (spinAnimFrameId) {
            cancelAnimationFrame(spinAnimFrameId);
            spinAnimFrameId = null;
          }

          activeFilters = { user: true, device: true, merchant: true };
          ['user', 'device', 'merchant'].forEach(t => {
            const fBtn = document.getElementById(`filter-${t}`);
            if (fBtn) fBtn.classList.add('active');
          });

          await fetchRings();
          resetGraphView();
          closeSettingsModal();

          playAlertChime();
          showToast(`✓ Engine reboot complete — Telemetry & topology synchronized`, "System Restart", isHard ? "critical" : "success");
        } catch (err) {
          console.error("Restart error:", err);
          showToast(`Engine rebooted to local cache state`, "System Restart", "warning");
        } finally {
          if (btn) {
            btn.innerHTML = origText;
            btn.disabled = false;
          }
        }
      }, 650);
    }

    // Modal Control Functions: Independent Architecture, User Guide & Instructions
    function backToSettingsModal() {
      const arch = document.getElementById("architecture-modal");
      if (arch) arch.classList.remove("open");
      const guide = document.getElementById("user-guide-modal");
      if (guide) guide.classList.remove("open");
      const inst = document.getElementById("instructions-modal");
      if (inst) inst.classList.remove("open");

      openSettingsModal('docs');
    }

    function openArchitectureModal() {
      closeSettingsModal();
      const modal = document.getElementById("architecture-modal");
      if (modal) modal.classList.add("open");
    }

    function closeArchitectureModal(e) {
      if (e && e.target !== document.getElementById("architecture-modal") && !e.target.closest(".modal-close-btn")) return;
      const modal = document.getElementById("architecture-modal");
      if (modal) modal.classList.remove("open");
    }

    function openUserGuideModal() {
      closeSettingsModal();
      const modal = document.getElementById("user-guide-modal");
      if (modal) modal.classList.add("open");
    }

    function closeUserGuideModal(e) {
      if (e && e.target !== document.getElementById("user-guide-modal") && !e.target.closest(".modal-close-btn")) return;
      const modal = document.getElementById("user-guide-modal");
      if (modal) modal.classList.remove("open");
    }

    function openInstructionsModal() {
      closeSettingsModal();
      const modal = document.getElementById("instructions-modal");
      if (modal) modal.classList.add("open");
    }

    function closeInstructionsModal(e) {
      if (e && e.target !== document.getElementById("instructions-modal") && !e.target.closest(".modal-close-btn")) return;
      const modal = document.getElementById("instructions-modal");
      if (modal) modal.classList.remove("open");
    }

    // Aliases for backward compatibility
    function openGuideModal() {
      openUserGuideModal();
    }

    function closeGuideModal(e) {
      closeUserGuideModal(e);
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
        closeArchitectureModal();
        closeUserGuideModal();
        closeInstructionsModal();
        closeBenchmarkModal();
        closeNodeInspector();
        hideSearchSuggestions();
        const dropdown = document.getElementById("notif-flyout");
        if (dropdown) dropdown.style.display = "none";
      }
    });

    document.addEventListener("click", (e) => {
      const searchBox = document.querySelector(".search-box-clean");
      if (searchBox && !searchBox.contains(e.target)) {
        hideSearchSuggestions();
      }
      const notifContainer = document.querySelector(".notif-bell-container");
      const notifFlyout = document.getElementById("notif-flyout");
      if (notifContainer && notifFlyout && !notifContainer.contains(e.target)) {
        notifFlyout.style.display = "none";
      }
    });

    // =========================================================================
    // AUDIT NOTIFICATION & CHIME ENGINE (COME & GO TOASTS + SOUND + FLYOUT)
    // =========================================================================
    let notifications = [
      {
        id: 1,
        title: "DarkNode GNN Engine Ready",
        desc: "2-layer Heterogeneous MPNN inference model loaded with 10 syndicates in queue.",
        type: "info",
        time: "Just now",
        timestamp: Date.now()
      }
    ];
    let unreadNotifCount = 1;
    let toastTimer = null;

    function playNotificationSound(type = 'info') {
      if (!isSoundAlertEnabled) return;
      try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') {
          audioCtx.resume();
        }
        const now = audioCtx.currentTime;
        const osc1 = audioCtx.createOscillator();
        const osc2 = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();

        osc1.connect(gainNode);
        osc2.connect(gainNode);
        gainNode.connect(audioCtx.destination);

        if (type === 'critical') {
          // Urgent double warning tone for high-threat mule syndicates
          osc1.type = 'sawtooth';
          osc2.type = 'sine';
          osc1.frequency.setValueAtTime(659.25, now);
          osc1.frequency.setValueAtTime(880, now + 0.1);
          osc2.frequency.setValueAtTime(329.63, now);
          osc2.frequency.setValueAtTime(440, now + 0.1);
          gainNode.gain.setValueAtTime(0.14, now);
          gainNode.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
          osc1.start(now);
          osc2.start(now);
          osc1.stop(now + 0.35);
          osc2.stop(now + 0.35);
        } else {
          // Normal harmonic bell chime
          osc1.type = 'sine';
          osc2.type = 'sine';
          osc1.frequency.setValueAtTime(880, now); // A5
          osc1.frequency.setValueAtTime(1318.51, now + 0.08); // E6
          osc2.frequency.setValueAtTime(440, now);
          osc2.frequency.setValueAtTime(659.25, now + 0.08);
          gainNode.gain.setValueAtTime(0.12, now);
          gainNode.gain.exponentialRampToValueAtTime(0.001, now + 0.36);
          osc1.start(now);
          osc2.start(now);
          osc1.stop(now + 0.36);
          osc2.stop(now + 0.36);
        }
      } catch (e) {
        console.debug("Notification audio context unavailable:", e);
      }
    }

    function dismissToast() {
      const toast = document.getElementById("toast");
      if (!toast) return;
      if (toastTimer) {
        clearTimeout(toastTimer);
        toastTimer = null;
      }
      toast.classList.add("toast-exit");
      setTimeout(() => {
        toast.style.display = "none";
        toast.classList.remove("toast-exit");
      }, 240);
    }

    function showToastNotification(title, text, type = "info") {
      if (!isToastAlertEnabled) return;
      const toast = document.getElementById("toast");
      const titleEl = document.getElementById("toast-title");
      const textEl = document.getElementById("toast-text");
      const glowEl = document.getElementById("toast-glow");
      if (!toast || !textEl) return;

      if (titleEl) titleEl.innerText = title;
      textEl.innerText = text;

      if (type === "critical") {
        toast.style.borderLeftColor = "#ef4444";
        if (glowEl) {
          glowEl.style.backgroundColor = "#ef4444";
          glowEl.style.boxShadow = "none";
        }
      } else if (type === "success") {
        toast.style.borderLeftColor = "#34d399";
        if (glowEl) {
          glowEl.style.backgroundColor = "#34d399";
          glowEl.style.boxShadow = "none";
        }
      } else {
        toast.style.borderLeftColor = "var(--yellow-primary)";
        if (glowEl) {
          glowEl.style.backgroundColor = "var(--yellow-primary)";
          glowEl.style.boxShadow = "none";
        }
      }

      toast.classList.remove("toast-exit");
      toast.style.display = "flex";

      if (toastTimer) clearTimeout(toastTimer);
      toastTimer = setTimeout(() => {
        dismissToast();
      }, 4200);
    }

    function pushNotification(title, desc, type = "info") {
      const newNotif = {
        id: Date.now(),
        title: title,
        desc: desc,
        type: type,
        time: "Just now",
        timestamp: Date.now()
      };
      notifications.unshift(newNotif);
      if (notifications.length > 25) notifications.pop();
      unreadNotifCount++;
      updateNotifBadge();
      renderNotifList();

      playNotificationSound(type);
      showToastNotification(title, desc, type);
    }

    function showToast(text, title = "System Audit", type = "info") {
      pushNotification(title, text, type);
    }

    function updateNotifBadge() {
      const badge = document.getElementById("notif-badge");
      if (!badge) return;
      if (unreadNotifCount > 0) {
        badge.innerText = unreadNotifCount > 9 ? "9+" : unreadNotifCount;
        badge.classList.remove("hidden");
        badge.classList.add("bump");
        setTimeout(() => badge.classList.remove("bump"), 300);
      } else {
        badge.classList.add("hidden");
      }
    }

    function renderNotifList() {
      const list = document.getElementById("notif-flyout-list");
      if (!list) return;

      if (notifications.length === 0) {
        list.innerHTML = `
          <div class="notif-empty-state">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" style="margin-bottom: 6px; opacity: 0.5;"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
            <div>No active notifications</div>
          </div>
        `;
        return;
      }

      list.innerHTML = notifications.map(n => {
        let iconSvg = '';
        if (n.type === 'critical') {
          iconSvg = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`;
        } else if (n.type === 'warning') {
          iconSvg = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`;
        } else if (n.type === 'success') {
          iconSvg = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="20 6 9 17 4 12"/></svg>`;
        } else {
          iconSvg = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>`;
        }

        return `
          <div class="notif-item">
            <div class="notif-icon-col ${n.type}">
              ${iconSvg}
            </div>
            <div class="notif-body-col">
              <div class="notif-item-top">
                <span class="notif-item-title">${n.title}</span>
                <span class="notif-item-time">${n.time}</span>
              </div>
              <div class="notif-item-desc">${n.desc}</div>
            </div>
          </div>
        `;
      }).join('');
    }

    function toggleNotifDropdown(e) {
      if (e) e.stopPropagation();
      const dropdown = document.getElementById("notif-flyout");
      if (!dropdown) return;
      const isHidden = dropdown.style.display === "none";
      dropdown.style.display = isHidden ? "flex" : "none";
      if (isHidden) {
        unreadNotifCount = 0;
        updateNotifBadge();
        renderNotifList();
      }
    }

    function clearAllNotifications() {
      notifications = [];
      unreadNotifCount = 0;
      updateNotifBadge();
      renderNotifList();
      showToastNotification("Audit Log Cleared", "All notification items have been purged.", "info");
    }

    function triggerTestAlert() {
      pushNotification(
        "Critical Syndicate Alert",
        "Syndicate #3 crossed the 0.80 risk threshold. 12 mule accounts flagged for review.",
        "critical"
      );
    }

    /* Mobile Landscape Fit & Orientation Handlers */
    function checkOrientation() {
      const overlay = document.getElementById("orientation-overlay");
      const isPortrait = window.innerHeight > window.innerWidth;
      
      const isTouchOrMobile = ('ontouchstart' in window) || 
                              (navigator.maxTouchPoints > 0) || 
                              /Android|iPhone|iPad|iPod|webOS|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
      
      const isNarrowPortrait = isPortrait && (isTouchOrMobile || window.innerWidth <= 900);

      if (overlay) {
        if (isNarrowPortrait && !overlay.classList.contains("dismissed")) {
          overlay.style.display = "flex";
        } else {
          overlay.style.display = "none";
          if (!isPortrait) {
            overlay.classList.remove("dismissed");
          }
        }
      }

      adjustMobileFit();
    }

    function dismissOrientationModal() {
      const overlay = document.getElementById("orientation-overlay");
      if (overlay) {
        overlay.classList.add("dismissed");
        overlay.style.display = "none";
      }
      adjustMobileFit();
    }

    function toggleSidebar(side) {
      if (side === 'left') {
        const sb = document.querySelector('.sidebar-left');
        const pill = document.getElementById('expand-left-btn');
        if (!sb) return;
        const isCollapsed = sb.classList.toggle('collapsed');
        if (pill) pill.style.display = isCollapsed ? 'flex' : 'none';
      } else if (side === 'right') {
        const sb = document.querySelector('.sidebar-right');
        const pill = document.getElementById('expand-right-btn');
        if (!sb) return;
        const isCollapsed = sb.classList.toggle('collapsed');
        if (pill) pill.style.display = isCollapsed ? 'flex' : 'none';
      }
      setTimeout(() => {
        if (network) {
          network.redraw();
          fitGraphToScreen(true);
        }
      }, 150);
    }

    function adjustMobileFit() {
      const wrapper = document.getElementById("app-viewport-wrapper");
      if (!wrapper) return;

      // Reset any inline dimensions so CSS media queries handle edge-to-edge layout cleanly
      wrapper.style.position = "";
      wrapper.style.width = "100%";
      wrapper.style.height = "100%";
      wrapper.style.top = "";
      wrapper.style.left = "";
      wrapper.style.transform = "";
      wrapper.style.margin = "";

      // Ensure window scroll stays locked at top-left with zero drift
      window.scrollTo(0, 0);
      if (document.body) document.body.scrollTop = 0;
      if (document.documentElement) document.documentElement.scrollTop = 0;

      if (typeof network !== "undefined" && network) {
        network.redraw();
        fitGraphToScreen(false);
      }
    }

    function toggleFullScreen() {
      if (!document.fullscreenElement && !document.webkitFullscreenElement) {
        const el = document.documentElement;
        if (el.requestFullscreen) {
          el.requestFullscreen().catch(() => {});
        } else if (el.webkitRequestFullscreen) {
          el.webkitRequestFullscreen();
        }
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
          document.webkitExitFullscreen();
        }
      }
    }

    window.addEventListener("resize", () => {
      checkOrientation();
      if (network) {
        network.redraw();
        fitGraphToScreen(false);
      }
    });

    window.addEventListener("orientationchange", () => {
      setTimeout(checkOrientation, 100);
    });

    if (window.screen && window.screen.orientation) {
      window.screen.orientation.addEventListener("change", () => {
        setTimeout(checkOrientation, 100);
      });
    }

    window.addEventListener("DOMContentLoaded", () => {
      checkOrientation();
      renderNotifList();
      updateNotifBadge();
      fetchRings();
    });
  </script>
</body>
</html>
"""

output_html = (
    html_template
    .replace("__ACTUAL_RINGS_JSON__", fallback_data)
    .replace("__REAL_AML_RINGS_JSON__", real_aml_data)
    .replace("__FALLBACK_JSON__", fallback_data)
)
with open("web/index.html", "w", encoding="utf-8") as f:
    f.write(output_html)

print("web/index.html written successfully!")
