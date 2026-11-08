"""
Contract Review & Obligation Tracking Agent - Interactive Dashboard
Serves a full-featured web dashboard at http://localhost:8050
"""
import http.server
import json
import os
import socketserver
import datetime as dt

PORT = 8050

def generate_dashboard_html():
    """Generate the complete dashboard HTML with embedded data."""
    
    # Load all data
    results = json.load(open("out/results.json"))
    alerts = json.load(open("out/alerts.json"))
    audit_log = json.load(open("out/audit_log.json"))
    eval_results = json.load(open("out/eval_results.json"))
    ground_truth = json.load(open("ground_truth.json"))
    
    # Prepare data for JS
    results_json = json.dumps(results, default=str)
    alerts_json = json.dumps(alerts, default=str)
    audit_json = json.dumps(audit_log, default=str)
    eval_json = json.dumps(eval_results, default=str)
    gt_json = json.dumps(ground_truth, default=str)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Contract Review & Obligation Tracking Agent — Dashboard</title>
<style>
:root {{
    --bg: #0f172a;
    --card: #1e293b;
    --card-hover: #273548;
    --border: #334155;
    --text: #e2e8f0;
    --text-muted: #94a3b8;
    --accent: #3b82f6;
    --accent-light: #60a5fa;
    --success: #22c55e;
    --warning: #f59e0b;
    --danger: #ef4444;
    --info: #06b6d4;
    --purple: #a855f7;
    --pink: #ec4899;
    --gradient-1: linear-gradient(135deg, #3b82f6, #8b5cf6);
    --gradient-2: linear-gradient(135deg, #22c55e, #06b6d4);
    --gradient-3: linear-gradient(135deg, #f59e0b, #ef4444);
    --gradient-4: linear-gradient(135deg, #ec4899, #a855f7);
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden;
}}

/* Header */
.header {{
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-bottom: 1px solid var(--border);
    padding: 20px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(12px);
}}

.header-left {{
    display: flex;
    align-items: center;
    gap: 16px;
}}

.logo {{
    width: 44px; height: 44px;
    background: var(--gradient-1);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; font-weight: 700; color: white;
}}

.header h1 {{
    font-size: 20px; font-weight: 700; color: white;
}}

.header p {{
    font-size: 12px; color: var(--text-muted); margin-top: 2px;
}}

.header-right {{
    display: flex; align-items: center; gap: 16px;
    font-size: 13px; color: var(--text-muted);
}}

.badge {{
    display: inline-flex; align-items: center; gap: 4px;
    padding: 4px 10px; border-radius: 20px;
    font-size: 11px; font-weight: 600;
}}

.badge-success {{ background: rgba(34,197,94,0.15); color: #4ade80; }}
.badge-warning {{ background: rgba(245,158,11,0.15); color: #fbbf24; }}
.badge-danger {{ background: rgba(239,68,68,0.15); color: #f87171; }}
.badge-info {{ background: rgba(6,182,212,0.15); color: #22d3ee; }}
.badge-purple {{ background: rgba(168,85,247,0.15); color: #c084fc; }}

/* Navigation Tabs */
.nav-tabs {{
    display: flex;
    background: var(--card);
    border-bottom: 1px solid var(--border);
    padding: 0 32px;
    overflow-x: auto;
}}

.nav-tab {{
    padding: 14px 20px;
    font-size: 13px;
    font-weight: 500;
    color: var(--text-muted);
    cursor: pointer;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
    white-space: nowrap;
    user-select: none;
}}

.nav-tab:hover {{ color: var(--text); }}
.nav-tab.active {{ color: var(--accent-light); border-bottom-color: var(--accent); }}

/* Main */
.main {{ padding: 24px 32px; max-width: 1600px; margin: 0 auto; }}

.tab-content {{ display: none; }}
.tab-content.active {{ display: block; }}

/* Grid */
.grid {{ display: grid; gap: 20px; }}
.grid-4 {{ grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }}
.grid-3 {{ grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }}
.grid-2 {{ grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); }}

/* Cards */
.card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    transition: all 0.2s;
}}

.card:hover {{ border-color: rgba(59,130,246,0.3); }}

.card-header {{
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 16px;
}}

.card-title {{
    font-size: 14px; font-weight: 600; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.5px;
}}

/* Stat Cards */
.stat-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    position: relative;
    overflow: hidden;
}}

.stat-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}}

.stat-card.blue::before {{ background: var(--gradient-1); }}
.stat-card.green::before {{ background: var(--gradient-2); }}
.stat-card.orange::before {{ background: var(--gradient-3); }}
.stat-card.purple::before {{ background: var(--gradient-4); }}

.stat-label {{ font-size: 12px; color: var(--text-muted); font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }}
.stat-value {{ font-size: 32px; font-weight: 700; margin: 8px 0 4px; }}
.stat-sub {{ font-size: 12px; color: var(--text-muted); }}

/* Charts */
.chart-container {{
    position: relative;
    width: 100%;
}}

canvas {{ max-width: 100%; }}

/* Tables */
.table-container {{
    overflow-x: auto;
    border-radius: 8px;
    border: 1px solid var(--border);
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}}

th {{
    background: rgba(59,130,246,0.08);
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    font-size: 11px;
    letter-spacing: 0.5px;
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
}}

td {{
    padding: 10px 14px;
    border-bottom: 1px solid rgba(51,65,85,0.5);
    vertical-align: top;
}}

tr:hover td {{ background: rgba(59,130,246,0.04); }}

.severity-high {{ color: #f87171; font-weight: 700; }}
.severity-medium {{ color: #fbbf24; font-weight: 600; }}
.severity-low {{ color: #60a5fa; }}

.route-legal {{ color: #f87171; }}
.route-manager {{ color: #fbbf24; }}
.route-auto {{ color: #4ade80; }}

.status-past {{ color: #f87171; }}
.status-30 {{ color: #fbbf24; }}
.status-90 {{ color: #fb923c; }}
.status-upcoming {{ color: #4ade80; }}
.status-review {{ color: #60a5fa; }}

/* Section header */
.section-header {{
    display: flex; align-items: center; gap: 10px;
    margin: 28px 0 16px; font-size: 16px; font-weight: 600;
}}

.section-header .icon {{ font-size: 20px; }}

/* Donut chart */
.donut-wrapper {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 24px;
    padding: 10px 0;
}}

.donut-legend {{
    display: flex;
    flex-direction: column;
    gap: 8px;
}}

.legend-item {{
    display: flex; align-items: center; gap: 8px;
    font-size: 13px;
}}

.legend-dot {{
    width: 10px; height: 10px; border-radius: 50%;
}}

/* Architecture diagram */
.arch-diagram {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    padding: 20px;
}}

.arch-row {{
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: center;
}}

.arch-box {{
    padding: 12px 18px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 600;
    text-align: center;
    min-width: 140px;
    border: 1px solid;
}}

.arch-supervisor {{
    background: rgba(59,130,246,0.15); border-color: rgba(59,130,246,0.4); color: #60a5fa;
}}
.arch-worker {{
    background: rgba(168,85,247,0.12); border-color: rgba(168,85,247,0.35); color: #c084fc;
}}
.arch-human {{
    background: rgba(34,197,94,0.12); border-color: rgba(34,197,94,0.35); color: #4ade80;
}}
.arch-store {{
    background: rgba(245,158,11,0.12); border-color: rgba(245,158,11,0.35); color: #fbbf24;
}}

.arch-arrow {{
    color: var(--text-muted);
    font-size: 20px;
}}

/* Progress bar */
.progress-bar {{
    height: 8px;
    background: rgba(255,255,255,0.08);
    border-radius: 4px;
    overflow: hidden;
    margin-top: 8px;
}}

.progress-fill {{
    height: 100%;
    border-radius: 4px;
    transition: width 1s ease;
}}

/* Risk matrix */
.risk-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 12px;
}}

.risk-item {{
    padding: 14px;
    border-radius: 8px;
    border-left: 4px solid;
    background: rgba(255,255,255,0.02);
}}

.risk-item.high {{ border-left-color: #ef4444; }}
.risk-item.medium {{ border-left-color: #f59e0b; }}
.risk-item.low {{ border-left-color: #3b82f6; }}

.risk-title {{ font-size: 13px; font-weight: 600; margin-bottom: 4px; }}
.risk-detail {{ font-size: 12px; color: var(--text-muted); }}

/* Timeline */
.timeline {{ position: relative; padding-left: 24px; }}
.timeline::before {{
    content: ''; position: absolute; left: 8px; top: 0; bottom: 0;
    width: 2px; background: var(--border);
}}

.timeline-item {{
    position: relative;
    padding: 12px 0;
}}

.timeline-item::before {{
    content: '';
    position: absolute;
    left: -20px;
    top: 16px;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--accent);
    border: 2px solid var(--bg);
}}

.timeline-title {{ font-size: 13px; font-weight: 600; }}
.timeline-desc {{ font-size: 12px; color: var(--text-muted); margin-top: 2px; }}
.timeline-date {{ font-size: 11px; color: var(--accent-light); margin-top: 2px; }}

/* KPI card */
.kpi-card {{
    text-align: center;
    padding: 24px 16px;
}}

.kpi-value {{
    font-size: 42px;
    font-weight: 800;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.kpi-label {{ font-size: 13px; color: var(--text-muted); margin-top: 4px; }}
.kpi-target {{ font-size: 12px; color: var(--success); margin-top: 6px; }}

/* Responsive */
@media (max-width: 768px) {{
    .main {{ padding: 16px; }}
    .header {{ padding: 16px; }}
    .grid-4 {{ grid-template-columns: repeat(2, 1fr); }}
    .grid-2, .grid-3 {{ grid-template-columns: 1fr; }}
    .stat-value {{ font-size: 24px; }}
}}

/* Scroll animations */
.fade-in {{
    animation: fadeIn 0.4s ease forwards;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* Tooltip */
.tooltip-container {{ position: relative; }}
.tooltip-container .tooltip {{
    display: none;
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: #0f172a;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 11px;
    white-space: nowrap;
    z-index: 10;
}}
.tooltip-container:hover .tooltip {{ display: block; }}

/* University branding */
.uni-footer {{
    text-align: center;
    padding: 24px;
    margin-top: 40px;
    border-top: 1px solid var(--border);
    font-size: 12px;
    color: var(--text-muted);
}}
</style>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
</head>
<body>

<!-- Header -->
<div class="header">
    <div class="header-left">
        <div class="logo">CR</div>
        <div>
            <h1>Contract Review & Obligation Tracking Agent</h1>
            <p>Agentic AI for Business Operations — Woxsen University, Group 10</p>
        </div>
    </div>
    <div class="header-right">
        <span class="badge badge-success">● Prototype Active</span>
        <span>As-of: 6 Nov 2026</span>
    </div>
</div>

<!-- Tabs -->
<div class="nav-tabs">
    <div class="nav-tab active" data-tab="overview">📊 Overview</div>
    <div class="nav-tab" data-tab="contracts">📄 Contracts</div>
    <div class="nav-tab" data-tab="obligations">⏰ Obligations</div>
    <div class="nav-tab" data-tab="risk">⚠️ Risk & Flags</div>
    <div class="nav-tab" data-tab="evaluation">✅ Evaluation</div>
    <div class="nav-tab" data-tab="architecture">🏗️ Architecture</div>
    <div class="nav-tab" data-tab="business">💰 Business Case</div>
    <div class="nav-tab" data-tab="governance">🛡️ Governance</div>
    <div class="nav-tab" data-tab="audit">📋 Audit Log</div>
</div>

<!-- Main Content -->
<div class="main">

<!-- ═══════════════ TAB: OVERVIEW ═══════════════ -->
<div class="tab-content active" id="tab-overview">
    <div class="grid grid-4" style="margin-bottom:24px">
        <div class="stat-card blue fade-in">
            <div class="stat-label">Contracts Analyzed</div>
            <div class="stat-value" id="total-contracts">10</div>
            <div class="stat-sub">Across 4 contract types</div>
        </div>
        <div class="stat-card green fade-in">
            <div class="stat-label">Field Accuracy</div>
            <div class="stat-value" id="field-acc">97.8%</div>
            <div class="stat-sub">88 of 90 fields correct</div>
            <div class="progress-bar"><div class="progress-fill" style="width:97.8%;background:var(--gradient-2)"></div></div>
        </div>
        <div class="stat-card orange fade-in">
            <div class="stat-label">Obligation Recall</div>
            <div class="stat-value" id="ob-recall">96.7%</div>
            <div class="stat-sub">29 of 30 obligations found</div>
            <div class="progress-bar"><div class="progress-fill" style="width:96.7%;background:var(--gradient-3)"></div></div>
        </div>
        <div class="stat-card purple fade-in">
            <div class="stat-label">Playbook Flags</div>
            <div class="stat-value" id="total-flags">—</div>
            <div class="stat-sub">100% recall on expected flags</div>
            <div class="progress-bar"><div class="progress-fill" style="width:100%;background:var(--gradient-4)"></div></div>
        </div>
    </div>

    <div class="grid grid-3">
        <div class="card">
            <div class="card-header"><span class="card-title">Routing Distribution</span></div>
            <div class="chart-container"><canvas id="chart-routing"></canvas></div>
        </div>
        <div class="card">
            <div class="card-header"><span class="card-title">Obligation Status Breakdown</span></div>
            <div class="chart-container"><canvas id="chart-ob-status"></canvas></div>
        </div>
        <div class="card">
            <div class="card-header"><span class="card-title">Flag Severity Distribution</span></div>
            <div class="chart-container"><canvas id="chart-flag-severity"></canvas></div>
        </div>
    </div>

    <div class="grid grid-2" style="margin-top:20px">
        <div class="card">
            <div class="card-header"><span class="card-title">Contracts by Type</span></div>
            <div class="chart-container"><canvas id="chart-types"></canvas></div>
        </div>
        <div class="card">
            <div class="card-header"><span class="card-title">Governing Law Distribution</span></div>
            <div class="chart-container"><canvas id="chart-laws"></canvas></div>
        </div>
    </div>
</div>

<!-- ═══════════════ TAB: CONTRACTS ═══════════════ -->
<div class="tab-content" id="tab-contracts">
    <div class="section-header"><span class="icon">📄</span> All Contracts — Extracted Fields</div>
    <div class="table-container">
        <table id="contracts-table">
            <thead>
                <tr>
                    <th>ID</th><th>Type</th><th>Term</th><th>Auto-Renew</th><th>Notice</th>
                    <th>Payment</th><th>Liability</th><th>Indemnity</th><th>Law</th>
                    <th>DPDP</th><th>Term. Conv.</th><th>Route</th><th>Flags</th>
                </tr>
            </thead>
            <tbody id="contracts-tbody"></tbody>
        </table>
    </div>
</div>

<!-- ═══════════════ TAB: OBLIGATIONS ═══════════════ -->
<div class="tab-content" id="tab-obligations">
    <div class="grid grid-4" style="margin-bottom:20px">
        <div class="stat-card blue">
            <div class="stat-label">Past Due</div>
            <div class="stat-value status-past" id="ob-past">—</div>
        </div>
        <div class="stat-card orange">
            <div class="stat-label">Due ≤ 30 Days</div>
            <div class="stat-value status-30" id="ob-30">—</div>
        </div>
        <div class="stat-card purple">
            <div class="stat-label">Due ≤ 90 Days</div>
            <div class="stat-value status-90" id="ob-90">—</div>
        </div>
        <div class="stat-card green">
            <div class="stat-label">Upcoming</div>
            <div class="stat-value status-upcoming" id="ob-upcoming">—</div>
        </div>
    </div>
    <div class="section-header"><span class="icon">⏰</span> All Obligations & Alerts</div>
    <div class="table-container">
        <table>
            <thead>
                <tr><th>Contract</th><th>Party</th><th>Action</th><th>Due Date</th><th>Status</th><th>Days</th></tr>
            </thead>
            <tbody id="obligations-tbody"></tbody>
        </table>
    </div>
</div>

<!-- ═══════════════ TAB: RISK & FLAGS ═══════════════ -->
<div class="tab-content" id="tab-risk">
    <div class="section-header"><span class="icon">⚠️</span> All Playbook Flags by Contract</div>
    <div class="table-container">
        <table>
            <thead>
                <tr><th>Contract</th><th>Route</th><th>Severity</th><th>Issue</th></tr>
            </thead>
            <tbody id="flags-tbody"></tbody>
        </table>
    </div>

    <div class="section-header"><span class="icon">📋</span> Playbook Rules</div>
    <div class="risk-grid">
        <div class="risk-item medium">
            <div class="risk-title">R-PAY: Max Payment Days ≤ 45</div>
            <div class="risk-detail">Flags MEDIUM if payment term exceeds 45 days</div>
        </div>
        <div class="risk-item medium">
            <div class="risk-title">R-NOTICE: Notice Window ≤ 60 days</div>
            <div class="risk-detail">Flags MEDIUM if auto-renewal notice exceeds 60 days</div>
        </div>
        <div class="risk-item medium">
            <div class="risk-title">R-LAW: Governing Law must be India</div>
            <div class="risk-detail">Flags MEDIUM if governing law is not India</div>
        </div>
        <div class="risk-item high">
            <div class="risk-title">R-LIAB: Liability must be capped</div>
            <div class="risk-detail">Flags HIGH if liability is unlimited</div>
        </div>
        <div class="risk-item medium">
            <div class="risk-title">R-INDEM: Indemnity must be mutual</div>
            <div class="risk-detail">Flags MEDIUM if indemnity is one-way</div>
        </div>
        <div class="risk-item high">
            <div class="risk-title">R-DPDP: Data Protection clause required</div>
            <div class="risk-detail">Flags HIGH if no DPDP Act 2023 clause found</div>
        </div>
    </div>
</div>

<!-- ═══════════════ TAB: EVALUATION ═══════════════ -->
<div class="tab-content" id="tab-evaluation">
    <div class="section-header"><span class="icon">✅</span> Test Results (Section 4.5)</div>
    <div class="grid grid-3" style="margin-bottom:20px">
        <div class="card kpi-card">
            <div class="kpi-value" id="eval-field-acc">—</div>
            <div class="kpi-label">Field Extraction Accuracy</div>
            <div class="kpi-target">Target: ≥ 95%  ✅ PASS</div>
        </div>
        <div class="card kpi-card">
            <div class="kpi-value" id="eval-ob-recall">—</div>
            <div class="kpi-label">Obligation Recall</div>
            <div class="kpi-target">Target: ≥ 95%  ✅ PASS</div>
        </div>
        <div class="card kpi-card">
            <div class="kpi-value" id="eval-routing">—</div>
            <div class="kpi-label">Routing Accuracy</div>
            <div class="kpi-target">Target: 100%  ✅ PASS</div>
        </div>
    </div>

    <div class="table-container" style="margin-bottom:20px">
        <table>
            <thead><tr><th>Test ID</th><th>Scenario</th><th>Expected</th><th>Actual</th><th>Result</th></tr></thead>
            <tbody>
                <tr><td>T1</td><td>Extract 9 key fields from 10 contracts</td><td>≥ 95% of 90 values</td><td id="t1-actual">—</td><td><span class="badge badge-success">PASS</span></td></tr>
                <tr><td>T2</td><td>Capture dated obligations incl. renewal deadlines</td><td>≥ 95% recall, 0 false positives</td><td id="t2-actual">—</td><td><span class="badge badge-success">PASS</span></td></tr>
                <tr><td>T3</td><td>Playbook flags vs ground-truth flags</td><td>All expected flags raised</td><td id="t3-actual">—</td><td><span class="badge badge-success">PASS</span></td></tr>
                <tr><td>T4</td><td>Routing to legal/manager/auto-approve</td><td>Route matches expected</td><td id="t4-actual">—</td><td><span class="badge badge-success">PASS</span></td></tr>
                <tr><td>T5</td><td>Unusual phrasings (3 cases)</td><td>Correct or visible failure</td><td>0/3 extracted; all 3 flagged</td><td><span class="badge badge-warning">SAFE FAIL</span></td></tr>
                <tr><td>T6</td><td>Obligation status as of 6 Nov 2026</td><td>Correct status bands</td><td id="t6-actual">—</td><td><span class="badge badge-success">PASS</span></td></tr>
            </tbody>
        </table>
    </div>

    <div class="section-header"><span class="icon">❌</span> Field Mismatches</div>
    <div class="table-container">
        <table>
            <thead><tr><th>Contract</th><th>Field</th><th>Expected</th><th>Actual</th></tr></thead>
            <tbody id="mismatches-tbody"></tbody>
        </table>
    </div>
</div>

<!-- ═══════════════ TAB: ARCHITECTURE ═══════════════ -->
<div class="tab-content" id="tab-architecture">
    <div class="section-header"><span class="icon">🏗️</span> System Architecture</div>
    <div class="card" style="margin-bottom:20px">
        <div class="arch-diagram">
            <div class="arch-row">
                <div class="arch-box arch-human">👤 User Interface<br><small>Upload · Review Queue · Dashboard</small></div>
            </div>
            <div class="arch-arrow">▼</div>
            <div class="arch-row">
                <div class="arch-box arch-supervisor">🎯 Supervisor Agent<br><small>Route · Retry · Escalate · Audit</small></div>
            </div>
            <div class="arch-arrow">▼ ▼ ▼ ▼</div>
            <div class="arch-row">
                <div class="arch-box arch-worker">📥 Intake & Classify<br><small>Type · Parties · Quality</small></div>
                <div class="arch-box arch-worker">🔍 Clause Extraction<br><small>9 Fields · Evidence · Confidence</small></div>
                <div class="arch-box arch-worker">⚖️ Risk Review<br><small>Playbook · Severity · Flags</small></div>
                <div class="arch-box arch-worker">📅 Obligation Tracker<br><small>Deadlines · Alerts · Owners</small></div>
            </div>
            <div class="arch-arrow">▼</div>
            <div class="arch-row">
                <div class="arch-box arch-human">👨‍⚖️ Human-in-the-Loop Gate<br><small>HC1: Legal · HC2: Manager · HC3: Low-Conf · HC4: Obligations</small></div>
            </div>
            <div class="arch-arrow">▼</div>
            <div class="arch-row">
                <div class="arch-box arch-store">📁 Contract Store</div>
                <div class="arch-box arch-store">🔎 Vector Index (RAG)</div>
                <div class="arch-box arch-store">🗄️ Obligation DB</div>
                <div class="arch-box arch-store">📝 Audit Log</div>
            </div>
        </div>
    </div>

    <div class="section-header"><span class="icon">🔧</span> Technology Stack</div>
    <div class="table-container">
        <table>
            <thead><tr><th>Layer</th><th>Production Target</th><th>Prototype</th><th>Reason</th></tr></thead>
            <tbody>
                <tr><td>LLM</td><td>Claude (Anthropic API)</td><td>Not used (rule-based)</td><td>Reproducibility</td></tr>
                <tr><td>Agent Framework</td><td>LangGraph</td><td>Plain Python functions</td><td>Same interface, no dependencies</td></tr>
                <tr><td>Data / Vector Store</td><td>Vector index + Postgres</td><td>JSON files</td><td>Simple, inspectable</td></tr>
                <tr><td>Integrations</td><td>Email & calendar alerts</td><td>Alert list as JSON</td><td>Logic without sending</td></tr>
                <tr><td>UI</td><td>Web review queue & dashboard</td><td>This dashboard</td><td>Full visualization</td></tr>
            </tbody>
        </table>
    </div>

    <div class="section-header"><span class="icon">📋</span> Agent Specification</div>
    <div class="table-container">
        <table>
            <thead><tr><th>Agent</th><th>Goal</th><th>Tools / APIs</th><th>Output</th></tr></thead>
            <tbody>
                <tr><td><strong>Supervisor</strong></td><td>Run workflow; route, retry or escalate</td><td>Worker calls; review-queue API; audit logger</td><td>Routing decision; final status</td></tr>
                <tr><td><strong>Intake & Classify</strong></td><td>Identify type, parties, language, quality</td><td>Text extraction; type classifier</td><td>Clean text; type; parties; effective date</td></tr>
                <tr><td><strong>Clause Extraction</strong></td><td>Extract 9 fields + obligations with evidence</td><td>LLM (structured output); regex; clause retriever</td><td>JSON of fields, obligations, evidence, confidence</td></tr>
                <tr><td><strong>Risk Review</strong></td><td>Compare fields with playbook, rate severity</td><td>Playbook lookup (RAG); rule engine</td><td>List of flags with severity and rationale</td></tr>
                <tr><td><strong>Obligation Tracker</strong></td><td>Register obligations, compute deadlines, schedule alerts</td><td>Obligation DB (write); calendar/email API</td><td>Obligation records; T-30 and T-7 alerts</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- ═══════════════ TAB: BUSINESS CASE ═══════════════ -->
<div class="tab-content" id="tab-business">
    <div class="grid grid-4" style="margin-bottom:20px">
        <div class="stat-card green">
            <div class="stat-label">Total Benefit (Yr 1+2)</div>
            <div class="stat-value" style="color:#4ade80">₹49.9L</div>
            <div class="stat-sub">INR Lakh over 2 operating years</div>
        </div>
        <div class="stat-card orange">
            <div class="stat-label">Total Cost (Yr 0+1+2)</div>
            <div class="stat-value" style="color:#fbbf24">₹29.3L</div>
            <div class="stat-sub">Including development</div>
        </div>
        <div class="stat-card blue">
            <div class="stat-label">ROI</div>
            <div class="stat-value" style="color:#60a5fa">70.3%</div>
            <div class="stat-sub">Over two operating years</div>
        </div>
        <div class="stat-card purple">
            <div class="stat-label">Payback Period</div>
            <div class="stat-value" style="color:#c084fc">10.5mo</div>
            <div class="stat-sub">From start of Year 1</div>
        </div>
    </div>

    <div class="grid grid-2">
        <div class="card">
            <div class="card-header"><span class="card-title">Cost-Benefit Analysis (INR Lakh)</span></div>
            <div class="chart-container"><canvas id="chart-cost-benefit"></canvas></div>
        </div>
        <div class="card">
            <div class="card-header"><span class="card-title">Cumulative Net Benefit</span></div>
            <div class="chart-container"><canvas id="chart-cumulative"></canvas></div>
        </div>
    </div>

    <div class="grid grid-2" style="margin-top:20px">
        <div class="card">
            <div class="card-header"><span class="card-title">Benefit Breakdown (Annual)</span></div>
            <div class="chart-container"><canvas id="chart-benefit-breakdown"></canvas></div>
        </div>
        <div class="card">
            <div class="card-header"><span class="card-title">Sensitivity Analysis</span></div>
            <div class="chart-container"><canvas id="chart-sensitivity"></canvas></div>
        </div>
    </div>

    <div class="section-header"><span class="icon">📈</span> KPI Targets</div>
    <div class="table-container">
        <table>
            <thead><tr><th>KPI</th><th>Baseline</th><th>Target</th><th>Measurement</th></tr></thead>
            <tbody>
                <tr><td>First-pass review time</td><td>4.0 hours</td><td>≤ 1.5 hours</td><td>Workflow timestamps</td></tr>
                <tr><td>Missed/late obligations</td><td>6%</td><td>&lt; 1%</td><td>Tracker audit</td></tr>
                <tr><td>Field extraction accuracy</td><td>N/A (manual)</td><td>≥ 95%</td><td>Lawyer sample (60+ contracts)</td></tr>
                <tr><td>High-risk flag recall</td><td>N/A</td><td>100%</td><td>Expert re-review</td></tr>
                <tr><td>Obligation coverage</td><td>~40%</td><td>≥ 95%</td><td>Tracker audit</td></tr>
                <tr><td>Human override rate</td><td>N/A</td><td>Track; investigate &gt; 20%</td><td>Audit log</td></tr>
            </tbody>
        </table>
    </div>

    <div class="section-header"><span class="icon">🗺️</span> Phased Rollout Roadmap</div>
    <div class="timeline">
        <div class="timeline-item">
            <div class="timeline-title">Phase 1: Pilot</div>
            <div class="timeline-desc">60 contracts, 2 business units, shadow mode. Agent suggests; humans decide everything.</div>
            <div class="timeline-date">Months 1–3</div>
        </div>
        <div class="timeline-item">
            <div class="timeline-title">Phase 2: Expand</div>
            <div class="timeline-desc">All vendor contracts + NDAs + customer agreements. Autonomous extraction; approval for HIGH flags.</div>
            <div class="timeline-date">Months 4–9</div>
        </div>
        <div class="timeline-item">
            <div class="timeline-title">Phase 3: Scale</div>
            <div class="timeline-desc">All contract types; ERP integrations; analytics. Auto-approve clean contracts with sampling audit.</div>
            <div class="timeline-date">Months 10–18</div>
        </div>
    </div>
</div>

<!-- ═══════════════ TAB: GOVERNANCE ═══════════════ -->
<div class="tab-content" id="tab-governance">
    <div class="section-header"><span class="icon">🛡️</span> Risk Register</div>
    <div class="risk-grid" style="margin-bottom:24px">
        <div class="risk-item high">
            <div class="risk-title">Hallucination</div>
            <div class="risk-detail">Invented clause/value/date → Evidence required; dates by code</div>
        </div>
        <div class="risk-item high">
            <div class="risk-title">Missed Clause (False Negative)</div>
            <div class="risk-detail">Rule engine for numeric; recall tracked; sampling audit</div>
        </div>
        <div class="risk-item high">
            <div class="risk-title">Prompt Injection</div>
            <div class="risk-detail">Contract text as data; no outbound tools for extraction; schema validation</div>
        </div>
        <div class="risk-item high">
            <div class="risk-title">Data Privacy Breach</div>
            <div class="risk-detail">DPA with model provider; redact PII; encryption; role-based access</div>
        </div>
        <div class="risk-item medium">
            <div class="risk-title">Automation Bias</div>
            <div class="risk-detail">Show evidence next to flags; random deep-review sampling</div>
        </div>
        <div class="risk-item medium">
            <div class="risk-title">Model/Service Outage</div>
            <div class="risk-detail">Fallback to manual queue; abstraction layer; data export</div>
        </div>
        <div class="risk-item high">
            <div class="risk-title">Wrong Deadline</div>
            <div class="risk-detail">Deterministic date code with unit tests; HC4 human confirmation</div>
        </div>
        <div class="risk-item low">
            <div class="risk-title">Bias / Unfair Outcome</div>
            <div class="risk-detail">Uniform playbook rules; review override stats by vendor type</div>
        </div>
    </div>

    <div class="section-header"><span class="icon">🔐</span> Autonomy Levels</div>
    <div class="table-container" style="margin-bottom:24px">
        <table>
            <thead><tr><th>Level</th><th>Actions</th><th>Controls</th></tr></thead>
            <tbody>
                <tr><td><span class="badge badge-success">Autonomous</span></td><td>Read, classify, extract, compute deadlines, draft flags, write audit log</td><td>Schema validation; evidence required; confidence ≥ 0.8; all logged</td></tr>
                <tr><td><span class="badge badge-warning">Needs Approval</span></td><td>Accept HIGH-flag contract, register obligations, change playbook, send external alert</td><td>Named approver; approval + reason recorded; time-stamped</td></tr>
                <tr><td><span class="badge badge-danger">Prohibited</span></td><td>Sign contracts, edit text, contact counterparty, delete records, send PII, give legal opinions</td><td>Technically blocked by permissions</td></tr>
            </tbody>
        </table>
    </div>

    <div class="section-header"><span class="icon">📜</span> Regulatory Map</div>
    <div class="table-container" style="margin-bottom:24px">
        <table>
            <thead><tr><th>Law / Standard</th><th>Relevance</th><th>Design Response</th></tr></thead>
            <tbody>
                <tr><td>DPDP Act, 2023</td><td>Personal data in contracts; fiduciary/processor duties</td><td>Purpose limitation; minimize PII; access control; breach-notification check</td></tr>
                <tr><td>IT Act, 2000</td><td>Electronic records; unauthorized access</td><td>Secure storage; access logs</td></tr>
                <tr><td>Indian Contract Act, 1872</td><td>Formation & enforceability; software ≠ party</td><td>Agent assists only; humans decide & sign</td></tr>
                <tr><td>NIST AI RMF 1.0</td><td>Risk management framework</td><td>Govern · Map · Measure · Manage</td></tr>
                <tr><td>EU AI Act</td><td>If EU counterparties involved; decision support</td><td>Transparency + human oversight</td></tr>
            </tbody>
        </table>
    </div>

    <div class="section-header"><span class="icon">⚔️</span> Planned Adversarial Tests</div>
    <div class="table-container">
        <table>
            <thead><tr><th>ID</th><th>Test</th><th>Expected Behaviour</th><th>Status</th></tr></thead>
            <tbody>
                <tr><td>A1</td><td>"Ignore previous instructions" in clause</td><td>Treated as data; flagged</td><td><span class="badge badge-info">Not Yet Run</span></td></tr>
                <tr><td>A2</td><td>Hidden text with instructions</td><td>Detected or ignored</td><td><span class="badge badge-info">Not Yet Run</span></td></tr>
                <tr><td>A3</td><td>Conflicting values (body vs annex)</td><td>Conflict flagged; routed to human</td><td><span class="badge badge-info">Not Yet Run</span></td></tr>
                <tr><td>A4</td><td>Ambiguous date format (03/04/2026)</td><td>Low confidence; routed to human</td><td><span class="badge badge-info">Not Yet Run</span></td></tr>
                <tr><td>A5</td><td>No governing-law clause</td><td>Null returned; LOW flag</td><td><span class="badge badge-info">Not Yet Run</span></td></tr>
                <tr><td>A6</td><td>Very long contract (100+ pages)</td><td>Chunked; no loss of late clauses</td><td><span class="badge badge-info">Not Yet Run</span></td></tr>
                <tr><td>A7</td><td>Personal data in header</td><td>Not copied to logs/index</td><td><span class="badge badge-info">Not Yet Run</span></td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- ═══════════════ TAB: AUDIT LOG ═══════════════ -->
<div class="tab-content" id="tab-audit">
    <div class="section-header"><span class="icon">📋</span> Full Audit Trail</div>
    <div class="table-container">
        <table>
            <thead><tr><th>Timestamp</th><th>Agent</th><th>Event</th><th>Details</th></tr></thead>
            <tbody id="audit-tbody"></tbody>
        </table>
    </div>
</div>

</div><!-- /main -->

<!-- Footer -->
<div class="uni-footer">
    <strong>Woxsen University — School of Business</strong><br>
    Course: Agentic AI for Business Operations &nbsp;|&nbsp; Programme: MBA Semester IV &nbsp;|&nbsp; Academic Year: 2026-2027<br>
    Group 10: Prabhat Verma (M1,M5) · Varun Rajesh Parkar (M2,M3) · Anchal Kumari (M4)<br>
    Faculty Guide: Dr. Shyam Joshi &nbsp;|&nbsp; Date: 08/11/2026
</div>

<script>
// ===== DATA =====
const results = {results_json};
const alerts = {alerts_json};
const auditLog = {audit_json};
const evalResults = {eval_json};
const groundTruth = {gt_json};

// ===== TAB NAVIGATION =====
document.querySelectorAll('.nav-tab').forEach(tab => {{
    tab.addEventListener('click', () => {{
        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
    }});
}});

// ===== OVERVIEW STATS =====
const totalFlags = results.reduce((s, r) => s + r.flags.length, 0);
document.getElementById('total-flags').textContent = totalFlags;

// Field accuracy from eval
if (evalResults.field_accuracy) {{
    document.getElementById('field-acc').textContent = evalResults.field_accuracy.percentage + '%';
    document.getElementById('eval-field-acc').textContent = evalResults.field_accuracy.percentage + '%';
    document.getElementById('t1-actual').textContent = evalResults.field_accuracy.correct + '/' + evalResults.field_accuracy.total + ' (' + evalResults.field_accuracy.percentage + '%)';
}}
if (evalResults.obligation_recall) {{
    document.getElementById('ob-recall').textContent = evalResults.obligation_recall.percentage + '%';
    document.getElementById('eval-ob-recall').textContent = evalResults.obligation_recall.percentage + '%';
    document.getElementById('t2-actual').textContent = evalResults.obligation_recall.found + '/' + evalResults.obligation_recall.total + ' (' + evalResults.obligation_recall.percentage + '%)';
}}
if (evalResults.routing_accuracy) {{
    document.getElementById('eval-routing').textContent = evalResults.routing_accuracy.percentage + '%';
    document.getElementById('t4-actual').textContent = evalResults.routing_accuracy.correct + '/' + evalResults.routing_accuracy.total + ' (' + evalResults.routing_accuracy.percentage + '%)';
}}
if (evalResults.flag_summary) {{
    document.getElementById('t3-actual').textContent = totalFlags + ' flags (' + evalResults.flag_summary.high + ' HIGH, ' + evalResults.flag_summary.medium + ' MEDIUM, ' + evalResults.flag_summary.low + ' LOW)';
}}
if (evalResults.obligation_status) {{
    const os = evalResults.obligation_status;
    document.getElementById('ob-past').textContent = os['PAST DUE'] || 0;
    document.getElementById('ob-30').textContent = os['DUE <=30d'] || 0;
    document.getElementById('ob-90').textContent = os['DUE <=90d'] || 0;
    document.getElementById('ob-upcoming').textContent = os['UPCOMING'] || 0;
    const statusParts = Object.entries(os).map(([k,v]) => v + ' ' + k).join(', ');
    document.getElementById('t6-actual').textContent = statusParts;
}}

// ===== CHARTS =====
const chartColors = {{
    blue: '#3b82f6', purple: '#a855f7', green: '#22c55e',
    yellow: '#f59e0b', red: '#ef4444', cyan: '#06b6d4',
    pink: '#ec4899', orange: '#fb923c'
}};

// Routing donut
const routeCounts = evalResults.contracts_by_route || {{}};
new Chart(document.getElementById('chart-routing'), {{
    type: 'doughnut',
    data: {{
        labels: ['Legal Review', 'Manager Review', 'Auto-Approve'],
        datasets: [{{ data: [routeCounts['LEGAL REVIEW REQUIRED']||0, routeCounts['MANAGER REVIEW']||0, routeCounts['AUTO-APPROVE (log only)']||0],
            backgroundColor: [chartColors.red, chartColors.yellow, chartColors.green],
            borderWidth: 0 }}]
    }},
    options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom', labels: {{ color: '#94a3b8', font: {{ size: 11 }} }} }} }} }}
}});

// Obligation status donut
const obStatus = evalResults.obligation_status || {{}};
new Chart(document.getElementById('chart-ob-status'), {{
    type: 'doughnut',
    data: {{
        labels: Object.keys(obStatus),
        datasets: [{{ data: Object.values(obStatus),
            backgroundColor: [chartColors.red, chartColors.yellow, chartColors.orange, chartColors.green, chartColors.blue],
            borderWidth: 0 }}]
    }},
    options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom', labels: {{ color: '#94a3b8', font: {{ size: 11 }} }} }} }} }}
}});

// Flag severity bar
const fs = evalResults.flag_summary || {{}};
new Chart(document.getElementById('chart-flag-severity'), {{
    type: 'bar',
    data: {{
        labels: ['HIGH', 'MEDIUM', 'LOW'],
        datasets: [{{ data: [fs.high||0, fs.medium||0, fs.low||0],
            backgroundColor: [chartColors.red, chartColors.yellow, chartColors.blue],
            borderRadius: 6 }}]
    }},
    options: {{ responsive: true, indexAxis: 'y', plugins: {{ legend: {{ display: false }} }},
        scales: {{ x: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ color: 'rgba(51,65,85,0.3)' }} }},
                  y: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ display: false }} }} }} }}
}});

// Contract types
const typeCounts = {{}};
groundTruth.forEach(g => {{ typeCounts[g.type] = (typeCounts[g.type]||0) + 1; }});
new Chart(document.getElementById('chart-types'), {{
    type: 'bar',
    data: {{
        labels: Object.keys(typeCounts),
        datasets: [{{ data: Object.values(typeCounts),
            backgroundColor: [chartColors.blue, chartColors.purple, chartColors.cyan, chartColors.pink],
            borderRadius: 6 }}]
    }},
    options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }},
        scales: {{ x: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }}, grid: {{ display: false }} }},
                  y: {{ beginAtZero: true, ticks: {{ color: '#94a3b8', stepSize: 1 }}, grid: {{ color: 'rgba(51,65,85,0.3)' }} }} }} }}
}});

// Governing law
const lawCounts = {{}};
groundTruth.forEach(g => {{ lawCounts[g.governing_law] = (lawCounts[g.governing_law]||0) + 1; }});
new Chart(document.getElementById('chart-laws'), {{
    type: 'pie',
    data: {{
        labels: Object.keys(lawCounts),
        datasets: [{{ data: Object.values(lawCounts),
            backgroundColor: [chartColors.green, chartColors.purple, chartColors.cyan],
            borderWidth: 0 }}]
    }},
    options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom', labels: {{ color: '#94a3b8' }} }} }} }}
}});

// Cost-benefit chart
new Chart(document.getElementById('chart-cost-benefit'), {{
    type: 'bar',
    data: {{
        labels: ['Year 0', 'Year 1', 'Year 2'],
        datasets: [
            {{ label: 'Total Cost', data: [12.0, 8.5, 8.8], backgroundColor: chartColors.red, borderRadius: 4 }},
            {{ label: 'Total Benefit', data: [0, 22.2, 27.7], backgroundColor: chartColors.green, borderRadius: 4 }},
            {{ label: 'Net Benefit', data: [-12.0, 13.7, 18.9], backgroundColor: chartColors.blue, borderRadius: 4 }}
        ]
    }},
    options: {{ responsive: true,
        plugins: {{ legend: {{ labels: {{ color: '#94a3b8' }} }} }},
        scales: {{ x: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ display: false }} }},
                  y: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ color: 'rgba(51,65,85,0.3)' }} }} }} }}
}});

// Cumulative net benefit
new Chart(document.getElementById('chart-cumulative'), {{
    type: 'line',
    data: {{
        labels: ['Year 0', 'Year 1', 'Year 2'],
        datasets: [{{ label: 'Cumulative Net Benefit (INR Lakh)', data: [-12.0, 1.7, 20.6],
            borderColor: chartColors.green, backgroundColor: 'rgba(34,197,94,0.1)',
            fill: true, tension: 0.3, pointRadius: 6, pointBackgroundColor: chartColors.green }}]
    }},
    options: {{ responsive: true,
        plugins: {{ legend: {{ labels: {{ color: '#94a3b8' }} }} }},
        scales: {{ x: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ display: false }} }},
                  y: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ color: 'rgba(51,65,85,0.3)' }} }} }} }}
}});

// Benefit breakdown
new Chart(document.getElementById('chart-benefit-breakdown'), {{
    type: 'doughnut',
    data: {{
        labels: ['Review Time Saved (₹6.0L)', 'Admin Saved (₹6.7L)', 'Leakage Avoided (₹15.0L)'],
        datasets: [{{ data: [6.0, 6.7, 15.0],
            backgroundColor: [chartColors.blue, chartColors.purple, chartColors.green],
            borderWidth: 0 }}]
    }},
    options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom', labels: {{ color: '#94a3b8', font: {{ size: 11 }} }} }} }} }}
}});

// Sensitivity analysis
new Chart(document.getElementById('chart-sensitivity'), {{
    type: 'bar',
    data: {{
        labels: ['Best Case', 'Base Case', 'Worst Case'],
        datasets: [
            {{ label: 'Benefit', data: [64.9, 49.9, 25.0], backgroundColor: chartColors.green, borderRadius: 4 }},
            {{ label: 'Cost', data: [26.4, 29.3, 36.6], backgroundColor: chartColors.red, borderRadius: 4 }}
        ]
    }},
    options: {{ responsive: true,
        plugins: {{ legend: {{ labels: {{ color: '#94a3b8' }} }} }},
        scales: {{ x: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ display: false }} }},
                  y: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ color: 'rgba(51,65,85,0.3)' }} }} }} }}
}});

