#include <iostream>

int main(int argc, char** argv){
    char nome[30];
    char endereço[30];
    int idade;

    printf("Nome: \n");
    scanf("%s", &nome);
    
    printf("Endereço: \n");
    scanf("%s", &endereço);

    printf("Idade: \n");
    scanf("%d", &idade);

    printf("\n Nome: %s", nome);
    printf("\n Endereço: %s", endereço);
    printf("\n Nome: %d", idade);

}