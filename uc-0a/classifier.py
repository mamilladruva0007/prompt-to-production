import argparse
import csv
import json

# Define severity triggers (replace/add more if needed)
TRIGGERS = ["critical", "high", "urgent", "important"]

def classify_complaint(row: dict) -> dict:
    """
    Classify a single complaint row.
    Returns a dict with complaint_id, category, priority, reason, flag
    """
    complaint_id = row.get("complaint_id", "")
    message = row.get("message", "")
    result = {
        "complaint_id": complaint_id,
        "category": "general",
        "priority": "normal",
        "reason": "",
        "flag": False
    }

    if not message:
        result["reason"] = "Missing message"
        result["flag"] = True
        return result

    # Simple RICE-inspired severity check
    for trig in TRIGGERS:
        if trig.lower() in message.lower():
            result["priority"] = trig
            result["reason"] = f"Matched trigger: {trig}"
            result["flag"] = True
            break

    return result

def batch_classify(input_path: str, output_path: str):
    """
    Read input CSV, classify each row, write results JSON.
    """
    results = []

    with open(input_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                classified = classify_complaint(row)
                results.append(classified)
            except Exception as e:
                results.append({
                    "complaint_id": row.get("complaint_id", ""),
                    "category": "error",
                    "priority": "error",
                    "reason": str(e),
                    "flag": True
                })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UC-0A Complaint Classifier")
    parser.add_argument("--input",  required=True, help="Path to test_[city].csv")
    parser.add_argument("--output", required=True, help="Path to write results JSON")
    args = parser.parse_args()
    batch_classify(args.input, args.output)
    print(f"Done. Results written to {args.output}")
