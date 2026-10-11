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
  <!-- Ultra-sharp Professional Fonts: Inter with Tabular Figures -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

  <style>
    :root {
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      --font-mono: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace;

      /* Dark Grey Theme */
      --bg-base: #0f1013;
      --bg-panel: #16171c;
      --bg-card: #1e2027;
      --bg-card-hover: #262832;
      --bg-input: #121317;
      
      --border-subtle: #272a34;
      --border-strong: #383c4a;
      
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
      
      --shadow-card: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
      --shadow-glow: 0 0 16px rgba(250, 204, 21, 0.2);
      
      --radius: 10px;
      --radius-sm: 6px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: var(--font-sans);
      background-color: var(--bg-base);
      color: var(--text-main);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-rendering: optimizeLegibility;
      letter-spacing: -0.01em;
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

    .brand-title span.kicker {
      color: var(--yellow-primary);
    }

    .badge-pill {
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-size: 10px;
      font-weight: 700;
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

    @keyframes spin {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }

    .spin-icon {
      animation: spin 0.85s linear infinite;
      display: inline-flex;
      align-items: center;
      justify-content: center;
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
      transition: all 0.2s ease;
    }

    .stat-val {
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
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
      font-family: var(--font-sans);
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
      font-family: var(--font-sans);
      font-size: 10px;
      font-weight: 700;
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
      font-size: 13px;
      font-weight: 700;
      color: var(--text-main);
      letter-spacing: -0.01em;
    }

    /* Risk Tier Filters in Sidebar */
    .tier-filter-row {
      display: flex;
      gap: 5px;
      padding: 0 12px 10px 12px;
      border-bottom: 1px solid var(--border-subtle);
    }

    .tier-tab-btn {
      flex: 1;
      height: 25px;
      font-size: 10.5px;
      font-weight: 600;
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 3px;
    }

    .tier-tab-btn:hover {
      background: var(--bg-card-hover);
      color: var(--text-main);
      border-color: var(--border-strong);
    }

    .tier-tab-btn.active {
      background: var(--yellow-bg);
      border-color: var(--yellow-border);
      color: var(--yellow-primary);
      font-weight: 700;
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
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
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
      transition: all 0.2s ease;
    }

    .hero-score-val {
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-size: 32px;
      font-weight: 800;
      line-height: 1;
      color: var(--yellow-primary);
    }

    .hero-score-sub {
      font-size: 10px;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-top: 4px;
    }

    .hero-rank-badge {
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-size: 10px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 5px;
      background: var(--yellow-bg);
      color: var(--yellow-primary);
      border: 1px solid var(--yellow-border);
    }

    .block-title {
      font-size: 11.5px;
      font-weight: 700;
      color: var(--text-main);
      letter-spacing: -0.01em;
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
      font-family: var(--font-sans);
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
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
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
    @keyframes toastIn {
      from { opacity: 0; transform: translateY(12px) scale(0.96); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }

    @keyframes toastOut {
      from { opacity: 1; transform: translateY(0) scale(1); }
      to { opacity: 0; transform: translateY(10px) scale(0.96); }
    }

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

    .toast-popup.visible {
      display: flex;
      animation: toastIn 0.22s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    .toast-popup.closing {
      animation: toastOut 0.18s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    .toast-dot-glow {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--yellow-primary);
      box-shadow: 0 0 8px rgba(250, 204, 21, 0.8);
    }

    /* Interactive System & User Guide Modal */
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
      animation: modalFadeIn 0.18s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes modalFadeIn {
      from { opacity: 0; transform: scale(0.97) translateY(8px); }
      to { opacity: 1; transform: scale(1) translateY(0); }
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
      line-height: 1.2;
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
      font-family: var(--font-sans);
      font-size: 10px;
      font-weight: 700;
      background: var(--bg-input);
      border: 1px solid var(--border-strong);
      padding: 2px 6px;
      border-radius: 4px;
      color: var(--yellow-primary);
    }

    /* Signal Meters */
    .signal-meter-bg {
      width: 100%;
      height: 4px;
      background: rgba(255, 255, 255, 0.07);
      border-radius: 2px;
      overflow: hidden;
      margin-top: 3px;
    }

    .signal-meter-fill {
      height: 100%;
      background: var(--yellow-primary);
      border-radius: 2px;
      transition: width 0.65s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Floating Node Inspector */
    .node-inspector-card {
      position: absolute;
      bottom: 14px;
      right: 14px;
      width: 270px;
      background: rgba(24, 25, 30, 0.96);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-strong);
      border-radius: 10px;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6), var(--shadow-glow);
      z-index: 25;
      overflow: hidden;
      animation: inspectorSlideUp 0.18s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes inspectorSlideUp {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .node-inspector-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 9px 12px;
      background: var(--bg-card);
      border-bottom: 1px solid var(--border-subtle);
    }

    .node-inspector-title {
      font-family: var(--font-sans);
      font-size: 12px;
      font-weight: 700;
      color: var(--text-main);
    }

    .node-type-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--yellow-primary);
    }

    .node-close-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      padding: 3px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .node-close-btn:hover {
      background: var(--bg-card-hover);
      color: var(--yellow-primary);
    }

    .node-inspector-body {
      padding: 11px 12px;
      display: flex;
      flex-direction: column;
      gap: 7px;
    }

    .inspect-field {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
    }

    .inspect-lbl {
      color: var(--text-muted);
    }

    .inspect-val {
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-weight: 700;
      color: var(--text-main);
    }

    .inspect-actions {
      display: flex;
      gap: 6px;
      margin-top: 4px;
    }

    /* Benchmark Modal Styles */
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
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-size: 18px;
      font-weight: 700;
      color: var(--text-muted);
    }

    .bench-score-bright {
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
      font-size: 22px;
      font-weight: 800;
      color: var(--yellow-primary);
    }

    .bench-delta-tag {
      font-family: var(--font-sans);
      font-variant-numeric: tabular-nums;
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
      border-radius: 3px;
      transition: width 0.75s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .bench-bar-gnn {
      position: absolute;
      left: 0;
      top: 0;
      height: 100%;
      background: var(--yellow-primary);
      border-radius: 3px;
      box-shadow: 0 0 8px rgba(250, 204, 21, 0.5);
      transition: width 0.75s cubic-bezier(0.16, 1, 0.3, 1);
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
      <div class="api-box">
        <div class="status-dot" id="status-dot"></div>
        <input type="text" id="api-url" value="http://localhost:8000" placeholder="http://localhost:8000">
        <span class="status-text" id="status-label">ONLINE</span>
      </div>

      <button class="btn btn-outline" onclick="openBenchmarkModal()" title="View Empirical Model Benchmarks vs Bank Rules">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
        Benchmark
      </button>

      <button class="btn btn-outline" onclick="openGuideModal()" title="View System Architecture and Dashboard Operator Guide">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        User Guide
      </button>

      <button class="btn btn-yellow" id="analyze-btn" onclick="fetchRings()" title="Trigger Full Graph Neural Network Inference Analysis">
        <span id="analyze-icon"><svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg></span>
        <span id="analyze-text">Run Analysis</span>
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

      <!-- Risk Tier Filters (3 Tabs) -->
      <div class="tier-filter-row">
        <button class="tier-tab-btn active" id="tier-all" onclick="setTierFilter('all')">All (<span id="count-all">10</span>)</button>
        <button class="tier-tab-btn" id="tier-critical" onclick="setTierFilter('critical')">Critical (<span id="count-critical">10</span>)</button>
        <button class="tier-tab-btn" id="tier-elevated" onclick="setTierFilter('elevated')">Elevated (<span id="count-elevated">0</span>)</button>
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
        <button class="canvas-pill-btn" id="globe-mode-btn" onclick="toggleGlobeMode()" title="Rotate model manually like a 3D globe using cursor (click + drag horizontally or vertically)">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
          <span id="globe-mode-label">3D Globe: Off</span>
        </button>
        <button class="canvas-pill-btn" id="reset-globe-btn" onclick="resetGlobeView()" title="Reset 3D Globe orientation to default view" style="display: none;">
          Reset Globe
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

      <!-- Floating Node Inspector Card -->
      <div class="node-inspector-card" id="node-inspector" style="display: none;">
        <div class="node-inspector-head">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span class="node-type-dot" id="inspect-dot"></span>
            <span class="node-inspector-title" id="inspect-id">User 0</span>
          </div>
          <button class="node-close-btn" onclick="closeNodeInspector()">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>
        <div class="node-inspector-body">
          <div class="inspect-field">
            <span class="inspect-lbl">Entity Role</span>
            <span class="inspect-val" id="inspect-role">Syndicate Mule Account</span>
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
            <div class="signal-item-row" style="flex-direction: column; align-items: stretch; gap: 5px;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="signal-label-text"><span class="signal-prefix-tag">DEV</span>Shared Device Ratio</span>
                <span class="signal-metric-val" id="sig-device">0%</span>
              </div>
              <div class="signal-meter-bg"><div class="signal-meter-fill" id="meter-device" style="width: 0%;"></div></div>
            </div>
            <div class="signal-item-row" style="flex-direction: column; align-items: stretch; gap: 5px;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="signal-label-text"><span class="signal-prefix-tag">NET</span>Shared IP Pairs</span>
                <span class="signal-metric-val" id="sig-ip">0 pairs</span>
              </div>
              <div class="signal-meter-bg"><div class="signal-meter-fill" id="meter-ip" style="width: 0%;"></div></div>
            </div>
            <div class="signal-item-row" style="flex-direction: column; align-items: stretch; gap: 5px;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="signal-label-text"><span class="signal-prefix-tag">VEL</span>Burst Velocity</span>
                <span class="signal-metric-val" id="sig-vel">0 tx/hr</span>
              </div>
              <div class="signal-meter-bg"><div class="signal-meter-fill" id="meter-vel" style="width: 0%;"></div></div>
            </div>
            <div class="signal-item-row" style="flex-direction: column; align-items: stretch; gap: 5px;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="signal-label-text"><span class="signal-prefix-tag">GNN</span>Model Confidence</span>
                <span class="signal-metric-val" id="sig-gnn">0.00</span>
              </div>
              <div class="signal-meter-bg"><div class="signal-meter-fill" id="meter-gnn" style="width: 0%;"></div></div>
            </div>
            <div class="signal-item-row" style="flex-direction: column; align-items: stretch; gap: 5px;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="signal-label-text"><span class="signal-prefix-tag">NEW</span>New Accounts Ratio</span>
                <span class="signal-metric-val" id="sig-fresh">0</span>
              </div>
              <div class="signal-meter-bg"><div class="signal-meter-fill" id="meter-fresh" style="width: 0%;"></div></div>
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
          <div style="display: flex; gap: 6px;">
            <button class="btn btn-outline" style="height: 34px; flex: 1;" onclick="copySarSummary()" title="Copy Case Investigation Summary">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
              Copy SAR
            </button>
            <button class="btn btn-outline" style="height: 34px; flex: 1;" onclick="exportJson()" title="Download Complete JSON Forensic Dossier">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              Export JSON
            </button>
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

  <!-- Interactive System & User Guide Modal -->
  <div class="modal-backdrop" id="guide-modal" onclick="closeGuideModal(event)">
    <div class="modal-window" onclick="event.stopPropagation()">
      <div class="modal-head">
        <div class="modal-title-group">
          <div class="brand-logo-mark" style="width:24px; height:24px;">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#111215" stroke-width="2.5"><circle cx="12" cy="12" r="3"/><circle cx="19" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><line x1="12" y1="9" x2="19" y2="6.5"/><line x1="12" y1="15" x2="5" y2="17.5"/></svg>
          </div>
          <div class="modal-title">
            Dark<span style="color: var(--yellow-primary);">Node</span> Operator Guide & Architecture
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
            Mule accounts operate in organized syndicates where individual transactions appear benign. Traditional rule-based engines inspect transactions in isolation, resulting in high false alarms (<strong>58.1% of alerts were false positives</strong>, yielding only 41.9% precision) on common events like public Wi-Fi access or family-shared tablets.
          </p>
          <p>
            <strong>DarkNode</strong> implements a 2-layer Heterogeneous Graph Message Passing Neural Network (MPNN) over three entity types (<strong>Users</strong>, <strong>Devices</strong>, <strong>Merchants</strong>). By propagating structural graph embeddings across shared device fingerprints, IP subnet interconnections, and transaction velocity bursts, DarkNode elevates precision to <strong>95.0%</strong> (0.974 F1) and limits false alarms to just 5.0%.
          </p>
        </div>

        <!-- Section 2: Dashboard Walkthrough -->
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
                Real-time topological graph with constant 11px screen labels at any zoom level. Dynamic zoom condenses nodes when zooming out and spreads them freely when zooming in.
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
              <div><span class="shortcut-badge">Mouse Wheel</span> or <span class="shortcut-badge">Pinch Trackpad</span> (gentle, controlled zoom speed)</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid var(--border-subtle);">
              <span>Pan Viewport</span>
              <div><span class="shortcut-badge">Click + Drag</span> background canvas</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid var(--border-subtle);">
              <span>Focus Entity</span>
              <div><span class="shortcut-badge">Click Node</span> or <span class="shortcut-badge">Click User Chip</span> in dossier</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid var(--border-subtle);">
              <span>Spread Out / Decluster</span>
              <div>Click <span class="shortcut-badge">Spread Out</span> on top canvas bar for open layout</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid var(--border-subtle);">
              <span>3D Globe Rotation</span>
              <div>Click <span class="shortcut-badge">3D Globe: On</span> or hold <span class="shortcut-badge">Shift / Alt / Right-Click</span> and drag cursor horizontally/vertically</div>
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
            Dark<span style="color: var(--yellow-primary);">Node</span> Empirical Benchmark — GNN vs Bank Rules
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
              <div class="bench-bar-base" style="width: 41.9%;" data-width="41.9%"></div>
              <div class="bench-bar-gnn" style="width: 95.0%;" data-width="95.0%"></div>
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
              <div class="bench-bar-base" style="width: 58.1%; background: #ef4444;" data-width="58.1%"></div>
              <div class="bench-bar-gnn" style="width: 5.0%; background: #34d399;" data-width="5.0%"></div>
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
              <div class="bench-bar-base" style="width: 59.1%;" data-width="59.1%"></div>
              <div class="bench-bar-gnn" style="width: 97.4%;" data-width="97.4%"></div>
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
    let currentTierFilter = 'all';
    let inspectedNodeId = null;

    // =========================================================================
    // BUTTERY-SMOOTH 3D GLOBE TRACKBALL (60-120 FPS ZERO LAG)
    // =========================================================================
    let currentNodesDataSet = null;
    let baseNodes3D = {}; // { id: { x0: number, y0: number, z0: number, origSize: number } }
    let currentGraphCentroid = { x: 0, y: 0 };
    let currentYaw = 0; // Horizontal rotation around Y-axis (radians)
    let currentPitch = 0; // Vertical rotation around X-axis (radians)
    let targetYaw = 0;
    let targetPitch = 0;
    let globeModeActive = false;
    let isGlobeDragging = false;
    let dragStartX = 0;
    let dragStartY = 0;
    let dragStartYaw = 0;
    let dragStartPitch = 0;
    let globeRafPending = false;
    let analysisFaceAngle = 0;
    let morphRafId = null;

    function calculateCentroid(positions) {
      let sumX = 0, sumY = 0, count = 0;
      for (const id in positions) {
        if (positions[id]) {
          sumX += positions[id].x;
          sumY += positions[id].y;
          count++;
        }
      }
      return count > 0 ? { x: sumX / count, y: sumY / count } : { x: 0, y: 0 };
    }

    function setup3DCoordinates(positions) {
      baseNodes3D = {};
      currentGraphCentroid = calculateCentroid(positions);
      currentYaw = 0;
      currentPitch = 0;
      targetYaw = 0;
      targetPitch = 0;
      updateGlobeIndicator();

      const ids = Object.keys(positions);
      if (ids.length === 0) return;

      // Find max radius from centroid
      let maxDist = 0;
      for (const id of ids) {
        const p = positions[id];
        const dist = Math.hypot(p.x - currentGraphCentroid.x, p.y - currentGraphCentroid.y);
        if (dist > maxDist) maxDist = dist;
      }
      const globeRadius = Math.max(160, maxDist * 1.05);

      // Deterministically map each node into 3D spherical shell coordinates
      ids.forEach((id, idx) => {
        const p = positions[id];
        const x0 = p.x - currentGraphCentroid.x;
        const y0 = p.y - currentGraphCentroid.y;
        const r2D = Math.hypot(x0, y0);

        // Spherical depth: alternate front/back hemispheres so nodes form a rich 3D constellation
        const hemisphere = (idx % 2 === 0) ? 1 : -1;
        const sphereCap = Math.sqrt(Math.max(0, globeRadius * globeRadius - r2D * r2D));
        const z0 = hemisphere * Math.min(sphereCap * 0.85, 180 + (idx % 3) * 25);

        // Get original visual size if defined
        const existingNode = currentNodesDataSet ? currentNodesDataSet.get(id) : null;
        const origSize = existingNode && existingNode.size ? existingNode.size : (id.startsWith("user") ? 20 : (id.startsWith("dev") ? 22 : 18));

        baseNodes3D[id] = { x0, y0, z0, origSize };
      });
    }

    function renderGlobeFrame() {
      globeRafPending = false;
      if (!network || !network.body || !network.body.nodes) return;

      // Smooth interpolation towards target yaw/pitch for fluid 60-120 FPS
      currentYaw += (targetYaw - currentYaw) * 0.7;
      currentPitch += (targetPitch - currentPitch) * 0.7;

      const cosYaw = Math.cos(currentYaw);
      const sinYaw = Math.sin(currentYaw);
      const cosPitch = Math.cos(currentPitch);
      const sinPitch = Math.sin(currentPitch);
      const fov = 750;

      for (const id in baseNodes3D) {
        const node3D = baseNodes3D[id];
        const visNode = network.body.nodes[id];
        if (!visNode) continue;

        // 1. Rotate Yaw (Y-axis)
        const x1 = node3D.x0 * cosYaw + node3D.z0 * sinYaw;
        const z1 = -node3D.x0 * sinYaw + node3D.z0 * cosYaw;

        // 2. Rotate Pitch (X-axis)
        const y2 = node3D.y0 * cosPitch - z1 * sinPitch;
        const z2 = node3D.y0 * sinPitch + z1 * cosPitch;

        // 3. Perspective projection
        const scale = fov / (fov + z2);
        visNode.x = currentGraphCentroid.x + x1 * scale;
        visNode.y = currentGraphCentroid.y + y2 * scale;
        if (visNode.options) {
          visNode.options.size = Math.max(10, Math.min(34, Math.round(node3D.origSize * scale)));
        }
      }

      network.redraw();

      if (isGlobeDragging || Math.abs(currentYaw - targetYaw) > 0.0005 || Math.abs(currentPitch - targetPitch) > 0.0005) {
        globeRafPending = true;
        requestAnimationFrame(renderGlobeFrame);
      } else {
        updateGlobeIndicator();
      }
    }

    function toggleGlobeMode() {
      globeModeActive = !globeModeActive;
      const btn = document.getElementById("globe-mode-btn");
      const label = document.getElementById("globe-mode-label");
      const canvasContainer = document.getElementById("network-canvas");

      if (btn) btn.classList.toggle("active", globeModeActive);
      if (label) label.innerText = `3D Globe: ${globeModeActive ? 'On' : 'Off'}`;

      if (canvasContainer) {
        canvasContainer.style.cursor = globeModeActive ? "grab" : "";
      }

      if (network) {
        if (globeModeActive) {
          network.setOptions({
            physics: { enabled: false },
            interaction: { dragView: false, dragNodes: false }
          });
          network.stopSimulation();
        } else {
          network.setOptions({
            physics: { enabled: physicsState },
            interaction: { dragView: true, dragNodes: true }
          });
        }
      }

      showToast(`3D Globe Mode ${globeModeActive ? 'Enabled — Drag cursor horizontally or vertically to spin smoothly' : 'Disabled'}`);
    }

    function resetGlobeView() {
      targetYaw = 0;
      targetPitch = 0;
      currentYaw = 0;
      currentPitch = 0;
      if (network && network.body && network.body.nodes) {
        for (const id in baseNodes3D) {
          const node3D = baseNodes3D[id];
          const visNode = network.body.nodes[id];
          if (visNode) {
            visNode.x = currentGraphCentroid.x + node3D.x0;
            visNode.y = currentGraphCentroid.y + node3D.y0;
            if (visNode.options) visNode.options.size = node3D.origSize;
          }
        }
        network.redraw();
      }
      if (currentNodesDataSet) {
        const finalUpdates = Object.keys(baseNodes3D).map(id => ({
          id,
          x: currentGraphCentroid.x + baseNodes3D[id].x0,
          y: currentGraphCentroid.y + baseNodes3D[id].y0,
          size: baseNodes3D[id].origSize
        }));
        currentNodesDataSet.update(finalUpdates);
      }
      updateGlobeIndicator();
      if (network) {
        network.fit({ animation: { duration: 350, easingFunction: "easeInOutQuad" } });
      }
      showToast("Reset 3D Globe orientation to default view");
    }

    function updateGlobeIndicator() {
      const resetBtn = document.getElementById("reset-globe-btn");
      if (!resetBtn) return;
      const yawDeg = Math.round((currentYaw * 180 / Math.PI) % 360);
      const pitchDeg = Math.round((currentPitch * 180 / Math.PI) % 360);
      const isRotated = Math.abs(yawDeg) > 1 || Math.abs(pitchDeg) > 1;

      if (isRotated) {
        resetBtn.style.display = "inline-flex";
        resetBtn.innerText = `Reset 3D (${yawDeg}°, ${pitchDeg}°)`;
      } else {
        resetBtn.style.display = "none";
      }
    }

    function initCanvasRotationListeners() {
      const container = document.getElementById("network-canvas");
      if (!container || container.dataset.rotListenersAttached) return;
      container.dataset.rotListenersAttached = "true";

      container.addEventListener("contextmenu", (e) => {
        if (globeModeActive || e.altKey || e.shiftKey) {
          e.preventDefault();
        }
      });

      container.addEventListener("mousedown", (e) => {
        const isTrigger = globeModeActive || e.altKey || e.button === 2;
        if (!isTrigger || !network) return;

        isGlobeDragging = true;
        dragStartX = e.clientX;
        dragStartY = e.clientY;
        dragStartYaw = currentYaw;
        dragStartPitch = currentPitch;
        targetYaw = currentYaw;
        targetPitch = currentPitch;
        container.style.cursor = "grabbing";

        network.setOptions({
          physics: { enabled: false },
          interaction: { dragView: false, dragNodes: false }
        });
        network.stopSimulation();

        e.preventDefault();
        e.stopPropagation();
      }, true);

      window.addEventListener("mousemove", (e) => {
        if (!isGlobeDragging) return;

        const deltaX = e.clientX - dragStartX;
        const deltaY = e.clientY - dragStartY;

        targetYaw = dragStartYaw + deltaX * 0.007;

        const maxPitch = (75 * Math.PI) / 180;
        const rawPitch = dragStartPitch - deltaY * 0.007;
        targetPitch = Math.max(-maxPitch, Math.min(maxPitch, rawPitch));

        if (!globeRafPending) {
          globeRafPending = true;
          requestAnimationFrame(renderGlobeFrame);
        }
      });

      window.addEventListener("mouseup", (e) => {
        if (!isGlobeDragging) return;
        isGlobeDragging = false;
        const c = document.getElementById("network-canvas");
        if (c) {
          c.style.cursor = globeModeActive ? "grab" : "";
        }
        if (network) {
          network.setOptions({
            interaction: {
              dragView: !globeModeActive,
              dragNodes: !globeModeActive
            }
          });
        }
        if (currentNodesDataSet && network && network.body && network.body.nodes) {
          const finalUpdates = [];
          for (const id in baseNodes3D) {
            const visNode = network.body.nodes[id];
            if (visNode) finalUpdates.push({ id, x: visNode.x, y: visNode.y });
          }
          if (finalUpdates.length > 0) currentNodesDataSet.update(finalUpdates);
        }
        updateGlobeIndicator();
      });
    }

    // =========================================================================
    // MODEL TRACTION & SMOOTH FACE TRANSITION (NO DIRECT JUMP)
    // =========================================================================
    function computeTargetLayout(graphData, callback) {
      let offscreen = document.getElementById("offscreen-canvas");
      if (!offscreen) {
        offscreen = document.createElement("div");
        offscreen.id = "offscreen-canvas";
        offscreen.style.cssText = "position:absolute;left:-9999px;top:-9999px;width:800px;height:600px;visibility:hidden;pointer-events:none;";
        document.body.appendChild(offscreen);
      }

      const visibleNodes = graphData.nodes.filter(n => activeFilters[n.group] !== false);
      const visibleIds = new Set(visibleNodes.map(n => n.id));
      const visibleEdges = (graphData.edges || []).filter(e => visibleIds.has(e.from) && visibleIds.has(e.to));

      const tempNodes = new vis.DataSet(visibleNodes.map(n => ({ id: n.id })));
      const tempEdges = new vis.DataSet(visibleEdges.map(e => ({ from: e.from, to: e.to })));

      const tempOptions = {
        physics: {
          enabled: true,
          solver: "forceAtlas2Based",
          forceAtlas2Based: {
            gravitationalConstant: -420,
            centralGravity: 0.003,
            springLength: currentSpringLength,
            springConstant: 0.035,
            damping: 0.45,
            avoidOverlap: 1.0
          },
          stabilization: {
            enabled: true,
            iterations: 120,
            updateInterval: 25
          }
        }
      };

      let completed = false;
      const tempNet = new vis.Network(offscreen, { nodes: tempNodes, edges: tempEdges }, tempOptions);

      function finalize() {
        if (completed) return;
        completed = true;
        const positions = tempNet.getPositions();
        tempNet.destroy();
        callback(positions);
      }

      tempNet.once("stabilizationIterationsDone", finalize);
      setTimeout(finalize, 180); // Safety fallback
    }

    function animateTractionMorph(startPositions, targetPositions, onComplete, duration = 650) {
      if (morphRafId) cancelAnimationFrame(morphRafId);
      const startTime = performance.now();
      const nodeIds = Object.keys(targetPositions);

      if (network) {
        network.setOptions({ physics: { enabled: false } });
        network.stopSimulation();
      }

      let sumX = 0, sumY = 0, cCount = 0;
      for (const id in startPositions) {
        if (startPositions[id]) {
          sumX += startPositions[id].x;
          sumY += startPositions[id].y;
          cCount++;
        }
      }
      const fallbackX = cCount > 0 ? sumX / cCount : 0;
      const fallbackY = cCount > 0 ? sumY / cCount : 0;

      function step(now) {
        const elapsed = now - startTime;
        const progress = Math.min(1, elapsed / duration);
        // Elastic spring traction ease-out
        const ease = 1 - Math.pow(1 - progress, 3);

        for (const id of nodeIds) {
          const visNode = network && network.body && network.body.nodes ? network.body.nodes[id] : null;
          if (!visNode) continue;

          const s = startPositions[id] || { x: fallbackX, y: fallbackY };
          const t = targetPositions[id];

          visNode.x = s.x + (t.x - s.x) * ease;
          visNode.y = s.y + (t.y - s.y) * ease;
        }

        if (network) network.redraw();

        if (progress < 1) {
          morphRafId = requestAnimationFrame(step);
        } else {
          morphRafId = null;
          const finalUpdates = nodeIds.map(id => ({
            id: id,
            x: targetPositions[id].x,
            y: targetPositions[id].y
          }));
          if (currentNodesDataSet) currentNodesDataSet.update(finalUpdates);
          setup3DCoordinates(targetPositions);
          if (network) {
            network.fit({ animation: { duration: 300, easingFunction: "easeInOutQuad" } });
          }
          if (onComplete) onComplete();
        }
      }

      morphRafId = requestAnimationFrame(step);
    }

    async function fetchRings() {
      const url = document.getElementById("api-url").value.trim().replace(/\/$/, "");
      const dot = document.getElementById("status-dot");
      const label = document.getElementById("status-label");
      const analyzeBtn = document.getElementById("analyze-btn");
      const analyzeIcon = document.getElementById("analyze-icon");
      const analyzeText = document.getElementById("analyze-text");

      // Enter analysis processing state
      if (analyzeBtn) {
        analyzeBtn.disabled = true;
        analyzeBtn.style.opacity = "0.85";
      }
      if (analyzeIcon) {
        analyzeIcon.innerHTML = `<svg class="spin-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10" stroke-opacity="0.25"/><path d="M12 2a10 10 0 0 1 10 10"/></svg>`;
      }
      if (analyzeText) {
        analyzeText.innerText = "Analyzing GNN...";
      }

      const reqStartTime = Date.now();

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
      } finally {
        // Guarantee at least 320ms so feedback feels tactile and deliberate
        const elapsed = Date.now() - reqStartTime;
        if (elapsed < 320) {
          await new Promise(r => setTimeout(r, 320 - elapsed));
        }

        // Restore button state
        if (analyzeBtn) {
          analyzeBtn.disabled = false;
          analyzeBtn.style.opacity = "1";
        }
        if (analyzeIcon) {
          analyzeIcon.innerHTML = `<svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>`;
        }
        if (analyzeText) {
          analyzeText.innerText = "Run Analysis";
        }
      }

      document.getElementById("stat-rings").innerText = allRings.length;
      document.getElementById("rings-count-badge").innerText = `${allRings.length} total`;

      const crit = allRings.filter(r => r.score >= 0.75).length;
      const elev = allRings.length - crit;
      const cntAll = document.getElementById("count-all");
      const cntCrit = document.getElementById("count-critical");
      const cntElev = document.getElementById("count-elevated");
      if (cntAll) cntAll.innerText = allRings.length;
      if (cntCrit) cntCrit.innerText = crit;
      if (cntElev) cntElev.innerText = elev;

      renderRingsList(allRings);
      if (allRings.length > 0) {
        selectRing(activeIndex, true);
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
        if (currentTierFilter === 'elevated') {
          container.innerHTML = `
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 180px; text-align: center; color: var(--text-muted); padding: 18px;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--yellow-primary)" stroke-width="2" style="opacity: 0.9; margin-bottom: 8px;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              <span style="font-size: 12px; font-weight: 700; color: var(--text-main);">0 Elevated Syndicates</span>
              <span style="font-size: 11px; margin-top: 5px; color: var(--text-muted); line-height: 1.45;">All 10 detected mule syndicates met the Critical Risk threshold (&ge; 75%).</span>
            </div>
          `;
        } else {
          container.innerHTML = `
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 160px; text-align: center; color: var(--text-muted); padding: 16px;">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="opacity: 0.5; margin-bottom: 8px;"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
              <span style="font-size: 12px; font-weight: 600; color: var(--text-main);">No matching syndicates</span>
              <span style="font-size: 11px; margin-top: 4px; color: var(--text-dim);">Try searching another Ring or User ID</span>
            </div>
          `;
        }
        return;
      }

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
      const query = document.getElementById("search-filter").value.toLowerCase().trim();
      const filtered = allRings.filter(r => {
        const matchesQuery = !query ||
               `ring #${r.ring_id}`.toLowerCase().includes(query) ||
               `syndicate ${r.ring_id}`.toLowerCase().includes(query) ||
               String(r.ring_id).includes(query) ||
               r.members.some(m => String(m).includes(query));
        if (!matchesQuery) return false;
        if (currentTierFilter === 'critical') return r.score >= 0.75;
        if (currentTierFilter === 'elevated') return r.score < 0.75;
        return true;
      });
      renderRingsList(filtered);
    }

    function selectRing(index, isAnalysisTriggered = false) {
      activeIndex = index;
      const ring = allRings[index];
      if (!ring) return;

      // Update Active States
      const cards = document.querySelectorAll(".ring-card-item");
      cards.forEach((c, i) => c.classList.toggle("active", i === index));

      // Update Inspector Panel
      document.getElementById("inspector-heading").innerText = `Syndicate #${ring.ring_id}`;
      document.getElementById("inspector-badge").innerText = `RANK #${ring.rank || index + 1}`;
      document.getElementById("threat-rank-pill").innerText = `RANK #${ring.rank || index + 1}`;

      // Instant Threat Risk Score
      document.getElementById("threat-score-num").innerText = `${(ring.score * 100).toFixed(1)}%`;

      document.getElementById("sig-device").innerText = `${ring.shared_device_pct}%`;
      document.getElementById("sig-ip").innerText = `${ring.shared_ip_pairs} pairs`;
      document.getElementById("sig-vel").innerText = `${ring.transaction_velocity} tx/hr`;
      document.getElementById("sig-gnn").innerText = ring.avg_model_score.toFixed(3);
      document.getElementById("sig-fresh").innerText = `${ring.fresh_account_count} accounts`;
      document.getElementById("members-count").innerText = ring.member_count;

      // Direct, clean meter bar updates
      const mDev = document.getElementById("meter-device");
      const mIp = document.getElementById("meter-ip");
      const mVel = document.getElementById("meter-vel");
      const mGnn = document.getElementById("meter-gnn");
      const mFresh = document.getElementById("meter-fresh");

      if (mDev) mDev.style.width = `${Math.min(100, ring.shared_device_pct)}%`;
      if (mIp) mIp.style.width = `${Math.min(100, (ring.shared_ip_pairs / 28) * 100)}%`;
      if (mVel) mVel.style.width = `${Math.min(100, (ring.transaction_velocity / 45) * 100)}%`;
      if (mGnn) mGnn.style.width = `${Math.min(100, ring.avg_model_score * 100)}%`;
      if (mFresh) mFresh.style.width = `${Math.min(100, (ring.fresh_account_count / ring.member_count) * 100)}%`;

      // Reset freeze button
      const freezeBtn = document.getElementById("freeze-btn");
      freezeBtn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg> Freeze Ring Accounts (Simulation)`;
      freezeBtn.disabled = false;
      freezeBtn.style.opacity = "1";

      // Render Account Chips instantly
      const chipsBox = document.getElementById("members-chips");
      chipsBox.innerHTML = ring.members.map(m => `
        <span class="chip-account" onclick="focusOnNode('user_${m}')">User ${m}</span>
      `).join("");

      closeNodeInspector();
      // Render Graph with smooth model traction morph
      renderGraph(ring.graph, isAnalysisTriggered);
    }

    function renderGraph(graphData, isAnalysisTriggered = false) {
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

      // Physics configuration (settles calmly into clear syndicate topology)
      const options = {
        physics: {
          enabled: physicsState,
          solver: "forceAtlas2Based",
          forceAtlas2Based: {
            gravitationalConstant: -420,
            centralGravity: 0.003,
            springLength: currentSpringLength,
            springConstant: 0.035,
            damping: 0.45,
            avoidOverlap: 1.0
          },
          stabilization: {
            enabled: true,
            iterations: 150,
            updateInterval: 25
          }
        },
        interaction: {
          hover: true,
          tooltipDelay: 80,
          zoomView: true,
          dragView: true,
          dragNodes: true,
          zoomSpeed: 0.5, // Standard, common, normal zoom speed across all trackpads and mice
          navigationButtons: false,
          keyboard: false
        }
      };

      // FIRST LOAD: Initialize network instance
      if (!network) {
        currentNodesDataSet = nodes;
        network = new vis.Network(container, data, options);

        initCanvasRotationListeners();

        // Once layout stabilizes, lock into static view so zooming is 100% calm and smooth
        network.once("stabilizationIterationsDone", function() {
          network.fit({ animation: { duration: 350, easingFunction: "easeInOutQuad" } });
          network.stopSimulation();
          network.setOptions({ physics: { enabled: false } });
          setup3DCoordinates(network.getPositions());
        });

        // Update 3D base positions if user drags an individual node in standard mode
        network.on("dragEnd", function(params) {
          if (params.nodes && params.nodes.length > 0 && !isGlobeDragging && !globeModeActive) {
            setup3DCoordinates(network.getPositions());
          }
        });

        // =========================================================================
        // CONSTANT SCREEN TEXT SIZE & VISIBILITY AT ALL ZOOM LEVELS
        // =========================================================================
        network.on("afterDrawing", function(ctx) {
          ctx.save();
          ctx.setTransform(1, 0, 0, 1, 0, 0);

          const positions = network.getPositions();
          ctx.font = "600 11px 'Inter', -apple-system, 'Segoe UI', Roboto, sans-serif";
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

            const textWidth = ctx.measureText(labelText).width;
            ctx.fillStyle = "rgba(17, 18, 22, 0.92)";
            ctx.beginPath();
            ctx.roundRect(textX - textWidth / 2 - 5, textY - 8, textWidth + 10, 16, 4);
            ctx.fill();

            ctx.strokeStyle = node.group === "user" ? "rgba(250, 204, 21, 0.4)" : (node.group === "device" ? "rgba(56, 189, 248, 0.4)" : "rgba(52, 211, 153, 0.4)");
            ctx.lineWidth = 0.8;
            ctx.stroke();

            ctx.fillStyle = node.group === "user" ? "#facc15" : (node.group === "device" ? "#38bdf8" : "#34d399");
            ctx.fillText(labelText, textX, textY);
          }

          ctx.restore();
        });

        // Click node to open deep inspector
        network.on("click", function(params) {
          if (globeModeActive) return;
          if (params.nodes.length > 0) {
            showNodeInspector(params.nodes[0]);
          } else {
            closeNodeInspector();
          }
        });

        return;
      }

      // SUBSEQUENT RENDERS / RUN ANALYSIS:
      // Smooth model traction face-morphing (NO DIRECT JUMP)
      const oldPositions = network.getPositions();
      const oldCentroid = calculateCentroid(oldPositions);

      computeTargetLayout(graphData, function(targetPositions) {
        // If analysis was re-run on the model, rotate/relax target face (like SS1 to SS2)
        if (isAnalysisTriggered) {
          analysisFaceAngle = (analysisFaceAngle + Math.PI * 0.42) % (Math.PI * 2);
        }
        if (analysisFaceAngle !== 0) {
          const tc = calculateCentroid(targetPositions);
          const cos = Math.cos(analysisFaceAngle);
          const sin = Math.sin(analysisFaceAngle);
          for (const id in targetPositions) {
            const p = targetPositions[id];
            const dx = p.x - tc.x;
            const dy = p.y - tc.y;
            targetPositions[id] = {
              x: tc.x + dx * cos - dy * sin,
              y: tc.y + dx * sin + dy * cos
            };
          }
        }

        // Initialize node coordinates at current on-screen positions so they don't jump
        const positionedNodes = visibleNodes.map(n => {
          const p = oldPositions[n.id] || {
            x: oldCentroid.x + (Math.random() - 0.5) * 50,
            y: oldCentroid.y + (Math.random() - 0.5) * 50
          };
          let color = "#facc15";
          let shape = "dot";
          let size = 20;

          if (n.group === "user") {
            color = "#facc15";
            shape = "dot";
            size = 20;
          } else if (n.group === "device") {
            color = "#38bdf8";
            shape = "diamond";
            size = 22;
          } else if (n.group === "merchant") {
            color = "#34d399";
            shape = "triangle";
            size = 18;
          }

          return {
            id: n.id,
            label: " ",
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
            shadow: { enabled: true, color: "rgba(0, 0, 0, 0.6)", size: 6, x: 0, y: 3 },
            x: p.x,
            y: p.y
          };
        });

        const newNodesDataSet = new vis.DataSet(positionedNodes);
        currentNodesDataSet = newNodesDataSet;
        network.setData({ nodes: newNodesDataSet, edges: edges });

        // Launch smooth traction morph transition between faces
        animateTractionMorph(oldPositions, targetPositions, function() {
          setup3DCoordinates(targetPositions);
        }, 650);
      });
    }

    function showNodeInspector(nodeId) {
      inspectedNodeId = nodeId;
      const ring = allRings[activeIndex];
      if (!ring || !ring.graph) return;
      const node = ring.graph.nodes.find(n => n.id === nodeId);
      if (!node) return;

      const card = document.getElementById("node-inspector");
      const dot = document.getElementById("inspect-dot");
      const idEl = document.getElementById("inspect-id");
      const roleEl = document.getElementById("inspect-role");
      const scoreEl = document.getElementById("inspect-score");
      const degEl = document.getElementById("inspect-deg");

      idEl.innerText = node.label || node.id;
      
      const connectedEdges = (ring.graph.edges || []).filter(e => e.from === nodeId || e.to === nodeId);
      degEl.innerText = `${connectedEdges.length} links connected`;

      if (node.group === "user") {
        dot.style.background = "var(--yellow-primary)";
        roleEl.innerText = "Syndicate Mule Account";
        scoreEl.innerText = `${(ring.avg_model_score * 100).toFixed(1)}% Anomaly Risk`;
        scoreEl.style.color = "var(--yellow-primary)";
      } else if (node.group === "device") {
        dot.style.background = "var(--node-device)";
        roleEl.innerText = "Shared Hardware Fingerprint";
        scoreEl.innerText = `${ring.shared_device_pct}% Device Sharing`;
        scoreEl.style.color = "var(--node-device)";
      } else if (node.group === "merchant") {
        dot.style.background = "var(--node-merchant)";
        roleEl.innerText = "Target Merchant Endpoint";
        scoreEl.innerText = `${ring.transaction_velocity} tx/hr Burst Velocity`;
        scoreEl.style.color = "var(--node-merchant)";
      }

      card.style.display = "block";
      showToast(`Selected: ${node.label || node.id}`);
    }

    function closeNodeInspector() {
      const card = document.getElementById("node-inspector");
      if (card) card.style.display = "none";
      inspectedNodeId = null;
    }

    function isolateNodeNeighbors() {
      if (!inspectedNodeId || !network) return;
      const connected = network.getConnectedNodes(inspectedNodeId);
      network.selectNodes([inspectedNodeId, ...connected]);
      network.focus(inspectedNodeId, { scale: 1.4, animation: { duration: 400, easingFunction: "easeInOutQuad" } });
      showToast(`Focused direct links of ${inspectedNodeId}`);
    }

    function copyNodeId() {
      if (!inspectedNodeId) return;
      navigator.clipboard.writeText(inspectedNodeId).then(() => {
        showToast(`Copied ${inspectedNodeId} to clipboard`);
      });
    }

    function resetGraphView() {
      resetGlobeView();
      if (network) network.fit({ animation: { duration: 350, easingFunction: "easeInOutQuad" } });
    }

    function zoomIn() {
      if (!network) return;
      const s = network.getScale();
      network.moveTo({
        scale: s * 1.3,
        animation: { duration: 200, easingFunction: "easeInOutQuad" }
      });
    }

    function zoomOut() {
      if (!network) return;
      const s = network.getScale();
      network.moveTo({
        scale: s / 1.3,
        animation: { duration: 200, easingFunction: "easeInOutQuad" }
      });
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
            forceAtlas2Based: { springLength: currentSpringLength, gravitationalConstant: currentSpringLength === 380 ? -620 : -420 }
          }
        });
        network.startSimulation();
        setTimeout(() => {
          if (network) {
            network.stopSimulation();
            setup3DCoordinates(network.getPositions());
          }
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
      const btn = document.getElementById("freeze-btn");
      btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg> Accounts Suspended (Simulation)`;
      btn.disabled = true;
      btn.style.opacity = "0.7";
      showToast(`Simulation: Suspended ${ring.member_count} syndicate accounts in Ring #${ring.ring_id}`);
    }

    function copySarSummary() {
      const ring = allRings[activeIndex];
      if (!ring) return;
      const summaryText = `[DARKNODE FORENSIC CASE REPORT]
Case ID: DARKNODE-RING-${ring.ring_id}
Threat Assessment: ${(ring.score * 100).toFixed(1)}% RISK (Rank #${ring.rank || activeIndex + 1})
Syndicate Members (${ring.member_count}): ${ring.members.map(m => `User_${m}`).join(", ")}
Evidence Signals:
- Hardware Sharing: ${ring.shared_device_pct}% of accounts share physical device IDs
- IP Subnets: ${ring.shared_ip_pairs} interconnected proxy pairs
- Burst Velocity: ${ring.transaction_velocity} tx/hr
- Heterogeneous GNN Confidence: ${ring.avg_model_score.toFixed(3)}
- Rapid Onboarding: ${ring.fresh_account_count} accounts created in burst window
Action Recommendation: Coordinated mule syndicate detected. Initiate credential suspension and SAR filing.`;

      navigator.clipboard.writeText(summaryText).then(() => {
        showToast(`Copied SAR Forensic Report for Ring #${ring.ring_id}!`);
      }).catch(() => {
        showToast(`Case report prepared for Ring #${ring.ring_id}`);
      });
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
      if (modal) {
        modal.classList.add("open");
        // Animate benchmark comparison bars from 0% to target data-width
        const bars = modal.querySelectorAll(".bench-bar-base, .bench-bar-gnn");
        bars.forEach(bar => {
          const target = bar.getAttribute("data-width") || bar.style.width;
          if (!bar.getAttribute("data-width")) bar.setAttribute("data-width", target);
          bar.style.width = "0%";
          requestAnimationFrame(() => {
            requestAnimationFrame(() => {
              bar.style.width = target;
            });
          });
        });
      }
    }

    function closeBenchmarkModal(e) {
      if (e && e.target !== document.getElementById("benchmark-modal") && !e.target.closest(".modal-close-btn")) return;
      const modal = document.getElementById("benchmark-modal");
      if (modal) modal.classList.remove("open");
    }

    // Keyboard Shortcuts
    document.addEventListener("keydown", (e) => {
      if (e.target.tagName === "INPUT") return;
      if (e.key === "Escape") {
        closeGuideModal();
        closeBenchmarkModal();
        closeNodeInspector();
      } else if (e.key === "f" || e.key === "F") {
        resetGraphView();
      } else if (e.key === " ") {
        e.preventDefault();
        togglePhysics();
      } else if (e.key === "+" || e.key === "=") {
        zoomIn();
      } else if (e.key === "-" || e.key === "_") {
        zoomOut();
      }
    });

    let toastTimer = null;
    function showToast(text) {
      const toast = document.getElementById("toast");
      if (!toast) return;
      document.getElementById("toast-text").innerText = text;
      toast.classList.remove("closing");
      toast.classList.add("visible");
      if (toastTimer) clearTimeout(toastTimer);
      toastTimer = setTimeout(() => {
        toast.classList.add("closing");
        setTimeout(() => {
          toast.classList.remove("visible", "closing");
        }, 180);
      }, 3200);
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
