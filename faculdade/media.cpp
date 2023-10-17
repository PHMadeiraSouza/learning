#include <iostream>

int main(int argc, char** argv){
    float nota1;
    float nota2;
    float media;

    printf("Insira nota 1: ");
    scanf("%f", &nota1);
    printf("\n");

    printf("Insira nota 2: ");
    scanf("%f", &nota2);
    printf("\n");

    media = (nota1 + nota2) / 2;

    printf("media = %f", media);
}