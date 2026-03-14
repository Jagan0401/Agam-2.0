from deep_translator import GoogleTranslator


def translate_text(text, target_lang):

    language_map = {
        "english": "en",
        "tamil": "ta",
        "hindi": "hi",
        "malayalam": "ml",
        "telugu": "te",
        "kannada": "kn"
    }

    if target_lang == "english":
        return text

    lang_code = language_map.get(target_lang)

    try:
        translated = GoogleTranslator(source='auto', target=lang_code).translate(text)
        return translated
    except Exception:
        return text