"""
Video Generator for Agentic AI Contract Review & Obligation Tracking Solution
Produces an HD animated infographic video (1920x1080 MP4, ~2.5 mins).
"""
import os, subprocess, json
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
OUTPUT_DIR = r"C:\Users\varun\.gemini\antigravity\scratch\contract-dashboard\video_assets"
VIDEO_PATH = r"C:\Users\varun\.gemini\antigravity\scratch\contract-dashboard\demo_explainer_video.mp4"

WIDTH, HEIGHT = 1920, 1080
FPS = 24

# Colors
BG_DARK = (15, 23, 42)        # #0f172a
CARD_BG = (30, 41, 59)        # #1e293b
CARD_BORDER = (51, 65, 85)    # #334155
TEXT_WHITE = (248, 250, 252)  # #f8fafc
TEXT_MUTED = (148, 163, 184)  # #94a3b8
BLUE_ACCENT = (59, 130, 246)  # #3b82f6
GREEN_SUCCESS = (34, 197, 94) # #22c55e
AMBER_WARN = (245, 158, 11)   # #f59e0b
RED_ALERT = (239, 68, 68)     # #ef4444
PURPLE_BRAND = (168, 85, 247) # #a855f7
CYAN_INFO = (6, 182, 212)     # #06b6d4

def get_font(size, bold=False):
    font_names = [
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
    ]
    for fn in font_names:
        if os.path.exists(fn):
            try:
                return ImageFont.truetype(fn, size)
            except Exception:
                pass
    return ImageFont.load_default()

FONT_TITLE = get_font(52, bold=True)
FONT_SUBTITLE = get_font(32, bold=False)
FONT_HEADING = get_font(36, bold=True)
FONT_BODY = get_font(26, bold=False)
FONT_BODY_BOLD = get_font(26, bold=True)
FONT_SMALL = get_font(20, bold=False)
FONT_METRIC = get_font(68, bold=True)

def draw_header(draw, title, subtitle):
    # Top banner
    draw.rectangle([(0, 0), (WIDTH, 120)], fill=CARD_BG)
    draw.line([(0, 120), (WIDTH, 120)], fill=CARD_BORDER, width=2)
    # Badge
    draw.rounded_rectangle([(60, 28), (120, 88)], radius=12, fill=BLUE_ACCENT)
    draw.text((75, 40), "AI", font=FONT_HEADING, fill=TEXT_WHITE)
    # Titles
    draw.text((140, 30), title, font=FONT_HEADING, fill=TEXT_WHITE)
    draw.text((140, 75), subtitle, font=FONT_SMALL, fill=TEXT_MUTED)
    # Woxsen logo/text on right
    draw.text((WIDTH - 420, 48), "WOXSEN UNIVERSITY | GROUP 10", font=FONT_SMALL, fill=TEXT_MUTED)

def draw_footer(draw, current_scene, total_scenes=8):
    # Bottom progress bar
    draw.line([(0, HEIGHT - 20), (WIDTH, HEIGHT - 20)], fill=CARD_BORDER, width=4)
    prog_w = int((current_scene / total_scenes) * WIDTH)
    draw.line([(0, HEIGHT - 20), (prog_w, HEIGHT - 20)], fill=BLUE_ACCENT, width=4)
    draw.text((60, HEIGHT - 55), "Contract Review & Obligation Tracking Agent • Academic Demonstration", font=FONT_SMALL, fill=TEXT_MUTED)

def create_card(img, draw, x, y, w, h, title="", border_color=CARD_BORDER, bg_color=CARD_BG):
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=16, fill=bg_color, outline=border_color, width=2)
    if title:
        draw.text((x + 24, y + 20), title, font=FONT_BODY_BOLD, fill=BLUE_ACCENT)

# ----------------- SCENE BUILDERS -----------------

