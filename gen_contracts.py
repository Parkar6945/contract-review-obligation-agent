"""Synthetic contract and ground-truth generator for the Contract Review & Obligation Tracking Agent project."""
import json, os, random, datetime as dt

random.seed(42)

TYPES = [
    ("SaaS Subscription Agreement", "SaaS"),
    ("Master Services Agreement", "MSA"),
    ("Supply Agreement", "Supply"),
    ("Services Agreement", "Services"),
]

CUSTOMERS = [
    "Pinnacle Infotech Pvt Ltd", "Deccan Auto Components Ltd",
    "Saffron Retail Holdings", "Vistara Logistics Corp",
    "Meridian Pharma Ltd", "Zenith Financial Services",
    "Horizon Agritech", "Quantum Digital Solutions Pvt Ltd",
    "Coral Hospitality Group", "Summit Engineering Works"
]

SUPPLIERS = [
    "CloudNine Solutions Inc", "Helix Components Co",
    "DataBridge Analytics Pvt Ltd", "Prism Software Ltd",
    "NovaTech Systems", "Apex Cloud Services",
    "CyberShield Security Inc", "Atlas Supply Chain Co",
    "TerraFirm IT Solutions", "Orbit Technologies Ltd"
]

LAWS = ["India", "England", "Singapore"]

def rand_date(year=2026, month_range=(1, 6)):
    m = random.randint(*month_range)
    d = random.randint(1, 28)
    return dt.date(year, m, d)

