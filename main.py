from utils import settings


def main():
    pass


if __name__ == "__main__":
    try:
        config = settings.load_config("config.json")
        main()
    except Exception as e:
        print("Error!", e)
