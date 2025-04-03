from .base import *
from pathlib import Path
import environ
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()

# Read env variables
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allowed hosts for production
ALLOWED_HOSTS = ['*']

# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Logging level for production
LOGGING["loggers"][""]["level"] = "ERROR"