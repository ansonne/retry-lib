import pytest
from retry_lib import retry


def test_retry_sucesso():
    @retry(max_retries=3)
    def ok():
        return 42

    assert ok() == 42


def test_retry_falha():
    chamadas = {"count": 0}

    @retry(max_retries=2, delay=0.1)
    def falha():
        chamadas["count"] += 1
        raise ValueError("Erro!")

    with pytest.raises(ValueError):
        falha()

    assert chamadas["count"] == 2
