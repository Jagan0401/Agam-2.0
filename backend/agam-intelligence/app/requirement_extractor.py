import re


def extract_requirements(message):

    message = message.lower()

    requirements = {}
    features = []

    # BHK detection
    bhk_match = re.search(r'(\d+)\s*bhk', message)
    if bhk_match:
        requirements["bhk"] = int(bhk_match.group(1))

    # City detection
    city_match = re.search(r'in\s+([a-zA-Z\s]+)', message)
    if city_match:
        city = city_match.group(1).strip()
        city = re.split(r'\s+(with|that|which|and)', city)[0]
        requirements["city"] = city.title()

    # Price detection
    price_match = re.search(r'under\s+(\d+)\s*(lakh|lakhs|crore|crores)?', message)

    if price_match:

        amount = int(price_match.group(1))
        unit = price_match.group(2)

        if unit in ["lakh", "lakhs"]:
            amount *= 100000

        if unit in ["crore", "crores"]:
            amount *= 10000000

        requirements["price_max"] = amount

    # Feature extraction
    feature_patterns = re.findall(
        r'\b(big|small|large|spacious|modern|luxury|attached|private|beautiful|open|wide|covered|modular)\s+([a-z]+)',
        message
    )

    for adj, noun in feature_patterns:
        features.append(f"{adj} {noun}")

    if features:
        requirements["features"] = features

    return requirements