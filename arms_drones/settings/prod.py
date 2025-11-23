from .base import *


DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "localhost:85",
    "127.0.0.1",
    config("SERVER", default="127.0.0.1"),
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": int(os.environ["POSTGRES_DB_PORT"]),
    }
}
