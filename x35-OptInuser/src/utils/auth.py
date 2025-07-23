# src/utils/auth.py
from datetime import datetime

token_cache = {
    "token": None,
    "expires_at": None
}