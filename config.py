import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


TOKEN = os.getenv("TOKEN")
MIDJOURNERY_ID = 936929561302675456
SESSION_ID = "anything"

HEADERS = {
        "Authorization": os.getenv("AUTH_TOKEN"),
    }
