#include <stdio.h>

int main(int argc, char **argv) {
    char string[8];

    string[0] = 'h';
    string[1] = 'i';
    string[2] = ' ';
    string[3] = 't';
    string[4] = 'h';
    string[5] = 'e';
    string[6] = 'r';
    string[7] = 'e';
    string[8] = '\n';

    printf("%s\n", string);

    return 0;
}