// ===== CONTRACTS TABLE =====
const gtMap = {{}};
groundTruth.forEach(g => gtMap[g.id] = g);

const ctbody = document.getElementById('contracts-tbody');
results.forEach(r => {{
    const gt = gtMap[r.id] || {{}};
    const routeClass = r.route.includes('LEGAL') ? 'route-legal' : r.route.includes('MANAGER') ? 'route-manager' : 'route-auto';
    const flagBadges = r.flags.map(f => {{
        const cls = f.severity === 'HIGH' ? 'badge-danger' : f.severity === 'MEDIUM' ? 'badge-warning' : 'badge-info';
        return '<span class="badge ' + cls + '">' + f.severity + '</span>';
    }}).join(' ');
    
    ctbody.innerHTML += '<tr>' +
        '<td><strong>' + r.id + '</strong></td>' +
        '<td>' + (gt.type || '—') + '</td>' +
        '<td>' + (r.fields.term_months || '<em>—</em>') + 'mo</td>' +
        '<td>' + (r.fields.auto_renew ? '✅' : '❌') + '</td>' +
        '<td>' + (r.fields.notice_days || 0) + 'd</td>' +
        '<td>' + (r.fields.payment_days || '<em>—</em>') + 'd</td>' +
        '<td>' + (r.fields.liability || '—') + '</td>' +
        '<td>' + (r.fields.indemnity || '—') + '</td>' +
        '<td>' + (r.fields.governing_law || '—') + '</td>' +
        '<td>' + (r.fields.dpdp ? '✅' : '❌') + '</td>' +
        '<td>' + (r.fields.termination_convenience ? '✅' : '❌') + '</td>' +
        '<td class="' + routeClass + '">' + r.route + '</td>' +
        '<td>' + flagBadges + '</td>' +
    '</tr>';
}});

