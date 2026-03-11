import os

class Config:

    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY", "change_this_secret_key")

    # Database location
    DATABASE = "database/database.db"

    # Business Configuration
    BUSINESS_NAME = "ContentForge Editorial Studio"
    SUPPORT_EMAIL = "your-email@gmail.com"

    # Production Limits
    DAILY_ORDER_LIMIT = 25

    # Delivery Windows (hours)
    DELIVERY_HOURS_DEMO = 2
    DELIVERY_HOURS_STANDARD = 5
    DELIVERY_HOURS_EXPRESS = 2

    # Demo Limits
    MAX_DEMO_PER_EMAIL = 1
    MAX_DEMO_PER_DAY = 5
