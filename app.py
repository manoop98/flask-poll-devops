from flask import Flask, render_template, request, redirect, url_for, session
import os
import json

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")

# Environment label (set via App Service config)
ENV_LABEL = os.environ.get("ENV_LABEL", "DEV")
ENV_COLOR = os.environ.get("ENV_COLOR", "#2196F3")  # Blue for dev, orange for staging

# In-memory vote store (resets on restart — intentional for lab simplicity)
votes = {
    "q1": {"yes": 0, "no": 0},
    "q2": {"yes": 0, "no": 0},
    "q3": {"yes": 0, "no": 0},
}

QUESTIONS = {
    "q1": "Do you enjoy working from home?",
    "q2": "Is the current meeting schedule effective?",
    "q3": "Would you recommend this company to a friend?",
}


@app.route("/")
def index():
    voted = session.get("voted", False)
    return render_template(
        "index.html",
        questions=QUESTIONS,
        voted=voted,
        env_label=ENV_LABEL,
        env_color=ENV_COLOR,
    )


@app.route("/vote", methods=["POST"])
def vote():
    if session.get("voted"):
        return redirect(url_for("results"))

    for qid in QUESTIONS:
        answer = request.form.get(qid)
        if answer in ("yes", "no"):
            votes[qid][answer] += 1

    session["voted"] = True
    return redirect(url_for("results"))


@app.route("/results")
def results():
    results_data = {}
    for qid, question in QUESTIONS.items():
        total = votes[qid]["yes"] + votes[qid]["no"]
        yes_pct = round((votes[qid]["yes"] / total * 100) if total > 0 else 0)
        no_pct = 100 - yes_pct if total > 0 else 0
        results_data[qid] = {
            "question": question,
            "yes": votes[qid]["yes"],
            "no": votes[qid]["no"],
            "total": total,
            "yes_pct": yes_pct,
            "no_pct": no_pct,
        }
    return render_template(
        "results.html",
        results=results_data,
        env_label=ENV_LABEL,
        env_color=ENV_COLOR,
    )


@app.route("/health")
def health():
    return json.dumps({"status": "ok", "env": ENV_LABEL}), 200, {
        "Content-Type": "application/json"
    }


@app.route("/reset", methods=["POST"])
def reset():
    # Reset all votes IN-PLACE (required for tests to pass)
    for qid in votes:
        votes[qid]["yes"] = 0
        votes[qid]["no"] = 0

    # Clear session completely
    session.clear()

    return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=(ENV_LABEL == "DEV"))
