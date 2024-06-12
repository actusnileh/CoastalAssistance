import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
YANDEX_MAPS_API = os.getenv("YANDEX_MAPS_API")
