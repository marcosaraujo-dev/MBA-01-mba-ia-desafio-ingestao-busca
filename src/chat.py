from search import search_prompt


def main():
    print("Inicializando sistema de busca...")
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    print("Sistema pronto. Digite 'sair' para encerrar.\n")

    while True:
        try:
            pergunta = input("Você: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando...")
            break

        if not pergunta:
            continue

        if pergunta.lower() in ("sair", "exit", "quit"):
            print("Encerrando...")
            break

        try:
            resposta = chain.invoke({"pergunta": pergunta})
            print(f"\nAssistente: {resposta}\n")
        except Exception as e:
            print(f"\nErro ao processar pergunta: {e}\n")


if __name__ == "__main__":
    main()
