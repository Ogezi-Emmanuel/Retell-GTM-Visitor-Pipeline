
import os
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
MIN_TIME_ON_PAGE_SECS = int(os.getenv("MIN_TIME_ON_PAGE_SECS", 30))
TARGET_PAGE_PATH = os.getenv("TARGET_PAGE_PATH", "/pricing")
