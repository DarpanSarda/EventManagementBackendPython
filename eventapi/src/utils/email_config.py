from pydantic import BaseModel, EmailStr
from fastapi_mail import ConnectionConfig
import os

class EmailSettings(BaseModel):
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "darpansarda77@gmail.com")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "Darpan@123")
    MAIL_FROM: EmailStr = os.getenv("MAIL_FROM", "darpansarda77@gmail.com")
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

email_settings = EmailSettings()

conf = ConnectionConfig(
    MAIL_USERNAME=email_settings.MAIL_USERNAME,
    MAIL_PASSWORD=email_settings.MAIL_PASSWORD,
    MAIL_FROM=email_settings.MAIL_FROM,
    MAIL_PORT=email_settings.MAIL_PORT,
    MAIL_SERVER=email_settings.MAIL_SERVER,
    MAIL_TLS=email_settings.MAIL_TLS,
    MAIL_SSL=email_settings.MAIL_SSL,
    USE_CREDENTIALS=True
)