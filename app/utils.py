"""
app/utils.py — Utility helpers yang dipakai di seluruh app.
"""
from flask import jsonify


def api_response(status="success", message="", data=None, status_code=200):
    """
    Format response JSON yang konsisten untuk semua API endpoint.

    Args:
        status:      "success" atau "error"
        message:     Pesan deskriptif
        data:        Dict atau list data (opsional)
        status_code: HTTP status code

    Returns:
        Flask Response object dengan format:
        {
            "status": "success" | "error",
            "message": "...",
            "data": {...} | [...] | null
        }
    """
    body = {
        "status": status,
        "message": message,
    }
    if data is not None:
        body["data"] = data
    return jsonify(body), status_code
