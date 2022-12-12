def pre_process_text(text: str) -> str:
    """
      Do all text pre processing here, censor bad words, or maybe even translate the text
    """

    # Following code is just an example of what you can us it for
    text = text[::-1]
    text = text.replace("and", "or").capitalize()
    return text
    #return "This is a text overwrite test"
