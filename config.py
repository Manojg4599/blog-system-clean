import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change_this_secret_key")
    DATABASE = "database.db"

    # Business Configuration
    BUSINESS_NAME = "RankRise Content Studio"
    SUPPORT_EMAIL = "your-email@gmail.com"

    # Daily production limit
    DAILY_LIMIT = 25

    # Delivery window
    DELIVERY_HOURS_DEMO = 48
    DELIVERY_HOURS_PAID = 24
