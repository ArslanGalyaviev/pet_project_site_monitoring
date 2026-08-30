import logging


class Site:
    def __init__(
        self,
        url,
        timeout=5.0,
        check_interval=60,
        consecutive_errors=0,
        alert_sent=False,
    ):
        self.url = url
        self.timeout = timeout
        self.check_interval = check_interval
        self.consecutive_errors = consecutive_errors
        self.alert_sent = alert_sent

    def record_success(self):
        self.consecutive_errors = 0
        self.alert_sent = False

    def record_failure(self):
        self.consecutive_errors += 1
        if self.consecutive_errors >= 5 and not self.alert_sent:
            logging.critical(f"Сайт {self.url} долго не работает")
            self.alert_sent = True
