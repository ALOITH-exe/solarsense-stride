import os
import sqlite3
import functools
import requests
from flask import Flask, request, send_from_directory

app = Flask(__name__)

DEVICE_KEY = os.environ.get("DEVICE_KEY", "")
if not DEVICE_KEY:
    raise RuntimeError("DEVICE_KEY environment variable must be set")

DB = "solarsense.db"


def db():
    return sqlite3.connect(DB)

def audit_log(event, **kwargs):
    app.logger.info("AUDIT %s %s", event, kwargs)

def require_auth(role="user"):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if role == "device":
                if request.headers.get("X-Key") != DEVICE_KEY:
                    return "Denied", 403
            else:
                if not request.headers.get("Authorization"):
                    return "Unauthorized", 401
            return fn(*args, **kwargs)
        return wrapper
    return decorator


@app.route("/api/reading", methods=["POST"])
@require_auth("device")
def reading():
    d = request.get_json()
    db().execute(
        "INSERT INTO readings (meter, kwh) VALUES (?, ?)",
        (d["meter"], d["kwh"]),
    )
    audit_log("reading.inserted", meter=d["meter"])
    return "Stored"


@app.route("/dashboard")
@require_auth("user")
def dashboard():
    home = request.args.get("home_id")
    rows = db().execute(
        "SELECT kwh FROM readings WHERE home=?",
        (home,),
    ).fetchall()
    return str(rows)


@app.route("/firmware")
@require_auth("user")
def firmware():
    r = requests.get(
        "https://updates.example.com/fw.bin",
        verify=True,
        timeout=5,
    )
    return r.content


@app.route("/tariff", methods=["POST"])
@require_auth("user")
def tariff():
    db().execute(
        "UPDATE tariffs SET rate=? WHERE id=?",
        (request.form["rate"], request.form["id"]),
    )
    audit_log("tariff.updated", id=request.form["id"], rate=request.form["rate"])
    return "Updated"


@app.route("/export")
@require_auth("user")
def export():
    filename = request.args.get("file", "")
    return send_from_directory("exports", filename)


@app.route("/health")
def health():
    return "ok"
