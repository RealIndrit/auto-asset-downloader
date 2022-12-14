import re


def pre_process_text(text: str) -> str:
    """
      Do all text pre processing here, censor bad words, or maybe even translate the text
    """

    # Following code is just an example of what you can us it for
    wordlist = [("fuck", "frick"), ("sex", "the deed"), ("penis", "pp"),
                ("dick", "pp"), ("pussy", "cat"), ("vagina", "cat"),
                ("porn", "dirty videos")]
    for word in wordlist:
        text = text.lower().replace(word[0], word[1])
    return text.capitalize()