"""Evaluation script – scores the prototype output against ground_truth.json."""
import json, os

def evaluate():
    gt = json.load(open("ground_truth.json"))
    results = json.load(open("out/results.json"))
    
    gt_map = {g["id"]: g for g in gt}
    res_map = {r["id"]: r for r in results}
    
    # Field accuracy
    FIELDS = ["term_months","auto_renew","notice_days","payment_days","liability",
              "governing_law","dpdp","termination_convenience","indemnity"]
    
    total_fields = 0
    correct_fields = 0
    field_details = []
    
    for cid in sorted(gt_map.keys()):
        g = gt_map[cid]
        r = res_map.get(cid)
        if not r:
            print(f"WARNING: {cid} not found in results")
            continue
        for field in FIELDS:
            total_fields += 1
            expected = g.get(field)
            actual = r["fields"].get(field)
            match = expected == actual
            if match:
                correct_fields += 1
            else:
                field_details.append({"contract": cid, "field": field, "expected": expected, "actual": actual})
    
    field_accuracy = correct_fields / total_fields * 100 if total_fields > 0 else 0
    
    # Obligation recall
    total_obligations = 0
    found_obligations = 0
    missed_obligations = []
    
    for cid in sorted(gt_map.keys()):
        g = gt_map[cid]
        r = res_map.get(cid)
        if not r:
            continue
        for gt_ob in g.get("obligations", []):
            total_obligations += 1
            found = False
            for res_ob in r.get("obligations", []):
                if res_ob.get("due") == gt_ob.get("due") or (res_ob.get("action") and gt_ob.get("action") and gt_ob["action"][:20] in res_ob["action"]):
                    found = True
                    break
            if found:
                found_obligations += 1
            else:
                missed_obligations.append({"contract": cid, "obligation": gt_ob})
    
    obligation_recall = found_obligations / total_obligations * 100 if total_obligations > 0 else 0
    
    # Flag accuracy
    alerts = json.load(open("out/alerts.json"))
    
    # Routing accuracy
    routing_correct = 0
    routing_total = 0
    for cid in sorted(gt_map.keys()):
        g = gt_map[cid]
        r = res_map.get(cid)
        if not r:
            continue
        routing_total += 1
        # Expected route based on ground truth
        has_high = False
        has_medium = False
        if g.get("liability") == "unlimited":
            has_high = True
        if not g.get("dpdp"):
            has_high = True
        if g.get("indemnity") == "one-way":
            has_medium = True
        if g.get("governing_law") not in ["India"]:
            has_medium = True
        if g.get("payment_days") and g.get("payment_days") > 45:
            has_medium = True
        if g.get("auto_renew") and g.get("notice_days", 0) > 60:
            has_medium = True
        
        if has_high:
            expected_route = "LEGAL REVIEW REQUIRED"
        elif has_medium:
            expected_route = "MANAGER REVIEW"
        else:
            expected_route = "AUTO-APPROVE (log only)"
        
        if r["route"] == expected_route:
            routing_correct += 1
    
    routing_accuracy = routing_correct / routing_total * 100 if routing_total > 0 else 0
    
    # Count flags
    total_flags = sum(len(r.get("flags", [])) for r in results)
    high_flags = sum(1 for r in results for f in r.get("flags", []) if f["severity"] == "HIGH")
    medium_flags = sum(1 for r in results for f in r.get("flags", []) if f["severity"] == "MEDIUM")
    low_flags = sum(1 for r in results for f in r.get("flags", []) if f["severity"] == "LOW")
    
    # Obligation status summary
    status_counts = {}
    for a in alerts:
        st = a.get("status", "UNKNOWN")
        status_counts[st] = status_counts.get(st, 0) + 1
    
    eval_results = {
        "field_accuracy": {"correct": correct_fields, "total": total_fields, "percentage": round(field_accuracy, 1)},
        "field_mismatches": field_details,
        "obligation_recall": {"found": found_obligations, "total": total_obligations, "percentage": round(obligation_recall, 1)},
        "missed_obligations": missed_obligations,
        "routing_accuracy": {"correct": routing_correct, "total": routing_total, "percentage": round(routing_accuracy, 1)},
        "flag_summary": {"total": total_flags, "high": high_flags, "medium": medium_flags, "low": low_flags},
        "obligation_status": status_counts,
        "contracts_by_route": {
            "LEGAL REVIEW REQUIRED": sum(1 for r in results if r["route"] == "LEGAL REVIEW REQUIRED"),
            "MANAGER REVIEW": sum(1 for r in results if r["route"] == "MANAGER REVIEW"),
            "AUTO-APPROVE (log only)": sum(1 for r in results if r["route"] == "AUTO-APPROVE (log only)")
        }
    }
    
    json.dump(eval_results, open("out/eval_results.json", "w"), indent=2)
    
    print("=" * 60)
    print("CONTRACT REVIEW AGENT - EVALUATION RESULTS")
    print("=" * 60)
    print(f"\nField Extraction Accuracy: {correct_fields}/{total_fields} = {field_accuracy:.1f}%")
    if field_details:
        print("  Mismatches:")
        for d in field_details:
            print(f"    {d['contract']}.{d['field']}: expected={d['expected']} actual={d['actual']}")
    print(f"\nObligation Recall: {found_obligations}/{total_obligations} = {obligation_recall:.1f}%")
    if missed_obligations:
        print("  Missed:")
        for m in missed_obligations:
            print(f"    {m['contract']}: {m['obligation']}")
    print(f"\nRouting Accuracy: {routing_correct}/{routing_total} = {routing_accuracy:.1f}%")
    print(f"\nFlag Summary: {total_flags} total ({high_flags} HIGH, {medium_flags} MEDIUM, {low_flags} LOW)")
    print(f"\nObligation Status: {status_counts}")
    print(f"\nContracts by Route: {eval_results['contracts_by_route']}")
    print("=" * 60)
    
    return eval_results

if __name__ == "__main__":
    evaluate()
