from app.session_manager import get_session
from app.requirement_extractor import extract_requirements
from app.translator import translate_text
from app.property_service import search_properties


def handle_message(session_id, message):

    session = get_session(session_id)
    message = message.lower().strip()

    # -------------------------
    # LANGUAGE SELECTION
    # -------------------------
    if session["language"] is None:

        supported_languages = [
            "english",
            "tamil",
            "hindi",
            "malayalam",
            "telugu",
            "kannada"
        ]

        if message in supported_languages:
            session["language"] = message
            response = "Great! Tell me about the house you are looking for."
            return translate_text(response, session["language"])

        response = """
Hello 👋
I am your AI property assistant.

Please select your preferred language:

1. English
2. Tamil
3. Hindi
4. Malayalam
5. Telugu
6. Kannada
"""
        return response

    # -------------------------
    # REQUIREMENT EXTRACTION
    # -------------------------
    new_requirements = extract_requirements(message)

    if new_requirements:
        session["requirements"].update(new_requirements)

    requirements = session["requirements"]

    # -------------------------
    # FEATURE SKIP OPTION
    # -------------------------
    if message in ["no", "none", "no features", "nothing"]:
        requirements["features"] = []
        session["asked_features"] = False

    # -------------------------
    # CLARIFICATION QUESTIONS
    # -------------------------

    if not requirements.get("city"):
        return translate_text(
            "Which city are you looking for the house in?",
            session["language"]
        )

    if not requirements.get("bhk"):
        return translate_text(
            "How many bedrooms do you need? (For example: 2BHK or 3BHK)",
            session["language"]
        )

    if not requirements.get("price_max"):
        return translate_text(
            "What is your budget for the house?",
            session["language"]
        )

    # Ask feature preferences only once
    if "features" not in requirements and not session["asked_features"]:

        session["asked_features"] = True

        return translate_text(
            "Do you have any specific features in mind? For example: balcony, garden, parking, big hall, etc. (You can also say 'no')",
            session["language"]
        )

    # -------------------------
    # SEARCH PROPERTIES
    # -------------------------
    properties = search_properties(requirements)

    # -------------------------
    # BUILD RESPONSE
    # -------------------------
    city = requirements.get("city", "")
    bhk = requirements.get("bhk", "")
    price = requirements.get("price_max", "")
    features = requirements.get("features", [])

    response = "Got it! "

    if bhk:
        response += f"You're looking for a {bhk}BHK "

    response += "house "

    if city:
        response += f"in {city} "

    if price:
        response += f"under ₹{price:,} "

    if features:
        response += "with "
        response += ", ".join(features)

    response += ". Let me find some options for you."

    # -------------------------
    # SHOW RESULTS
    # -------------------------
    if properties:

        response += "\n\nHere are some homes I found:\n"

        for p in properties:
            response += f"\n{p['title']} - ₹{p['price']:,} in {p['city']}"

    return translate_text(response, session["language"])