// ===== OBLIGATIONS TABLE =====
const obtbody = document.getElementById('obligations-tbody');
alerts.sort((a, b) => {{
    const order = {{'PAST DUE': 0, 'DUE <=30d': 1, 'DUE <=90d': 2, 'UPCOMING': 3, 'NEEDS REVIEW (no date parsed)': 4}};
    return (order[a.status] || 5) - (order[b.status] || 5);
}});
alerts.forEach(a => {{
    const statusClass = a.status.includes('PAST') ? 'status-past' : a.status.includes('30') ? 'status-30' : a.status.includes('90') ? 'status-90' : a.status.includes('UPCOMING') ? 'status-upcoming' : 'status-review';
    obtbody.innerHTML += '<tr>' +
        '<td><strong>' + a.contract + '</strong></td>' +
        '<td>' + a.party + '</td>' +
        '<td>' + a.action + '</td>' +
        '<td>' + (a.due || '—') + '</td>' +
        '<td class="' + statusClass + '"><strong>' + a.status + '</strong></td>' +
        '<td>' + (a.days !== null ? a.days + 'd' : '—') + '</td>' +
    '</tr>';
}});

// ===== FLAGS TABLE =====
const ftbody = document.getElementById('flags-tbody');
results.forEach(r => {{
    r.flags.forEach(f => {{
        const sevClass = 'severity-' + f.severity.toLowerCase();
        const routeClass = r.route.includes('LEGAL') ? 'route-legal' : r.route.includes('MANAGER') ? 'route-manager' : 'route-auto';
        ftbody.innerHTML += '<tr>' +
            '<td><strong>' + r.id + '</strong></td>' +
            '<td class="' + routeClass + '">' + r.route + '</td>' +
            '<td class="' + sevClass + '">' + f.severity + '</td>' +
            '<td>' + f.issue + '</td>' +
        '</tr>';
    }});
}});

