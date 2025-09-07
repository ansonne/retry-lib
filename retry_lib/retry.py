import time
import functools
import logging
from typing import Callable, Type, Tuple, Any, Optional


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def retry(
    max_retries: int = 3,
    delay: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[int, Exception], None]] = None,
) -> Callable[..., Any]:
    """
    Decorador para reexecutar uma função em caso de erro.

    Args:
        max_retries: número máximo de tentativas.
        delay: tempo em segundos entre as tentativas.
        exceptions: exceções que disparam retry.
        on_retry: callback opcional chamado a cada falha
            (recebe tentativa e exceção).
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_retries + 1):
                try:
                    logger.info(
                        f"Executando {func.__name__} (tentativa {attempt})"
                    )
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(f"Tentativa {attempt} falhou: {e}")
                    if on_retry:
                        on_retry(attempt, e)
                    if attempt == max_retries:
                        logger.error(
                            f"Função {func.__name__} falhou após "
                            f"{max_retries} tentativas"
                        )
                        raise
                    time.sleep(delay)

        return wrapper

    return decorator
