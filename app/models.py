import logging
from sqlmodel import SQLModel, Field


class Site(SQLModel, table=True):
    url: str = Field(default=None, primary_key=True)
    timeout: float = Field(default=5)
    check_interval: int = Field(default=10)
    consecutive_errors: int = Field(default=0)
    alert_sent: bool = Field(default=False)

    def record_success(self) -> None:
        self.consecutive_errors = 0
        self.alert_sent = False

    def record_failure(self) -> bool:
        self.consecutive_errors += 1
        if self.consecutive_errors >= 5 and not self.alert_sent:
            logging.critical(f"Сайт {self.url} долго не работает")
            self.alert_sent = True
            return True
        return False
