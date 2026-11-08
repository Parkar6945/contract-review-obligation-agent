"""Contract Review & Obligation Tracking Agent - prototype (offline, rule-based baseline).
Each 'agent' exposes the same interface an LLM-backed agent would, so the extractor can be swapped for an LLM call."""
import re, json, glob, datetime as dt, os

MONTHS=["january","february","march","april","may","june","july","august","september","october","november","december"]
NUM={"fifteen":15,"thirty":30,"forty-five":45,"sixty":60,"ninety":90,"one hundred twenty":120,"twelve":12,"twenty-four":24,"thirty-six":36,"two":2,"three":3,"five":5,"seven":7,"ten":10,"one":1}
PLAYBOOK={"max_payment_days":45,"min_notice_days":30,"max_notice_days":60,"approved_laws":["India"],"require_dpdp":True,
    "liability":"must be capped","indemnity":"must be mutual"}
LOG=[]

def audit(agent,event,**kw):
    LOG.append({"ts":dt.datetime(2026,11,6,10,0).isoformat(),"agent":agent,"event":event,**kw})

def parse_date(s):
    m=re.search(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})",s)
    if m and m.group(2).lower() in MONTHS:
        return dt.date(int(m.group(3)),MONTHS.index(m.group(2).lower())+1,int(m.group(1)))
    m=re.search(r"([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})",s)
    if m and m.group(1).lower() in MONTHS:
        return dt.date(int(m.group(3)),MONTHS.index(m.group(1).lower())+1,int(m.group(2)))
    m=re.search(r"(\d{2})/(\d{2})/(\d{4})",s)
    if m:
        return dt.date(int(m.group(3)),int(m.group(2)),int(m.group(1)))
    return None

def clauses(text):
    return [re.sub(r"^\d+\.\s*","",p).strip() for p in text.split("\n\n")[1:] if p.strip()]

# ---- Agent 1: Clause Extraction ----
def extract(text):
    f={"auto_renew":None,"notice_days":0,"payment_days":None,"liability":None,"governing_law":None,"dpdp":False,
        "termination_convenience":False,"indemnity":None,"term_months":None,"effective":None}
    cl=clauses(text); obs=[]
    for c in cl:
        u=c.upper()
        if c.startswith("This ") and "Effective Date" in c:
            d=parse_date(c); f["effective"]=d.isoformat() if d else None
        if u.startswith("TERM."):
            m=re.search(r"\((\d+)\)\s*months",c)
            if m: f["term_months"]=int(m.group(1))
        elif u.startswith("RENEWAL."):
            f["auto_renew"]="automatically renew" in c and "not automatically renew" not in c
            m=re.search(r"not less than .*?\((\d+)\) days",c)
            if m: f["notice_days"]=int(m.group(1))
        elif u.startswith("PAYMENT."):
            m=re.search(r"within .*?\((\d+)\) days",c)
            if m: f["payment_days"]=int(m.group(1))
        elif u.startswith("LIMITATION"):
            f["liability"]="unlimited" if "unlimited" in c else ("fixed" if "INR" in c else "fees")
        elif u.startswith("INDEMNITY"):
            f["indemnity"]="mutual" if "Each party shall indemnify" in c else "one-way"
        elif u.startswith("TERMINATION"):
            f["termination_convenience"]="for convenience" in c
        elif u.startswith("DATA PROTECTION"):
            f["dpdp"]="Digital Personal Data Protection Act" in c
        elif u.startswith("GOVERNING"):
            f["governing_law"]=next((k for k in ["India","England","Singapore"] if k in c),None)
        # obligations: 'shall' + date
        if re.search(r"\b(shall (deliver|submit|provide))\b",c) and not u.startswith(("PAYMENT","CONFID","DATA")):
            d=parse_date(c.split(".",1)[1] if "." in c[:25] else c)
            who="Supplier" if c.split(". ",1)[-1].startswith("Supplier") else "Customer"
            act=re.search(r"shall (.*?)(?: on or before| no later than| by )",c)
            obs.append({"party":who,"action":act.group(1) if act else c[:50],"due":d.isoformat() if d else None})
    if f["auto_renew"] and f["effective"] and f["term_months"] and f["notice_days"]:
        e=dt.date.fromisoformat(f["effective"]); y=e.year+f["term_months"]//12
        end=dt.date(y,e.month,e.day)-dt.timedelta(days=1)
        obs.append({"party":"Either","action":"send notice of non-renewal (deadline)","due":(end-dt.timedelta(days=f["notice_days"])).isoformat()})
    return f,obs

# ---- Agent 2: Risk Review against playbook ----
def review(f):
    flags=[]
    def add(sev,msg): flags.append({"severity":sev,"issue":msg})
    if f["liability"]=="unlimited": add("HIGH","Unlimited liability")
    if f["indemnity"]=="one-way": add("MEDIUM","One-way indemnity against Customer")
    if f["governing_law"] and f["governing_law"] not in PLAYBOOK["approved_laws"]: add("MEDIUM",f"Non-approved governing law: {f['governing_law']}")
    if f["payment_days"] is None: add("LOW","Payment term not extracted - manual check")
    elif f["payment_days"]>PLAYBOOK["max_payment_days"]: add("MEDIUM",f"Payment term {f['payment_days']} days exceeds {PLAYBOOK['max_payment_days']}")
    if f["auto_renew"] and f["notice_days"]>PLAYBOOK["max_notice_days"]: add("MEDIUM",f"Auto-renewal notice window {f['notice_days']} days is long")
    if not f["dpdp"]: add("HIGH","No DPDP Act 2023 data protection clause")
    if f["term_months"] is None: add("LOW","Term not extracted - manual check")
    return flags

# ---- Agent 3: Obligation tracker ----
def track(cid,obs,asof):
    out=[]
    for o in obs:
        if not o["due"]:
            out.append({**o,"contract":cid,"status":"NEEDS REVIEW (no date parsed)","days":None}); continue
        d=(dt.date.fromisoformat(o["due"])-asof).days
        st="PAST DUE" if d<0 else "DUE <=30d" if d<=30 else "DUE <=90d" if d<=90 else "UPCOMING"
        out.append({**o,"contract":cid,"status":st,"days":d})
    return out

# ---- Supervisor with human-in-the-loop routing ----
def run(asof=dt.date(2026,11,6)):
    results=[];alerts=[]
    for p in sorted(glob.glob("contracts/*.txt")):
        cid=os.path.basename(p)[:-4]; text=open(p).read()
        f,obs=extract(text); audit("extractor","extracted",contract=cid)
        flags=review(f); audit("reviewer","flags",contract=cid,n=len(flags))
        route="LEGAL REVIEW REQUIRED" if any(x["severity"]=="HIGH" for x in flags) else ("MANAGER REVIEW" if flags else "AUTO-APPROVE (log only)")
        audit("supervisor","routed",contract=cid,route=route)
        results.append({"id":cid,"fields":f,"obligations":obs,"flags":flags,"route":route})
        alerts+=track(cid,obs,asof)
    return results,alerts

if __name__=="__main__":
    r,a=run()
    os.makedirs("out", exist_ok=True)
    json.dump(r,open("out/results.json","w"),indent=1,default=str)
    json.dump(a,open("out/alerts.json","w"),indent=1)
    json.dump(LOG,open("out/audit_log.json","w"),indent=1)
    for x in r: print(x["id"],x["route"],[y["issue"] for y in x["flags"]])