def scene_1_title():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    # Hero Title Box
    draw.rounded_rectangle([(260, 200), (1660, 740)], radius=24, fill=CARD_BG, outline=BLUE_ACCENT, width=3)
    
    # Institution
    draw.text((360, 250), "WOXSEN UNIVERSITY • SCHOOL OF BUSINESS", font=FONT_BODY_BOLD, fill=BLUE_ACCENT)
    draw.text((360, 290), "Course: Agentic AI for Business Operations • MBA Semester IV", font=FONT_SMALL, fill=TEXT_MUTED)
    
    # Project Title
    draw.text((360, 360), "AGENTIC AI SOLUTION FOR CONTRACT REVIEW", font=FONT_TITLE, fill=TEXT_WHITE)
    draw.text((360, 430), "& OBLIGATION TRACKING", font=FONT_TITLE, fill=CYAN_INFO)
    
    # Subtitle
    draw.text((360, 520), "End-to-End Autonomous Multi-Agent Architecture with Human-in-the-Loop Governance", font=FONT_SUBTITLE, fill=TEXT_MUTED)
    
    # Team Credits
    draw.line([(360, 590), (1560, 590)], fill=CARD_BORDER, width=2)
    draw.text((360, 620), "Group 10 Team:", font=FONT_BODY_BOLD, fill=TEXT_WHITE)
    draw.text((360, 660), "Prabhat Verma (M1, M5)   •   Varun Rajesh Parkar (M2, M3)   •   Anchal Kumari (M4)", font=FONT_BODY, fill=TEXT_MUTED)
    draw.text((1200, 660), "Faculty Guide: Dr. Shyam Joshi", font=FONT_BODY_BOLD, fill=AMBER_WARN)
    
    draw_footer(draw, 1)
    return img

def scene_2_problem():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "1. THE PROBLEM: Commercial Contract Management Leakage", "Baseline Challenges Identified in Mid-Sized Indian Enterprises (600 Active Contracts)")
    
    # 3 Stat Metric Cards
    cards_data = [
        ("4.0 Hours", "Manual Review Time", "Each commercial agreement requires tedious human reading across 12+ clauses.", RED_ALERT),
        ("6% Missed", "Obligations Late/Missed", "Notice periods buried in auto-renewal clauses lead to unintentional annual lock-in.", AMBER_WARN),
        ("9% Revenue", "Eroded Through Leakage", "World Commerce & Contracting (WorldCC) benchmark on contract management gaps.", PURPLE_BRAND)
    ]
    
    for i, (metric, label, desc, color) in enumerate(cards_data):
        x = 100 + i * 590
        draw.rounded_rectangle([(x, 180), (x + 540, 420)], radius=16, fill=CARD_BG, outline=color, width=2)
        draw.text((x + 30, 210), metric, font=FONT_METRIC, fill=color)
        draw.text((x + 30, 290), label, font=FONT_BODY_BOLD, fill=TEXT_WHITE)
        draw.text((x + 30, 335), desc, font=FONT_SMALL, fill=TEXT_MUTED)
    
    # Process Gap Infographic
    create_card(img, draw, 100, 470, 1720, 480, "As-Is Process Pain Points & Root Cause (5 Whys Analysis)")
    
    steps = [
        ("1. Contract Intake", "PDF/Word emails arrive without standardization", RED_ALERT),
        ("2. Manual Reading", "Inconsistent review quality depending on fatigue", RED_ALERT),
        ("3. Excel Keying", "Copy-paste error; buried dates missed completely", RED_ALERT),
        ("4. Unchecked Risk", "Playbook deviations on Liability & DPDP pass unnoticed", RED_ALERT),
        ("5. Scattered Reminders", "Personal calendar entries disappear with employee turnover", RED_ALERT)
    ]
    
    for i, (title, sub, col) in enumerate(steps):
        sx = 140 + i * 325
        draw.rounded_rectangle([(sx, 560), (sx + 295, 840)], radius=12, fill=(20, 30, 48), outline=col, width=2)
        draw.text((sx + 20, 590), title, font=FONT_BODY_BOLD, fill=col)
        draw.text((sx + 20, 650), sub, font=FONT_SMALL, fill=TEXT_MUTED)
        if i < 4:
            draw.text((sx + 305, 680), "➔", font=FONT_HEADING, fill=CARD_BORDER)
            
    draw_footer(draw, 2)
    return img

