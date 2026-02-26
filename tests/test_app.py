import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from app import app, votes, QUESTIONS


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret"
    # Reset votes before each test
    for qid in votes:
        votes[qid]["yes"] = 0
        votes[qid]["no"] = 0
    with app.test_client() as client:
        yield client


def test_home_page_loads(client):
    """Home page should return 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_home_page_contains_questions(client):
    """Home page should show all poll questions."""
    response = client.get("/")
    for question in QUESTIONS.values():
        assert question.encode() in response.data


def test_health_endpoint(client):
    """Health check should return status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert b"ok" in response.data


def test_vote_submission(client):
    """Submitting all yes votes should increment counts."""
    response = client.post("/vote", data={"q1": "yes", "q2": "yes", "q3": "yes"})
    assert response.status_code == 302  # redirect to results
    assert votes["q1"]["yes"] == 1
    assert votes["q2"]["yes"] == 1
    assert votes["q3"]["yes"] == 1


def test_vote_no_answers(client):
    """Submitting no votes should increment no counts."""
    client.post("/vote", data={"q1": "no", "q2": "no", "q3": "no"})
    assert votes["q1"]["no"] == 1


def test_results_page_loads(client):
    """Results page should return 200."""
    response = client.get("/results")
    assert response.status_code == 200


def test_double_vote_blocked(client):
    """Second vote in same session should be blocked."""
    client.post("/vote", data={"q1": "yes", "q2": "yes", "q3": "yes"})
    client.post("/vote", data={"q1": "no", "q2": "no", "q3": "no"})
    # yes count should still be 1, not 0 (second vote blocked)
    assert votes["q1"]["yes"] == 1
    assert votes["q1"]["no"] == 0


def test_reset_clears_votes(client):
    """Reset should clear all vote counts."""
    client.post("/vote", data={"q1": "yes", "q2": "no", "q3": "yes"})
    client.post("/reset")
    assert votes["q1"]["yes"] == 0
    assert votes["q1"]["no"] == 0
