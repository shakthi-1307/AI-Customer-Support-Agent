ACKNOWLEDGEMENTS = {
    "ok",
    "okay",
    "thanks",
    "thank you",
    "got it",
    "understood",
    "noted",
    "わかりました",
    "はい。ありがとうございます",
    "merci",
}


def is_acknowledgement(message):
    text = message.strip().lower()

    return text in ACKNOWLEDGEMENTS