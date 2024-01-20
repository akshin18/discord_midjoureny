import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


TOKEN = os.getenv("TOKEN")
MIDJOURNERY_ID = int(os.getenv("MIDJOURNERY_ID"))
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
GUILD_ID = int(os.getenv("GUILD_ID"))
SESSION_ID = os.getenv("SESSION_ID")

HEADERS = {
        "Authorization": os.getenv("AUTH_TOKEN"),
    }