def scene_3_architecture():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "2. THE SOLUTION: Supervisor-Worker Multi-Agent Architecture", "LangGraph-Aligned Sequential Orchestration with Least-Privilege Isolation")
    
    # Supervisor Box
    draw.rounded_rectangle([(700, 160), (1220, 270)], radius=16, fill=(30, 58, 138), outline=BLUE_ACCENT, width=3)
    draw.text((740, 185), "🎯 SUPERVISOR AGENT", font=FONT_HEADING, fill=TEXT_WHITE)
    draw.text((740, 230), "Plan • Delegate • Route • Retry • Escalate", font=FONT_SMALL, fill=CYAN_INFO)
    
    # Down Arrows
    draw.text((950, 280), "▼", font=FONT_HEADING, fill=BLUE_ACCENT)
    
    # 4 Worker Agents
    workers = [
        ("📥 Intake & Classify", "Identifies contract type, parties, quality, and effective dates.", CYAN_INFO),
        ("🔍 Clause Extraction", "Extracts 9 key fields + quoted evidence spans + confidence scores.", BLUE_ACCENT),
        ("⚖️ Risk Review Agent", "Compares values against 6 playbook rules; assigns severity.", AMBER_WARN),
        ("⏰ Obligation Tracker", "Calculates non-renewal deadlines; schedules alerts T-30/T-7.", GREEN_SUCCESS)
    ]
    
    for i, (name, role, col) in enumerate(workers):
        wx = 80 + i * 445
        draw.rounded_rectangle([(wx, 340), (wx + 415, 520)], radius=14, fill=CARD_BG, outline=col, width=2)
        draw.text((wx + 20, 365), name, font=FONT_BODY_BOLD, fill=col)
        draw.text((wx + 20, 420), role, font=FONT_SMALL, fill=TEXT_MUTED)
    
    # Human Gate Box
    draw.text((950, 535), "▼", font=FONT_HEADING, fill=AMBER_WARN)
    draw.rounded_rectangle([(520, 590), (1400, 720)], radius=16, fill=(74, 4, 4), outline=RED_ALERT, width=2)
    draw.text((560, 615), "🛡️ HUMAN-IN-THE-LOOP APPROVAL GATE", font=FONT_HEADING, fill=TEXT_WHITE)
    draw.text((560, 665), "HC1: Legal Review (High Risk)  •  HC2: Manager Review  •  HC4: Obligation Sign-off", font=FONT_BODY, fill=AMBER_WARN)
    
    # Bottom Stores
    stores = [
        ("📁 Contract Store", "Raw text, clean JSON"),
        ("🔎 Playbook Rules", "6 corporate legal rules"),
        ("🗄️ Obligation DB", "Persistent SQLite / Postgres"),
        ("📋 Audit Trail", "Immutable action logs")
    ]
    for i, (sname, sdesc) in enumerate(stores):
        sx = 80 + i * 445
        draw.rounded_rectangle([(sx, 770), (sx + 415, 920)], radius=12, fill=(15, 25, 40), outline=CARD_BORDER, width=1)
        draw.text((sx + 24, 800), sname, font=FONT_BODY_BOLD, fill=TEXT_WHITE)
        draw.text((sx + 24, 850), sdesc, font=FONT_SMALL, fill=TEXT_MUTED)
        
    draw_footer(draw, 3)
    return img

