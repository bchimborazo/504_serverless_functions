# Code used for GCP inline editor

import json
import functions_framework

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function for HbA1c classification.
    Expects JSON with 'hba1c' value.
    Returns a JSON classification based on diabetes screening criteria.
    """
    # Prefer JSON body; fall back to query parameters
    data = request.get_json(silent=True) or {}
    args = request.args or {}
    
    hba1c = data.get("hba1c", args.get("hba1c"))
    
    # Presence check
    if hba1c is None:
        return (
            json.dumps({"error": "'hba1c' is required."}),
            400,
            {"Content-Type": "application/json"},
        )
    
    # Type/convert check
    try:
        hba1c_val = float(hba1c)
    except (TypeError, ValueError):
        return (
            json.dumps({"error": "'hba1c' must be a number."}),
            400,
            {"Content-Type": "application/json"},
        )
    
    # Classification logic: Normal if < 5.7%, Abnormal if >= 5.7%
    status = "normal" if hba1c_val < 5.7 else "abnormal"
    
    if status == "normal":
        category = "Normal (<5.7%)"
    elif hba1c_val < 6.5:
        category = "Prediabetes (5.7-6.4%)"
    else:
        category = "Diabetes Range (≥6.5%)"
    
    payload = {
        "hba1c": hba1c_val,
        "status": status,
        "category": category,
    }
    
    return json.dumps(payload), 200, {"Content-Type": "application/json"}