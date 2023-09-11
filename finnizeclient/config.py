import os

from dotenv import load_dotenv

load_dotenv()

# finnize api
FINNIZE_API_KEY = os.environ["FINNIZE_API_KEY"]
FINNIZE_API_SECRET = os.environ["FINNIZE_API_SECRET"]

# DEV ENVIRONMENT SET UP
FINNIZE_ENVIRONMENT = os.getenv("FINNIZE_ENVIRONMENT", default="False")

ROLE_ID = os.getenv("ROLE_ID", default="2")
NAME = os.getenv("NAME", default="guru")
CAN_LOGIN_ADMIN_SITE = os.getenv("CAN_LOGIN_ADMIN_SITE", default="False")
CAN_CREATE_STRATEGY = os.getenv("CAN_CREATE_STRATEGY", default="True")
USER_ID = os.environ["USER_ID"]
BROKER_ID = os.getenv("BROKER_ID", default="2")