def scene_4_worked_example():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "3. WORKED EXAMPLE: Contract C03 In Action", "Supply Agreement between Deccan Auto Components & Helix Components")
    
    # Left Box: Extracted Fields
    create_card(img, draw, 80, 160, 840, 790, "Extracted Fields (Clause Extraction Agent)")
    fields = [
        ("Agreement Type", "Supply Agreement", GREEN_SUCCESS),
        ("Term", "36 Months (to 21 March 2029)", TEXT_WHITE),
        ("Auto-Renewal", "Yes, 60 days non-renewal notice", AMBER_WARN),
        ("Payment Terms", "45 days from receipt of invoice", GREEN_SUCCESS),
        ("Liability Limit", "UNLIMITED (Supplier)", RED_ALERT),
        ("Indemnity", "Mutual Indemnity", GREEN_SUCCESS),
        ("Data Protection", "Digital Personal Data Protection Act, 2023", GREEN_SUCCESS),
        ("Governing Law", "Singapore (Non-approved jurisdiction)", AMBER_WARN),
    ]
    for i, (k, v, c) in enumerate(fields):
        y = 230 + i * 65
        draw.text((110, y), k, font=FONT_BODY_BOLD, fill=TEXT_MUTED)
        draw.text((420, y), v, font=FONT_BODY, fill=c)
        draw.line([(110, y + 45), (880, y + 45)], fill=CARD_BORDER, width=1)
    
    # Right Top Box: Risk Flags Raised
    create_card(img, draw, 960, 160, 880, 360, "Playbook Risk Review Flags Raised")
    flags = [
        ("🔴 HIGH SEVERITY", "Unlimited liability under Clause 4 (Breaches R-LIAB)", RED_ALERT),
        ("🟡 MEDIUM SEVERITY", "Non-approved governing law: Singapore (Breaches R-LAW)", AMBER_WARN),
        ("➡️ ROUTING DECISION", "LEGAL REVIEW REQUIRED (Escalated to General Counsel)", CYAN_INFO)
    ]
    for i, (tag, detail, col) in enumerate(flags):
        fy = 230 + i * 85
        draw.text((990, fy), tag, font=FONT_BODY_BOLD, fill=col)
        draw.text((990, fy + 35), detail, font=FONT_BODY, fill=TEXT_WHITE)
    
    # Right Bottom Box: Obligations Computed
    create_card(img, draw, 960, 560, 880, 390, "Registered & Computed Obligations")
    obs = [
        ("Supplier: Deliver Phase 1 Deliverables", "Due 2026-07-06  •  PAST DUE (Action Required)", RED_ALERT),
        ("Supplier: Submit Phase 2 Report", "Due 2026-10-05  •  PAST DUE (Confirm completion)", RED_ALERT),
        ("Either: Send Notice of Non-Renewal", "Due 2029-01-20 (End - 60d)  •  UPCOMING", GREEN_SUCCESS)
    ]
    for i, (action, status, col) in enumerate(obs):
        oy = 630 + i * 90
        draw.text((990, oy), action, font=FONT_BODY_BOLD, fill=TEXT_WHITE)
        draw.text((990, oy + 35), status, font=FONT_BODY, fill=col)
        
    draw_footer(draw, 4)
    return img