def make_contract(idx, ctype, customer, supplier, effective, term_months,
                  auto_renew, notice_days, payment_days, liability,
                  governing_law, dpdp, termination_convenience, indemnity,
                  obligations, unusual=None):
    cid = f"C{idx:02d}"
    end = dt.date(effective.year + term_months // 12, effective.month, effective.day) - dt.timedelta(days=1)
    
    lines = []
    lines.append(f"{ctype[0].upper()}")
    lines.append("")
    lines.append(f"This {ctype[0]} (\"Agreement\") is entered into as of the Effective Date {effective.strftime('%d %B %Y')} between {customer} (\"Customer\") and {supplier} (\"Supplier\").")
    lines.append("")
    
    # Term
    if unusual == "term_words":
        lines.append(f"1. TERM. This Agreement shall be effective for a period of two years from the Effective Date.")
    else:
        lines.append(f"1. TERM. This Agreement shall be effective for a period of ({term_months}) months from the Effective Date.")
    lines.append("")
    
    # Renewal
    if auto_renew:
        lines.append(f"2. RENEWAL. This Agreement shall automatically renew for successive periods of the same length unless either party provides written notice of non-renewal not less than ({notice_days}) days before the end of the then-current term.")
    else:
        lines.append(f"2. RENEWAL. This Agreement shall not automatically renew. Either party may propose renewal by written notice at least thirty (30) days before the end of the term.")
    lines.append("")
    
    # Payment
    if unusual == "payment_words":
        lines.append(f"3. PAYMENT. Customer shall pay all undisputed invoices within one and a half months of receipt of the invoice.")
    else:
        lines.append(f"3. PAYMENT. Customer shall pay all undisputed invoices within ({payment_days}) days of receipt of the invoice.")
    lines.append("")
    
    # Liability
    if liability == "unlimited":
        lines.append(f"4. LIMITATION OF LIABILITY. Supplier's aggregate liability under this Agreement shall be unlimited for all claims arising under or in connection with this Agreement.")
    elif liability == "fixed":
        lines.append(f"4. LIMITATION OF LIABILITY. Supplier's aggregate liability under this Agreement shall not exceed INR 50,00,000 (Fifty Lakh) for all claims arising under or in connection with this Agreement.")
    else:
        lines.append(f"4. LIMITATION OF LIABILITY. Supplier's aggregate liability under this Agreement shall not exceed the total fees paid by Customer in the twelve (12) months preceding the claim.")
    lines.append("")
    
    # Indemnity
    if indemnity == "mutual":
        lines.append(f"5. INDEMNITY. Each party shall indemnify the other against all losses, damages and costs arising from a breach of this Agreement or negligence of the indemnifying party.")
    else:
        lines.append(f"5. INDEMNITY. Supplier shall indemnify Customer against all losses, damages and costs arising from a breach of this Agreement or negligence of Supplier.")
    lines.append("")
    
    # Termination
    if termination_convenience:
        lines.append(f"6. TERMINATION. Either party may terminate this Agreement for convenience upon thirty (30) days' prior written notice to the other party.")
    else:
        lines.append(f"6. TERMINATION. Either party may terminate this Agreement only for material breach that remains uncured for thirty (30) days after written notice.")
    lines.append("")
    
    # Confidentiality
    lines.append(f"7. CONFIDENTIALITY. Each party shall keep confidential all information received from the other party that is marked as confidential or that a reasonable person would understand to be confidential.")
    lines.append("")
    
    # Data Protection
    if dpdp:
        lines.append(f"8. DATA PROTECTION. Each party shall comply with the Digital Personal Data Protection Act, 2023 and all applicable data protection laws. Supplier, as data processor, shall process personal data only as instructed by Customer and shall implement appropriate technical and organisational measures.")
    else:
        lines.append(f"8. GENERAL PROVISIONS. Each party shall comply with all applicable laws in the performance of its obligations under this Agreement.")
    lines.append("")
    
    # Governing Law
    lines.append(f"9. GOVERNING LAW. This Agreement shall be governed by and construed in accordance with the laws of {governing_law}.")
    lines.append("")
    
    # Obligations
    ob_num = 10
    for i, ob in enumerate(obligations):
        if unusual == "date_words" and i == len(obligations) - 1:
            lines.append(f"{ob_num + i}. DELIVERABLES. {ob['party']} shall {ob['action']} on or before the fifteenth day of December 2026.")
        else:
            due_str = dt.date.fromisoformat(ob['due']).strftime('%d %B %Y') if i % 2 == 0 else dt.date.fromisoformat(ob['due']).strftime('%B %d, %Y')
            lines.append(f"{ob_num + i}. DELIVERABLES. {ob['party']} shall {ob['action']} on or before {due_str}.")
        lines.append("")
    
    # Signatures
    lines.append("IN WITNESS WHEREOF, the parties have executed this Agreement as of the Effective Date.")
    lines.append("")
    lines.append(f"For {customer}:  ____________________")
    lines.append(f"For {supplier}:  ____________________")
    
    return cid, "\n".join(lines), end

def generate():
    os.makedirs("contracts", exist_ok=True)
    ground_truth = []
    
    configs = [
        # C01: SaaS, 24m, no auto-renew, 30 pay, fixed, Singapore, dpdp, no term-conv, mutual
        dict(idx=1, ctype=TYPES[0], customer=CUSTOMERS[0], supplier=SUPPLIERS[0],
             effective=dt.date(2026, 2, 15), term_months=24, auto_renew=False, notice_days=0,
             payment_days=30, liability="fixed", governing_law="Singapore", dpdp=True,
             termination_convenience=False, indemnity="mutual",
             obligations=[
                 {"party": "Supplier", "action": "deliver initial platform configuration", "due": "2026-04-15"},
                 {"party": "Customer", "action": "provide access credentials and data migration files", "due": "2026-03-15"},
             ]),
        # C02: MSA, 24m, auto-renew 60d, 60 pay, fixed, England, dpdp, term-conv, one-way
        dict(idx=2, ctype=TYPES[1], customer=CUSTOMERS[1], supplier=SUPPLIERS[1],
             effective=dt.date(2026, 1, 10), term_months=24, auto_renew=True, notice_days=60,
             payment_days=60, liability="fixed", governing_law="England", dpdp=True,
             termination_convenience=True, indemnity="one-way",
             obligations=[
                 {"party": "Supplier", "action": "deliver project plan and timeline", "due": "2026-02-10"},
                 {"party": "Supplier", "action": "submit quarterly performance report", "due": "2026-04-10"},
                 {"party": "Customer", "action": "provide site access for installation", "due": "2026-03-01"},
             ]),
        # C03: Supply, 36m, auto-renew 60d, 45 pay, unlimited, Singapore, dpdp, term-conv, mutual
        dict(idx=3, ctype=TYPES[2], customer=CUSTOMERS[2], supplier=SUPPLIERS[2],
             effective=dt.date(2026, 3, 22), term_months=36, auto_renew=True, notice_days=60,
             payment_days=45, liability="unlimited", governing_law="Singapore", dpdp=True,
             termination_convenience=True, indemnity="mutual",
             obligations=[
                 {"party": "Supplier", "action": "deliver Phase 1 deliverables", "due": "2026-07-06"},
                 {"party": "Supplier", "action": "submit Phase 2 completion report", "due": "2026-10-05"},
                 {"party": "Customer", "action": "provide final acceptance certificate", "due": "2027-01-15"},
             ]),
        # C04: Services, 12m, no auto-renew, 15 pay, fees, India, no dpdp, no term-conv, one-way
        dict(idx=4, ctype=TYPES[3], customer=CUSTOMERS[3], supplier=SUPPLIERS[3],
             effective=dt.date(2026, 4, 1), term_months=12, auto_renew=False, notice_days=0,
             payment_days=15, liability="fees", governing_law="India", dpdp=True,
             termination_convenience=False, indemnity="one-way",
             obligations=[
                 {"party": "Supplier", "action": "deliver training materials", "due": "2026-05-15"},
                 {"party": "Supplier", "action": "submit final deliverables report", "due": "2026-09-30"},
             ],
             unusual="payment_words"),
        # C05: SaaS, 36m, auto-renew 90d, 30 pay, fees, India, dpdp, term-conv, mutual
        dict(idx=5, ctype=TYPES[0], customer=CUSTOMERS[4], supplier=SUPPLIERS[4],
             effective=dt.date(2026, 1, 5), term_months=36, auto_renew=True, notice_days=90,
             payment_days=30, liability="fees", governing_law="India", dpdp=False,
             termination_convenience=True, indemnity="mutual",
             obligations=[
                 {"party": "Supplier", "action": "deliver system integration documentation", "due": "2026-03-05"},
                 {"party": "Customer", "action": "provide user acceptance test results", "due": "2026-04-05"},
                 {"party": "Supplier", "action": "submit go-live readiness report", "due": "2026-06-05"},
             ]),
        # C06: MSA, 24m, auto-renew 30d, 90 pay, unlimited, England, dpdp, no term-conv, mutual — unusual payment_words
        dict(idx=6, ctype=TYPES[1], customer=CUSTOMERS[5], supplier=SUPPLIERS[5],
             effective=dt.date(2026, 2, 1), term_months=24, auto_renew=True, notice_days=30,
             payment_days=90, liability="unlimited", governing_law="England", dpdp=True,
             termination_convenience=False, indemnity="mutual",
             obligations=[
                 {"party": "Supplier", "action": "deliver initial assessment report", "due": "2026-03-15"},
                 {"party": "Customer", "action": "provide historical data export", "due": "2026-03-01"},
                 {"party": "Supplier", "action": "submit compliance audit findings", "due": "2026-08-01"},
             ]),
        # C07: Supply, 24m, auto-renew 120d, 60 pay, fixed, Singapore, no dpdp, term-conv, one-way
        dict(idx=7, ctype=TYPES[2], customer=CUSTOMERS[6], supplier=SUPPLIERS[6],
             effective=dt.date(2026, 3, 1), term_months=24, auto_renew=True, notice_days=120,
             payment_days=60, liability="fixed", governing_law="Singapore", dpdp=True,
             termination_convenience=True, indemnity="one-way",
             obligations=[
                 {"party": "Supplier", "action": "deliver security audit report", "due": "2026-05-01"},
                 {"party": "Customer", "action": "provide network architecture documentation", "due": "2026-04-15"},
                 {"party": "Supplier", "action": "submit penetration test results", "due": "2026-07-01"},
             ],
             unusual="term_words"),
        # C08: Services, 12m, no auto-renew, 45 pay, fees, India, dpdp, no term-conv, mutual — unusual term_words
        dict(idx=8, ctype=TYPES[3], customer=CUSTOMERS[7], supplier=SUPPLIERS[7],
             effective=dt.date(2026, 5, 1), term_months=24, auto_renew=False, notice_days=0,
             payment_days=45, liability="fees", governing_law="India", dpdp=True,
             termination_convenience=False, indemnity="mutual",
             obligations=[
                 {"party": "Supplier", "action": "deliver prototype design documents", "due": "2026-07-01"},
                 {"party": "Customer", "action": "provide feedback on prototype", "due": "2026-08-15"},
             ]),
        # C09: SaaS, 36m, auto-renew 60d, 30 pay, fixed, England, dpdp, term-conv, one-way
        dict(idx=9, ctype=TYPES[0], customer=CUSTOMERS[8], supplier=SUPPLIERS[8],
             effective=dt.date(2026, 1, 20), term_months=36, auto_renew=True, notice_days=60,
             payment_days=30, liability="unlimited", governing_law="England", dpdp=True,
             termination_convenience=True, indemnity="one-way",
             obligations=[
                 {"party": "Supplier", "action": "deliver data migration completion report", "due": "2026-04-20"},
                 {"party": "Customer", "action": "provide legacy system access", "due": "2026-02-20"},
                 {"party": "Supplier", "action": "submit user training completion certificate", "due": "2026-06-20"},
             ]),
        # C10: Supply, 12m, no auto-renew, 30 pay, fees, India, dpdp, no term-conv, mutual — unusual date_words
        dict(idx=10, ctype=TYPES[2], customer=CUSTOMERS[9], supplier=SUPPLIERS[9],
             effective=dt.date(2026, 6, 1), term_months=12, auto_renew=False, notice_days=0,
             payment_days=30, liability="fees", governing_law="India", dpdp=False,
             termination_convenience=False, indemnity="mutual",
             obligations=[
                 {"party": "Supplier", "action": "deliver equipment specifications", "due": "2026-08-01"},
                 {"party": "Supplier", "action": "submit installation completion report", "due": "2026-12-15"},
             ],
             unusual="date_words"),
    ]
    
    for cfg in configs:
        unusual = cfg.pop("unusual", None)
        cid, text, end = make_contract(**cfg, unusual=unusual)
        
        with open(f"contracts/{cid}.txt", "w") as fp:
            fp.write(text)
        
        # Compute renewal notice deadline if auto_renew
        renewal_notice_deadline = None
        if cfg["auto_renew"] and cfg["notice_days"] > 0:
            renewal_notice_deadline = (end - dt.timedelta(days=cfg["notice_days"])).isoformat()
        
        gt = {
            "id": cid,
            "type": cfg["ctype"][0],
            "customer": cfg["customer"],
            "supplier": cfg["supplier"],
            "effective": cfg["effective"].isoformat(),
            "term_months": cfg["term_months"],
            "end": end.isoformat(),
            "auto_renew": cfg["auto_renew"],
            "notice_days": cfg["notice_days"],
            "payment_days": cfg["payment_days"],
            "liability": cfg["liability"],
            "governing_law": cfg["governing_law"],
            "dpdp": cfg["dpdp"],
            "termination_convenience": cfg["termination_convenience"],
            "indemnity": cfg["indemnity"],
            "obligations": cfg["obligations"],
            "unusual": unusual
        }
        if renewal_notice_deadline:
            gt["obligations"].append({
                "party": "Either",
                "action": "send notice of non-renewal (deadline)",
                "due": renewal_notice_deadline
            })
        ground_truth.append(gt)
    
    with open("ground_truth.json", "w") as fp:
        json.dump(ground_truth, fp, indent=2, default=str)
    
    print(f"Generated {len(configs)} contracts in contracts/ and ground_truth.json")

if __name__ == "__main__":
    generate()
