
from app.agents.safety_response_agent import generate_safety_response


def test_english_response():
    response = generate_safety_response(
        "Burning smell",
        "en"
    )
    assert "safety" in response.lower()


def test_french_response():
    response = generate_safety_response(
        "Odeur de brûlé",
        "fr"
    )
    assert "sécurité" in response.lower()


def test_arabic_response():
    response = generate_safety_response(
        "رائحة احتراق",
        "ar"
    )
    assert "سلامتك" in response
