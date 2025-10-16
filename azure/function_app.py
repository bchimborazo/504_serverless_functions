# Code used for Azure's inline editor

import json
import azure.functions as func
import logging

app = func.FunctionApp()

@app.function_name(name="hba1c_classifier")
@app.route(route="hba1c", auth_level=func.AuthLevel.ANONYMOUS)
def hba1c_classifier(req: func.HttpRequest) -> func.HttpResponse:
    """Azure HTTP Function for HbA1c classification.
    Expects JSON with 'hba1c' value.
    Returns a JSON classification based on diabetes screening criteria.
    """
    logging.info('Python HTTP trigger function processed a request.')
    
    # Try to get from JSON body first, then query parameters
    try:
        req_body = req.get_json()
        hba1c = req_body.get('hba1c')
    except ValueError:
        hba1c = req.params.get('hba1c')
    
    # Presence check
    if hba1c is None:
        return func.HttpResponse(
            json.dumps({"error": "'hba1c' is required."}),
            status_code=400,
            mimetype="application/json"
        )
    
    # Type/convert check
    try:
        hba1c_val = float(hba1c)
    except (TypeError, ValueError):
        return func.HttpResponse(
            json.dumps({"error": "'hba1c' must be a number."}),
            status_code=400,
            mimetype="application/json"
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
    
    return func.HttpResponse(
        json.dumps(payload),
        status_code=200,
        mimetype="application/json"
    )