def scene_5_evaluation():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "4. TESTING & EVALUATION: Empirical Benchmark Results", "Verified on 10 Synthetic Agreements across Test Suite T1 through T6")
    
    # 4 Scorecards
    scorecards = [
        ("97.8%", "FIELD ACCURACY (T1)", "88 of 90 fields correct\nTarget: >= 95% (PASS)", GREEN_SUCCESS),
        ("96.9%", "OBLIGATION RECALL (T2)", "31 of 32 captured\n100% Precision (PASS)", GREEN_SUCCESS),
        ("100%", "FLAG DETECTION (T3)", "22 of 22 flags raised\n5 High, 15 Med, 2 Low", CYAN_INFO),
        ("100%", "ROUTING ACCURACY (T4)", "10 of 10 routed correctly\n5 Legal, 4 Manager, 1 Auto", PURPLE_BRAND)
    ]
    for i, (pct, label, desc, col) in enumerate(scorecards):
        x = 80 + i * 445
        draw.rounded_rectangle([(x, 160), (x + 415, 360)], radius=16, fill=CARD_BG, outline=col, width=2)
        draw.text((x + 24, 190), pct, font=FONT_METRIC, fill=col)
        draw.text((x + 24, 275), label, font=FONT_BODY_BOLD, fill=TEXT_WHITE)
        draw.text((x + 24, 310), desc, font=FONT_SMALL, fill=TEXT_MUTED)
    
    # Test Suite Matrix Table
    create_card(img, draw, 80, 400, 1760, 550, "Full Verification Matrix (Module M3 Report Table 4.4)")
    
    headers = [("Test", 120), ("Scenario", 480), ("Expected Benchmark", 350), ("Measured Prototype Result", 450), ("Verdict", 180)]
    th_x = 120
    for htitle, hw in headers:
        draw.text((th_x, 460), htitle, font=FONT_BODY_BOLD, fill=BLUE_ACCENT)
        th_x += hw
    draw.line([(110, 500), (1800, 500)], fill=CARD_BORDER, width=2)
    
    trows = [
        ("T1", "Extract 9 key commercial fields", ">= 95% field accuracy", "88 / 90 correct (97.8%)", "PASS", GREEN_SUCCESS),
        ("T2", "Capture dated obligations + renewal dates", ">= 95% recall, 0 false pos.", "31 / 32 captured (96.9%)", "PASS", GREEN_SUCCESS),
        ("T3", "Check fields vs 6-rule legal playbook", "All expected flags raised", "22 / 22 flags detected", "PASS", GREEN_SUCCESS),
        ("T4", "Risk-based supervisor routing", "Route matches risk tier", "10 / 10 correct routes", "PASS", GREEN_SUCCESS),
        ("T5", "Adversarial & irregular wording tests", "Visible fallback, no guessing", "All 3 flagged for human check", "SAFE FAIL", AMBER_WARN),
        ("T6", "Temporal obligation status categorization", "Accurate date arithmetic", "24 Past, 1 <=90d, 5 Upcoming", "PASS", GREEN_SUCCESS),
    ]
    for i, (tid, sc, exp, act, verd, vcol) in enumerate(trows):
        ry = 525 + i * 65
        draw.text((120, ry), tid, font=FONT_BODY_BOLD, fill=TEXT_WHITE)
        draw.text((240, ry), sc, font=FONT_BODY, fill=TEXT_WHITE)
        draw.text((720, ry), exp, font=FONT_BODY, fill=TEXT_MUTED)
        draw.text((1070, ry), act, font=FONT_BODY, fill=TEXT_WHITE)
        draw.rounded_rectangle([(1520, ry - 5), (1670, ry + 35)], radius=8, fill=CARD_BG, outline=vcol, width=2)
        draw.text((1540, ry), verd, font=FONT_BODY_BOLD, fill=vcol)
        draw.line([(110, ry + 50), (1800, ry + 50)], fill=CARD_BORDER, width=1)
        
    draw_footer(draw, 5)
    return img

