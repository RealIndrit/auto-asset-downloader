from pathlib import Path


def write_to_file(path, text, encoding: str = "utf-8"):
    output_file = Path(path)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(text, encoding)


def append_to_file(path, text, encoding: str = "utf-8"):
    output_file = Path(path)
    if not Path(output_file).exists():
        output_file.parent.mkdir(exist_ok=True, parents=True)
    fp = Path(output_file).open('a', encoding=encoding)
    fp.write(text)