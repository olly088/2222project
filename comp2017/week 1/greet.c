#include <stdio.h>

int main (int argc, char** argv)
{
    printf("What is your name?   ");
    char buffer[32];
    scanf("%[^\n]%*c", buffer);
    printf("Your name is %s\n", buffer);
    return 0;
}