def scene_6_governance():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "5. GOVERNANCE, RISK & REGULATION (NIST AI RMF & DPDP)", "Institutional Safety Guardrails, Autonomy Boundaries, and Statutory Compliance")
    
    # 3 Autonomy Tiers
    draw.rounded_rectangle([(80, 160), (620, 520)], radius=16, fill=CARD_BG, outline=GREEN_SUCCESS, width=2)
    draw.text((110, 190), "🟢 AUTONOMOUS", font=FONT_HEADING, fill=GREEN_SUCCESS)
    draw.text((110, 240), "Tasks the Agent Performs Solo:", font=FONT_BODY_BOLD, fill=TEXT_WHITE)
    auto_items = ["• Read & parse contract structure", "• Extract 9 fields with quoted evidence", "• Compute notice dates deterministically", "• Log all actions to immutable audit log"]
    for i, it in enumerate(auto_items):
        draw.text((110, 290 + i * 45), it, font=FONT_SMALL, fill=TEXT_MUTED)
        
    draw.rounded_rectangle([(670, 160), (1210, 520)], radius=16, fill=CARD_BG, outline=AMBER_WARN, width=2)
    draw.text((700, 190), "🟡 HUMAN APPROVAL", font=FONT_HEADING, fill=AMBER_WARN)
    draw.text((700, 240), "Requires Explicit Human Gate:", font=FONT_BODY_BOLD, fill=TEXT_WHITE)
    appr_items = ["• Approval of HIGH severity flags", "• Obligation owner confirmations", "• Changes to corporate legal playbook", "• Non-standard phrasing interpretation"]
    for i, it in enumerate(appr_items):
        draw.text((700, 290 + i * 45), it, font=FONT_SMALL, fill=TEXT_MUTED)
        
    draw.rounded_rectangle([(1260, 160), (1800, 520)], radius=16, fill=CARD_BG, outline=RED_ALERT, width=2)
    draw.text((1290, 190), "🔴 PROHIBITED", font=FONT_HEADING, fill=RED_ALERT)
    draw.text((1290, 240), "Technically Blocked from Doing:", font=FONT_BODY_BOLD, fill=TEXT_WHITE)
    proh_items = ["• Signing/accepting commercial contracts", "• Contacting external counterparties", "• Providing legal counsel or advice", "• Training external models on PII"]
    for i, it in enumerate(proh_items):
        draw.text((1290, 290 + i * 45), it, font=FONT_SMALL, fill=TEXT_MUTED)
        
    # Compliance Mapping Box
    create_card(img, draw, 80, 560, 1720, 390, "Statutory Alignment: DPDP Act 2023 & NIST AI RMF 1.0")
    
    cols = [
        ("Digital Personal Data Protection (DPDP) Act 2023", "Fiduciary & processor duty checks; mandatory DPDP clause verification; purpose limitation; PII sanitization in vector embeddings.", CYAN_INFO),
        ("NIST AI Risk Management Framework", "Govern (Named Legal accountable owner) • Map (Stakeholder risk register) • Measure (T1-T6 benchmarks) • Manage (Fail-safe routing & audit).", BLUE_ACCENT),
        ("Indian Contract Act, 1872 & IT Act, 2000", "Recognizes electronic contract records; software is never a party to agreements; humans retain sole signature authority.", PURPLE_BRAND)
    ]
    for i, (head, text, col) in enumerate(cols):
        cx = 120 + i * 550
        draw.rounded_rectangle([(cx, 630), (cx + 510, 890)], radius=12, fill=(15, 25, 42), outline=col, width=1)
        draw.text((cx + 20, 660), head, font=FONT_BODY_BOLD, fill=col)
        # wrap text
        words = text.split(" ")
        lines = []
        cur = ""
        for w in words:
            if len(cur + " " + w) < 36:
                cur += " " + w
            else:
                lines.append(cur)
                cur = w
        if cur: lines.append(cur)
        for j, ln in enumerate(lines):
            draw.text((cx + 20, 715 + j * 32), ln.strip(), font=FONT_SMALL, fill=TEXT_MUTED)
            
    draw_footer(draw, 6)
    return img

