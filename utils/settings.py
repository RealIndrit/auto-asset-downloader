import json

config = dict


def load_config(config_file):
    global config
    config = None
    with open(config_file, "r") as f:
        config = json.load(f)
    return config


if __name__ == "main":
    load_config("config.json")
