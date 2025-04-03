from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allowed hosts for development
ALLOWED_HOSTS = ["*"]

# Logging level for development
LOGGING["loggers"][""]["level"] = "DEBUG" 