def scene_7_business_roi():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "6. BUSINESS IMPACT, ROI & ROADMAP (Module M5)", "Financial Viability and Rollout Plan for 600 Active Contracts")
    
    # 4 ROI Highlights
    roi_metrics = [
        ("₹49.9 Lakh", "TOTAL 2-YR BENEFIT", "Review time + Admin + Leakage avoided", GREEN_SUCCESS),
        ("₹29.3 Lakh", "TOTAL 3-YR COST", "Year 0 Build + Years 1 & 2 Maintenance", AMBER_WARN),
        ("70.3%", "2-YEAR ROI", "(Benefit - Cost) / Cost", BLUE_ACCENT),
        ("10.5 Mo", "PAYBACK PERIOD", "Breakeven achieved during Year 1", PURPLE_BRAND)
    ]
    for i, (val, title, sub, col) in enumerate(roi_metrics):
        x = 80 + i * 445
        draw.rounded_rectangle([(x, 160), (x + 415, 340)], radius=16, fill=CARD_BG, outline=col, width=2)
        draw.text((x + 24, 190), val, font=FONT_METRIC, fill=col)
        draw.text((x + 24, 265), title, font=FONT_BODY_BOLD, fill=TEXT_WHITE)
        draw.text((x + 24, 295), sub, font=FONT_SMALL, fill=TEXT_MUTED)
        
    # Cost-Benefit Table
    create_card(img, draw, 80, 380, 840, 570, "Cost-Benefit Breakdown (INR Lakh)")
    cbt_rows = [
        ("Development & Setup (Build)", "12.0", "0.0", "0.0"),
        ("Cloud & Model Running Cost", "0.0", "3.5", "3.8"),
        ("Oversight & Maintenance", "0.0", "5.0", "5.0"),
        ("Total Annual Cost", "12.0", "8.5", "8.8"),
        ("Review Time Saved", "0.0", "6.0", "6.0"),
        ("Admin Automation Saved", "0.0", "6.7", "6.7"),
        ("Leakage Avoided (2% -> 7.5%)", "0.0", "9.5", "15.0"),
        ("Total Annual Benefit", "0.0", "22.2", "27.7"),
        ("Cumulative Net Benefit", "-12.0", "+1.7", "+20.6")
    ]
    draw.text((110, 440), "Line Item", font=FONT_BODY_BOLD, fill=TEXT_WHITE)
    draw.text((540, 440), "Yr 0", font=FONT_BODY_BOLD, fill=TEXT_MUTED)
    draw.text((640, 440), "Yr 1", font=FONT_BODY_BOLD, fill=TEXT_MUTED)
    draw.text((740, 440), "Yr 2", font=FONT_BODY_BOLD, fill=TEXT_MUTED)
    draw.line([(100, 475), (880, 475)], fill=CARD_BORDER, width=2)
    
    for i, (item, y0, y1, y2) in enumerate(cbt_rows):
        ry = 495 + i * 48
        is_bold = "Total" in item or "Cumulative" in item
        f_use = FONT_BODY_BOLD if is_bold else FONT_BODY
        col_use = GREEN_SUCCESS if "Cumulative" in item else (TEXT_WHITE if is_bold else TEXT_MUTED)
        draw.text((110, ry), item, font=f_use, fill=col_use)
        draw.text((540, ry), y0, font=f_use, fill=col_use)
        draw.text((640, ry), y1, font=f_use, fill=col_use)
        draw.text((740, ry), y2, font=f_use, fill=col_use)
        
    # Phased Roadmap Box
    create_card(img, draw, 960, 380, 880, 570, "Implementation Roadmap & Milestones")
    phases = [
        ("PHASE 1: 8-Week Shadow Pilot (Months 1–3)", "60 contracts across 2 business units; side-by-side human comparison; 0 autonomy on risk.", CYAN_INFO),
        ("PHASE 2: Department Expansion (Months 4–9)", "All vendor agreements & NDAs; live obligation tracker integration; email alerts triggered.", BLUE_ACCENT),
        ("PHASE 3: Enterprise Scale (Months 10–18)", "Full ERP integration; auto-approval for clean contracts; live drift and accuracy audits.", GREEN_SUCCESS)
    ]
    for i, (pname, pdesc, pcol) in enumerate(phases):
        py = 460 + i * 160
        draw.rounded_rectangle([(990, py), (1780, py + 130)], radius=12, fill=(20, 30, 48), outline=pcol, width=2)
        draw.text((1020, py + 25), pname, font=FONT_BODY_BOLD, fill=pcol)
        draw.text((1020, py + 75), pdesc, font=FONT_SMALL, fill=TEXT_MUTED)
        
    draw_footer(draw, 7)
    return img

