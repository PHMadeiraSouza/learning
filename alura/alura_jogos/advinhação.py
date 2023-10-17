def jogar():
    import random

    print("*******************************")
    print("bem vindo ao jogo de advinhação")
    print("*******************************")

    max_tentativas = 3
    total_de_tentativas = max_tentativas

    print("entre quais valores o computador pode escolher? ")

    n_min = input("mínimo: ")
    while n_min != int:
        try: 
            n_min = int(n_min)
            break
        except:
            
            print("escolha um numero inteiro!")
            n_min = input("mínimo: ")

    n_max = input("máximo: ")
    while n_min != int:
        try: 
            n_max = int(n_max)
            break
        except:
            print("escolha um numero inteiro!")
            n_max = input("máximo: ")


    numero_secreto = random.randrange(n_min, n_max+1)

    print(f"O numero secreto é {numero_secreto}")

    while total_de_tentativas > 0:
        if total_de_tentativas > 1:
            print(f"Restam {total_de_tentativas} de {max_tentativas} tentativas")
        elif total_de_tentativas == 1:
            print("Ultima tentativa")
        
        chute = int(input(f"digite um nummero de {n_min} até {n_max}: "))

        if numero_secreto == chute:
            print("você acertou")
            break
        else:
            if chute > numero_secreto:
                dica = "maior"
            else:
                dica = "menor"
            print("você errou, seu chute foi", dica, "que o numero secreto")
            print("+=======+")
        total_de_tentativas -= 1
    print("fim de jogo")

if (__name__ == "__main__"):
    jogar()