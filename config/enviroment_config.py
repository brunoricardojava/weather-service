from decouple import config


def get_enviroment_config():
    return {
        "API_KEY": config("API_KEY"),
        "OPEN_WEATHER_BASE_URL": config("OPEN_WEATHER_BASE_URL"),
        "MAX_RATE": config("MAX_RATE", cast=int),
        "TIME_PERIOD": config("TIME_PERIOD", cast=int),
    }


ENV_CONFIG = get_enviroment_config()
