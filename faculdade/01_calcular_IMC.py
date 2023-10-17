def calcular_IMC():
    print("++++++++++++++++++++++++++++++++++++")
    print("   Bem Vindo á calculadora de IMC"   )
    print("++++++++++++++++++++++++++++++++++++")
    altura, peso = get_altura_e_peso()
    imc = peso / (altura ** 2)
    print(f"O seu IMC é {round(imc, 2)}")
    print(f"=== Sua condição é {tipo_corporal(imc)} ===")

def get_altura_e_peso():
    altura = input("Qual a sua altura (em centímetros): ")
    while altura.isnumeric() == False: 
        print("input inválido, tente novamente")
        altura = input("Qual a sua altura (em metros): ")
    altura = int(altura) / 100

    peso = input("qual o seu peso (em Kg): ")
    while peso.isnumeric() == False: 
        print("input inválido, tente novamente")
        peso = input("Qual o seu peso (em kg): ")
    peso = float(peso)
    return (altura, peso)

def tipo_corporal(imc):
    if imc >= 40:
        tipo_corporal = "Obesidade grau III"
    elif imc < 40 and imc >= 35:
        tipo_corporal = "Obesidade grau II"
    elif imc < 35 and imc >= 30:
        tipo_corporal = "Obesidade grau I"
    elif imc < 30 and imc >= 25:
        tipo_corporal = "Sobrepeso"
    elif imc < 25 and imc >= 18.6:
        tipo_corporal = "Normal"
    elif imc < 18.6:
        tipo_corporal = "Abaixo do normal"
    return tipo_corporal

if (__name__ == "__main__"):
    calcular_IMC()