import re
import os
from os import environ, getenv
from Script import script

# --- Helper Functions ---
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "on"]:
        return True
    elif value.lower() in ["false", "no", "0", "off"]:
        return False
    return default

# =========================================================
# ðŸ¤– BOT INFO & CREDENTIALS
# =========================================================
SESSION = environ.get('SESSION', 'Webavbot')
API_ID = int(environ.get('API_ID', 'Enter Your Api Id'))
API_HASH = environ.get('API_HASH', 'Enter Your Api Hash')
BOT_TOKEN = environ.get('BOT_TOKEN', 'Enter Your Bot Token')

# Admin Settings
ADMINS = [int(x) for x in environ.get('ADMINS', '8747490676').split()]
OWNER_USERNAME = environ.get("OWNER_USERNAME", 'ratul1277')

# =========================================================
# ðŸ—„ï¸ DATABASE CONNECTION
# =========================================================
DB_URL = environ.get('DATABASE_URI', "mongodb+srv://file-to-url:file-to-url-123@cluster0.w3uex4d.mongodb.net/?appName=Cluster0")
DB_NAME = environ.get('DATABASE_NAME', "testing")

# =========================================================
# ðŸ“¢ CHANNELS & LOGS
# =========================================================
# Mandatory Channels
BIN_CHANNEL = int(environ.get("BIN_CHANNEL", '-1003965015923'))
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", '-1003949564466'))

# Feature Specific Logs
PREMIUM_LOGS = int(environ.get("PREMIUM_LOGS", '-1003701301311'))
VERIFIED_LOG = int(environ.get('VERIFIED_LOG', '-1003966392215'))
SUPPORT_GROUP = int(environ.get("SUPPORT_GROUP", "-1003941765762"))

# Auth Channels (Safe Parsing)
auth_channel_str = environ.get("AUTH_CHANNEL", "-1003790425512")
AUTH_CHANNEL = [int(x) for x in auth_channel_str.split()] if auth_channel_str else []

# =========================================================
# ðŸ”— LINKS & URLS
# =========================================================
CHANNEL = environ.get('CHANNEL', 'https://t.me/I_LinkerUpdates/')
SUPPORT = environ.get('SUPPORT', 'https://t.me/I_LinkerChats/')
TUTORIAL_LINK_1 = environ.get('TUTORIAL_LINK_1', 'https://t.me/1')
TUTORIAL_LINK_2 = environ.get('TUTORIAL_LINK_2', 'https://t.me/2')

# =========================================================
# ðŸ” VERIFICATION & SHORTENER
# =========================================================
IS_VERIFY = is_enabled(environ.get("IS_VERIFY", "True"), True)
IS_SECOND_VERIFY = is_enabled(environ.get("IS_SECOND_VERIFY", "True"), True)
IS_SHORTLINK = is_enabled(environ.get('IS_SHORTLINK', "True"), True)

# Verification Config
VERIFY_EXPIRE = int(environ.get('VERIFY_EXPIRE', 1)) # In Minutes/Hours based on logic
SHORTLINK_URL = environ.get('SHORTLINK_URL', 'cuty.io')
SHORTLINK_API = environ.get('SHORTLINK_API', 'fe5e689e49f014fbfc6978495')

# Second Verification Config
SHORTLINK_WEBSITE2 = environ.get("SHORTENER_WEBSITE2", "gplinks.com")
SHORTLINK_API2 = environ.get("SHORTENER_API2", "3cd0d6f8f5abfdb64341f77a88d3fb6b1f6851b7")

# =========================================================
# âš™ï¸ SETTINGS & LIMITS
# =========================================================
FSUB = is_enabled(environ.get("FSUB", "True"), True)
ENABLE_LIMIT = is_enabled(environ.get("ENABLE_LIMIT", "True"), True)
MAINTENANCE_MODE = is_enabled(environ.get("MAINTENANCE_MODE", "False"), False)

# Time & Rate Limits
TIMEZONE = environ.get("TIMEZONE", "Asia/Dhaka")
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))
SLEEP_THRESHOLD = int(getenv('SLEEP_THRESHOLD', '60'))
RATE_LIMIT_TIMEOUT = int(environ.get("RATE_LIMIT_TIMEOUT", "600"))

# File Limits
MAX_FILES = int(environ.get("MAX_FILES", "10"))
BATCH_LIMIT = int(environ.get('BATCH_LIMIT', 5))

# =========================================================
# ðŸ–¼ï¸ MEDIA & CAPTIONS
# =========================================================
QR_CODE = environ.get('QR_CODE', 'https://graph.org/file/6afb4093d5ec5c4176979.jpg')
VERIFY_IMG = environ.get("VERIFY_IMG", "https://graph.org/file/1669ab9af68eaa62c3ca4.jpg")
AUTH_PICS = environ.get('AUTH_PICS', 'https://i.ibb.co.com/bjNL5Csj/file-00000000279871fa93dc17179e399163.png')
PICS = environ.get('PICS', 'https://i.ibb.co.com/bjNL5Csj/file-00000000279871fa93dc17179e399163.png')
FILE_PIC = environ.get('FILE_PIC', 'https://i.ibb.co/bj4My0bW/photo-2025-07-21-02-15-21-7529360175656861700.jpg')

FILE_CAPTION = environ.get('FILE_CAPTION', script.CAPTION)

# =========================================================
# ðŸŒ SERVER & APP CONFIG
# =========================================================
WORKERS = int(getenv('WORKERS', '4'))
MULTI_CLIENT = False
name = str(environ.get('name', 'infinity-linker'))

# Heroku & Port Config
if 'DYNO' in environ:
    ON_HEROKU = True
    APP_NAME = str(getenv('APP_NAME'))
else:
    ON_HEROKU = False
    APP_NAME = None

PORT = int(getenv('PORT', '8080'))
NO_PORT = is_enabled(getenv("NO_PORT", "True"), True)
HAS_SSL = is_enabled(getenv("HAS_SSL", "True"), True)
BIND_ADDRESS = getenv("WEB_SERVER_BIND_ADDRESS", "127.0.0.1")

# URL Generation
# Use provided URL from env, or generate based on FQDN/IP
custom_url = environ.get("URL")
if custom_url:
    URL = custom_url
else:
    FQDN = getenv("FQDN", BIND_ADDRESS)
    PROTOCOL = "https" if HAS_SSL else "http"
    PORT_SEGMENT = "" if NO_PORT else f":{PORT}"
    URL = f"{PROTOCOL}://{FQDN}{PORT_SEGMENT}/"

# Default fallback if nothing works (Matches your provided koyeb link)
if not URL or URL == "/":
    URL = "https://web-production-525b6.up.railway.app/"
    
