from app.models import Site


def test_site_alert_triggers_after_5_failures():
    s = Site(url="https://www.hse.ru")
    for _ in range(5):
        s.record_failure()
    assert s.consecutive_errors == 5, "Счетчик ошибок после 5 неудач не равен 5"
    assert s.alert_sent, "Идентификатор не обновился после 5 неудач"


def test_site_resets_on_success():
    s = Site(url="https://www.hse.ru")
    for _ in range(5):
        s.record_failure()
    s.record_success()
    assert (
        s.consecutive_errors == 0
    ), "Не произошел сброс 5 неудач после успешного запрос"
    assert not s.alert_sent, "Идентификатор не обновился после удачи после 5 неудач"
