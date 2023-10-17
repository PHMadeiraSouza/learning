import tracemalloc
tracemalloc.start()

import advinhação
import forca

print("********************************")
print("    +++Escolha o seu jogo+++")
print("********************************")

print("(1) Forca ou (2) Advinhação")
jogo = int(input("qual o jogo?"))

if jogo == 1:
    print("jogando adivinhação sem def")
    forca.jogar()
    
elif jogo == 2:
    print("jogando adivinhação")
    advinhação.jogar()
    print(tracemalloc.get_traced_memory())


print(tracemalloc.get_traced_memory())
tracemalloc.stop()
