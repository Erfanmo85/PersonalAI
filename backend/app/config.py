import os
from dotenv import load_dotenv

load_dotenv()

def _list(name):
    return [x.strip() for x in os.getenv(name, "").split(",") if x.strip()]

BASE_URL = os.getenv("BEATAPI_BASE_URL", "https://direct.beatapi.io/v1")
API_KEY = os.getenv("BEATAPI_API_KEY", "")
PROPOSERS = _list("PROPOSERS")
JUDGE = os.getenv("JUDGE", "")
PROPOSER_MAX_TOKENS = int(os.getenv("PROPOSER_MAX_TOKENS", "4000"))
JUDGE_MAX_TOKENS = int(os.getenv("JUDGE_MAX_TOKENS", "6000"))
APP_TOKEN = os.getenv("APP_TOKEN", "")
CORS_ORIGINS = _list("CORS_ORIGINS")
TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "90"))
BOT_NAME = os.getenv("BOT_NAME", "مستشار")
BOT_DESCRIPTION = os.getenv("BOT_DESCRIPTION", "")
USER_PROFILE = os.getenv("USER_PROFILE", "")
SHARE_PROFILE = os.getenv("SHARE_PROFILE_WITH_PROPOSERS", "false").lower() == "true"