def scene_8_conclusion():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    draw.rounded_rectangle([(260, 160), (1660, 880)], radius=24, fill=CARD_BG, outline=BLUE_ACCENT, width=3)
    
    draw.text((340, 220), "SUMMARY & DEMO ACCESS", font=FONT_TITLE, fill=TEXT_WHITE)
    draw.text((340, 290), "All Project Artifacts Are Live, Open-Source & Independently Reproducible", font=FONT_SUBTITLE, fill=CYAN_INFO)
    
    links = [
        ("🌐 Interactive Dashboard", "http://localhost:8050", "9-tab interactive analytics suite with Chart.js visualization"),
        ("🐙 GitHub Repository", "https://github.com/Parkar6945/contract-review-obligation-agent", "Complete codebase, generator, agents, evaluator, tests & README"),
        ("📄 Comprehensive Report", "Agentic AI Solution for Contract Review & Obligation Tracking", "Full MBA academic submission covering modules M1 through M5")
    ]
    for i, (title, url, note) in enumerate(links):
        ly = 380 + i * 150
        draw.rounded_rectangle([(340, ly), (1580, ly + 120)], radius=12, fill=(15, 25, 42), outline=CARD_BORDER, width=1)
        draw.text((370, ly + 20), title, font=FONT_BODY_BOLD, fill=GREEN_SUCCESS)
        draw.text((370, ly + 55), url, font=FONT_BODY, fill=BLUE_ACCENT)
        draw.text((370, ly + 85), note, font=FONT_SMALL, fill=TEXT_MUTED)
        
    draw.text((340, 830), "Woxsen University • School of Business • Academic Year 2026-2027", font=FONT_BODY, fill=TEXT_MUTED)
    draw_footer(draw, 8)
    return img

# ----------------- MAIN RENDERER -----------------

def build_video():
    print("Generating scene frames...")
    scenes = [
        (scene_1_title(), 16),       # 16 sec
        (scene_2_problem(), 20),     # 20 sec
        (scene_3_architecture(), 24),# 24 sec
        (scene_4_worked_example(), 24),# 24 sec
        (scene_5_evaluation(), 24),  # 24 sec
        (scene_6_governance(), 20),  # 20 sec
        (scene_7_business_roi(), 20),# 20 sec
        (scene_8_conclusion(), 16),  # 16 sec
    ]
    # Total duration = 164 seconds = ~2 mins 44 secs
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Save frames as PNGs
    frame_idx = 0
    concat_list = os.path.join(OUTPUT_DIR, "concat.txt")
    with open(concat_list, "w", encoding="utf-8") as f_concat:
        for s_idx, (img, duration_sec) in enumerate(scenes):
            frame_path = os.path.join(OUTPUT_DIR, f"scene_{s_idx:02d}.png")
            img.save(frame_path, format="PNG")
            print(f"Saved Scene {s_idx + 1} ({duration_sec}s)")
            f_concat.write(f"file '{frame_path}'\n")
            f_concat.write(f"duration {duration_sec}\n")
        # repeat last file per ffmpeg concat demuxer spec
        f_concat.write(f"file '{frame_path}'\n")

    print("\nEncoding video with ffmpeg...")
    cmd = [
        FFMPEG_EXE,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list,
        "-pix_fmt", "yuv420p",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        VIDEO_PATH
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"SUCCESS! Video created at: {VIDEO_PATH}")
        print(f"File size: {os.path.getsize(VIDEO_PATH) / (1024*1024):.2f} MB")
    else:
        print("FFmpeg error:", res.stderr)

if __name__ == "__main__":
    build_video()