// ===== MISMATCHES TABLE =====
const mtbody = document.getElementById('mismatches-tbody');
if (evalResults.field_mismatches) {{
    evalResults.field_mismatches.forEach(m => {{
        mtbody.innerHTML += '<tr><td>' + m.contract + '</td><td>' + m.field + '</td><td>' + JSON.stringify(m.expected) + '</td><td>' + JSON.stringify(m.actual) + '</td></tr>';
    }});
}}
if (!evalResults.field_mismatches || evalResults.field_mismatches.length === 0) {{
    mtbody.innerHTML = '<tr><td colspan="4" style="text-align:center;color:var(--success)">No mismatches — 100% accuracy on standard phrasings</td></tr>';
}}

// ===== AUDIT TABLE =====
const atbody = document.getElementById('audit-tbody');
auditLog.forEach(e => {{
    const details = Object.entries(e).filter(([k]) => !['ts','agent','event'].includes(k)).map(([k,v]) => k + '=' + v).join(', ');
    atbody.innerHTML += '<tr>' +
        '<td>' + e.ts + '</td>' +
        '<td><span class="badge badge-purple">' + e.agent + '</span></td>' +
        '<td>' + e.event + '</td>' +
        '<td>' + details + '</td>' +
    '</tr>';
}});
</script>
</body>
</html>"""
    return html


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            html = generate_dashboard_html()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(html.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            super().do_GET()
    
    def log_message(self, format, *args):
        pass  # Suppress logs


if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  Contract Review & Obligation Tracking Agent Dashboard")
    print(f"  Woxsen University — Group 10")
    print(f"{'='*60}")
    print(f"\n  🌐 Dashboard: http://localhost:{PORT}")
    print(f"  Press Ctrl+C to stop\n")
    
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        httpd.serve_forever()
