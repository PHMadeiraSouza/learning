import random
import unicodedata 

def jogar():
    print("******************************")
    print("  bem vindo ao jogo de forca")
    print("******************************")

    
    palavra_secreta = select_palavra_secreta()
    p_s_encriptada = ["_" for char in palavra_secreta]

    chutes = []
    fim_de_jogo = False

    print("jogando...")

    while  fim_de_jogo == False:
        print(chutes)
        
        #print palavra secreta encriptada
        print(" ".join(str(char) for char in p_s_encriptada))

        #chute do usuario
        chute = (input("qual letra? ")).strip().lower()
        while not chute.isalpha() or len(chute) != 1:
            print("chute inválido")
            chute = input("qual letra? ").strip().lower()


        chute_in_palavra_secreta(chute, palavra_secreta,chutes,p_s_encriptada)     

        fim_de_jogo = jogo_finalizado(palavra_secreta, p_s_encriptada, len(chutes))

    print(" ".join(char for char in p_s_encriptada))

    print("Fim de jogo")

def chute_in_palavra_secreta(chute, palavra_secreta,chutes,p_s_encriptada):
    chute_está_correto = False
    if chute in palavra_secreta:
            for pos, char in enumerate(palavra_secreta):
                if remove_non_ascii_normalized(char) == remove_non_ascii_normalized(chute):
                    p_s_encriptada[pos] = char
                    chute_está_correto = True
    elif chute not in chutes:
        chutes.append(chute) 
    return chute_está_correto

def jogo_finalizado(palavra_secreta, p_s_encriptada, n_chutes):
        finalizado = False           
        if n_chutes >= round((len(palavra_secreta) * 3) / 2):
            finalizado = True
            print("Você Perdeu")

        elif "_" not in p_s_encriptada:
            if palavra_secreta == "".join(char for char in p_s_encriptada):
                finalizado = True
                print("")
                print("Você Ganhou")
            else:
                print("algo está errado")
        return finalizado

def select_palavra_secreta():
    arquivo = open("alura_jogos\palavras.txt", 'r')
    palavras = []
    for linha in arquivo:
        palavras.append(linha.strip().lower())
    arquivo.close()
    palavra_secreta = random.choice(palavras).strip().lower()
    return palavra_secreta

def remove_non_ascii_normalized(string: str) -> str:
    normalized = unicodedata.normalize('NFD', string)
    return normalized.encode('ascii', 'ignore').decode('utf8').casefold()

if (__name__ == "__main__"):
    jogar()