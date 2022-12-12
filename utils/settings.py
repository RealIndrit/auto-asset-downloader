import json

config = dict


def load_config(config_file):
    global config
    config = None
    with open(config_file, "r") as f:
        config = json.load(f)
    return config


def save_config(config_file):
    with open(config_file, "w+") as f:
        json.dump(config, f, indent=3)