from retry_lib import retry

contador = {"tentativas": 0}


@retry(max_retries=5, delay=1)
def funcao_instavel():
    contador["tentativas"] += 1
    if contador["tentativas"] < 3:
        raise ValueError("Falhou!")
    return "Sucesso!"


if __name__ == "__main__":
    print(funcao_instavel())
