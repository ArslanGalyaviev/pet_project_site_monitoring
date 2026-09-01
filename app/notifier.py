import aiosmtplib
import logging
from email.message import EmailMessage
from .config import SMTP_HOST, SMTP_PORT, SMTP_LOGIN, SMTP_PASSWORD, ALERT_RECIPIENT


async def send_alert_email(site_url, error_details):
    msg = EmailMessage()
    msg["Subject"] = f"АЛЕРТ: Сайт {site_url} не работает!"
    msg["From"] = SMTP_LOGIN
    msg["To"] = ALERT_RECIPIENT
    msg.set_content(f"Сайт: {site_url}\n Детали ошибки: {error_details}")
    try:
        async with aiosmtplib.SMTP(
            hostname=SMTP_HOST, port=SMTP_PORT, use_tls=True
        ) as server:
            await server.login(SMTP_LOGIN, SMTP_PASSWORD)
            await server.send_message(msg)
        logging.info(
            f"Уведомление об ошибке {site_url} успешно отправлен на {ALERT_RECIPIENT}"
        )
    except Exception as e:
        logging.error(f"Не удалось отправить email-уведомление для {site_url}: {e}")
