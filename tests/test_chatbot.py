"""Tests for the Planet chatbot response logic."""

import pytest
from chatbot import get_response, PLANET_DATA


# ── Greeting ────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("msg", ["hi", "hello", "hey", "Hello!", "Hi there"])
def test_greeting(msg):
    reply = get_response(msg)
    assert "planet" in reply.lower() or "welcome" in reply.lower()


# ── Help ────────────────────────────────────────────────────────────────────

def test_help():
    reply = get_response("help")
    assert "help" in reply.lower() or "ask" in reply.lower()


# ── List planets ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("msg", ["list planets", "list all planets", "name all planets"])
def test_list_planets(msg):
    reply = get_response(msg)
    for planet in PLANET_DATA:
        assert planet.capitalize() in reply


# ── Planet summary ──────────────────────────────────────────────────────────

@pytest.mark.parametrize("planet", list(PLANET_DATA.keys()))
def test_planet_summary(planet):
    reply = get_response(f"tell me about {planet}")
    assert planet.capitalize() in reply
    assert PLANET_DATA[planet]["diameter"] in reply


# ── Moons ───────────────────────────────────────────────────────────────────

def test_moons_jupiter():
    reply = get_response("how many moons does Jupiter have?")
    assert "95" in reply


def test_moons_mercury():
    reply = get_response("How many moons does Mercury have?")
    assert "no moons" in reply.lower() or "0" in reply


# ── Temperature ─────────────────────────────────────────────────────────────

def test_temperature_venus():
    reply = get_response("What is the temperature on Venus?")
    assert "465" in reply


# ── Distance ────────────────────────────────────────────────────────────────

def test_distance_mars():
    reply = get_response("How far is Mars from the Sun?")
    assert "227.9" in reply


# ── Day length ───────────────────────────────────────────────────────────────

def test_day_saturn():
    reply = get_response("How long is a day on Saturn?")
    assert "10.7" in reply


# ── Year length ──────────────────────────────────────────────────────────────

def test_year_neptune():
    reply = get_response("How long is a year on Neptune?")
    assert "165" in reply


# ── Fun fact ────────────────────────────────────────────────────────────────

def test_fun_fact():
    reply = get_response("fun fact about Mars")
    assert PLANET_DATA["mars"]["fun_fact"] in reply


# ── Unknown message ──────────────────────────────────────────────────────────

def test_unknown():
    reply = get_response("what is the meaning of life?")
    assert reply  # just ensure a non-empty response


# ── Empty message ────────────────────────────────────────────────────────────

def test_empty_message():
    reply = get_response("")
    assert reply


# ── Flask app routes ─────────────────────────────────────────────────────────

@pytest.fixture
def client():
    from app import app as flask_app
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


def test_index_route(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Planet" in resp.data


def test_chat_route_valid(client):
    resp = client.post(
        "/chat",
        json={"message": "tell me about Earth"},
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "reply" in data
    assert "Earth" in data["reply"]


def test_chat_route_empty(client):
    resp = client.post("/chat", json={"message": ""})
    assert resp.status_code == 400


def test_chat_route_no_body(client):
    resp = client.post("/chat", data="not json", content_type="text/plain")
    assert resp.status_code == 400
