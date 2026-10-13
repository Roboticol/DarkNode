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
      /* Dark Slate & Charcoal Theme */
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
      color: #111215;
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
      background: rgba(24, 25, 30, 0.96);
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
      background: rgba(10, 11, 14, 0.82);
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
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#111215" stroke-width="2.5"><circle cx="12" cy="12" r="3"/><circle cx="19" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><line x1="12" y1="9" x2="19" y2="6.5"/><line x1="12" y1="15" x2="5" y2="17.5"/></svg>
      </div>
      <div class="brand-title">
        Dark <span class="kicker">Node</span>
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
          <div class="legend-dot" style="background: var(--node-merchant); border-radius: 2px;"></div>
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

  <!-- Interactive System & User Guide Modal -->
  <div class="modal-backdrop" id="guide-modal" onclick="closeGuideModal(event)">
    <div class="modal-window" onclick="event.stopPropagation()">
      <div class="modal-head">
        <div class="modal-title-group">
          <div class="brand-logo-mark" style="width:24px; height:24px;">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#111215" stroke-width="2.5"><circle cx="12" cy="12" r="3"/><circle cx="19" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><line x1="12" y1="9" x2="19" y2="6.5"/><line x1="12" y1="15" x2="5" y2="17.5"/></svg>
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

        <!-- Section 2: Dashboard Structure -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
            2. Dashboard Structure & Investigation Flow
          </h3>
          <div class="guide-grid-2">
            <div class="guide-step-card">
              <div class="guide-step-title">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
                Syndicate Directory (Left)
              </div>
              <div class="guide-step-desc">
                Lists all detected mule rings sorted by composite risk. Use the search bar to filter by Ring ID or User ID. Click any ring card to inspect its dedicated subgraph.
              </div>
            </div>

            <div class="guide-step-card">
              <div class="guide-step-title">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><circle cx="19" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><line x1="12" y1="9" x2="19" y2="6.5"/><line x1="12" y1="15" x2="5" y2="17.5"/></svg>
                Network Canvas (Center)
              </div>
              <div class="guide-step-desc">
                Interactive topological graph with high-contrast screen labels. Click any node to open the live Node Inspector.
              </div>
            </div>

            <div class="guide-step-card">
              <div class="guide-step-title">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                Syndicate Dossier (Right)
              </div>
              <div class="guide-step-desc">
                Reveals the 5 evidence signals (Shared Device %, Shared IP pairs, Burst Velocity, GNN Confidence, New Accounts). Click account chips to jump directly to any entity.
              </div>
            </div>

            <div class="guide-step-card">
              <div class="guide-step-title">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                Defense Simulation & Export
              </div>
              <div class="guide-step-desc">
                Simulate a one-click account suspension for incident drills or download the complete forensic evidence package in standard JSON format for audit compliance.
              </div>
            </div>
          </div>
        </div>

        <!-- Section 3: Navigation & Controls -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
            3. Canvas Navigation & Controls
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
              <span>Spread Out / Decluster</span>
              <div>Click <span class="shortcut-badge">Spread Out</span> on top canvas bar for open layout</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0;">
              <span>Entity Filters</span>
              <div>Toggle <span class="shortcut-badge">Users</span>, <span class="shortcut-badge">Devices</span>, or <span class="shortcut-badge">Merchants</span> to isolate subgraphs</div>
            </div>
          </div>
        </div>

        <!-- Section 4: Graph Visual Legend -->
        <div class="guide-section">
          <h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m9.17 14.83-4.24 4.24"/></svg>
            4. Graph Visual Legend
          </h3>
          <div style="display: flex; flex-wrap: wrap; gap: 18px; align-items: center; margin-top: 6px;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <div style="width: 12px; height: 12px; border-radius: 50%; background: #facc15;"></div>
              <span style="color: #f3f4f6; font-size: 12px;"><strong>User Node (Yellow)</strong>: Syndicate member account</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <div style="width: 12px; height: 12px; transform: rotate(45deg); background: #38bdf8;"></div>
              <span style="color: #f3f4f6; font-size: 12px;"><strong>Device Node (Cyan)</strong>: Shared hardware identifier</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <div style="width: 12px; height: 12px; clip-path: polygon(50% 0%, 0% 100%, 100% 100%); background: #34d399;"></div>
              <span style="color: #f3f4f6; font-size: 12px;"><strong>Merchant Node (Mint)</strong>: Shared high-velocity merchant</span>
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
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#111215" stroke-width="2.5"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
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

        <!-- Architectural Insights -->
        <div class="guide-section">
          <h3>
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            Why DarkNode Solves Rule-Based Heuristic Failure
          </h3>
          <p>
            Standard bank anti-money laundering (AML) rules fire on basic thresholds: e.g. <em>"Flag if multiple accounts use the same IP"</em> or <em>"Flag if 3+ transactions occur within an hour"</em>. This produces massive false positives whenever innocent people access university Wi-Fi, roommates share a device, or families shop during holiday sales.
          </p>
          <p>
            <strong>DarkNode's Heterogeneous GNN</strong> passes multi-hop message embeddings across the topology. Isolated shared devices without coordinated IP subnets and transaction burst graphs are recognized as benign clusters. Only tightly bound syndicates displaying concurrent multi-signal convergence reach high threat scores.
          </p>
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
    let inspectedNodeId = null;
    let frozenRings = new Set();

    // Real fallback dataset extracted from trained GNN model
    const FALLBACK_RINGS = __FALLBACK_JSON__;

    async function fetchRings() {
      const runBtn = document.getElementById("run-btn");
      const dot = document.getElementById("status-dot");
      const label = document.getElementById("status-label");
      const url = document.getElementById("api-url").value.trim().replace(/\\/$/, "");

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

      try {
        // Multi-step logic: Step 2 - Execute real PyTorch Geometric backend inference
        const res = await fetch(`${url}/analyze`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ top_k: 10, threshold: 0.5 })
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
        showToast(`GNN inference complete in ${elapsed}ms: ${allRings.length} syndicates ranked`);
      } catch (err) {
        console.warn("Backend unavailable, using cached model dossier:", err);
        allRings = FALLBACK_RINGS;
        dot.classList.remove("active-infer");
        dot.classList.add("offline");
        label.innerText = "CACHED GNN";
        showToast(`Loaded cached GNN model dossier (${allRings.length} rings)`);
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
      renderRingsList(allRings);
      if (allRings.length > 0) {
        const targetIdx = (activeIndex >= 0 && activeIndex < allRings.length) ? activeIndex : 0;
        selectRing(targetIdx, false);
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

    let currentRenderedRingId = null;

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

      // Handle freeze state for this ring
      const freezeBtn = document.getElementById("freeze-btn");
      const isFrozen = frozenRings.has(ring.ring_id);
      if (isFrozen) {
        freezeBtn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg> Accounts Suspended (Simulation)`;
        freezeBtn.disabled = true;
        freezeBtn.style.opacity = "0.7";
      } else {
        freezeBtn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg> Freeze Ring Accounts (Simulation)`;
        freezeBtn.disabled = false;
        freezeBtn.style.opacity = "1";
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
          enabled: physicsState,
          solver: "forceAtlas2Based",
          forceAtlas2Based: {
            gravitationalConstant: -460,
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
        }
      };

      if (network) network.destroy();
      network = new vis.Network(container, data, options);

      // Once layout stabilizes, fit perfectly to frame and stop simulation for zero jitter
      network.once("stabilizationIterationsDone", function() {
        network.fit({ animation: { duration: 350, easingFunction: "easeInOutQuad" } });
        network.stopSimulation();
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
          ctx.fillStyle = "rgba(17, 18, 22, 0.92)";
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

    function resetGraphView() {
      if (network) network.fit({ animation: { duration: 350, easingFunction: "easeInOutQuad" } });
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
            enabled: true,
            forceAtlas2Based: { springLength: currentSpringLength, gravitationalConstant: currentSpringLength === 380 ? -620 : -460 }
          }
        });
        network.startSimulation();
        setTimeout(() => {
          if (network) network.stopSimulation();
        }, 1200);
      }
    }

    function togglePhysics() {
      physicsState = !physicsState;
      const label = document.getElementById("physics-label");
      label.innerText = `Physics: ${physicsState ? 'On' : 'Off'}`;
      if (network) {
        if (physicsState) {
          network.setOptions({ physics: { enabled: true } });
          network.startSimulation();
        } else {
          network.stopSimulation();
          network.setOptions({ physics: { enabled: false } });
        }
      }
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
      showNodeInspector(nodeId);
    }

    function simulateFreeze() {
      const ring = allRings[activeIndex];
      if (!ring) return;
      frozenRings.add(ring.ring_id);

      const btn = document.getElementById("freeze-btn");
      btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg> Accounts Suspended (Simulation)`;
      btn.disabled = true;
      btn.style.opacity = "0.7";

      // Mark chips as frozen
      const chipsBox = document.getElementById("members-chips");
      chipsBox.innerHTML = ring.members.map(m => `
        <span class="chip-account frozen" onclick="focusOnNode('user_${m}')">
          User ${m} <span style="font-size: 8px; color: #ef4444;">[FROZEN]</span>
        </span>
      `).join("");

      // Update node styles in graph
      renderGraph(ring.graph);

      showToast(`Simulation: Suspended ${ring.member_count} syndicate accounts in Ring #${ring.ring_id} (Ref: #AML-SIM-${Date.now().toString().slice(-6)})`);
    }

    function exportJson() {
      const ring = allRings[activeIndex];
      if (!ring) return;
      const dossier = {
        ...ring,
        fincen_sar_metadata: {
          dossier_id: `DARKNODE-SAR-${ring.ring_id}-${Date.now().toString().slice(-6)}`,
          status: frozenRings.has(ring.ring_id) ? "SUSPENDED" : "DETECTED_ELEVATED",
          exported_at: new Date().toISOString(),
          gnn_architecture: "Heterogeneous MPNN 2-Layer"
        }
      };
      const blob = new Blob([JSON.stringify(dossier, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `darknode_syndicate_${ring.ring_id}.json`;
      a.click();
      URL.revokeObjectURL(url);
      showToast(`Exported Ring #${ring.ring_id} forensic dossier.`);
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
        closeGuideModal();
        closeBenchmarkModal();
        closeNodeInspector();
      }
    });

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
