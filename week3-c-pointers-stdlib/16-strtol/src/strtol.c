#include <stdio.h>
#include <stdlib.h>

int get_string(char *buf, int size) {
    char *ret;

    printf("please enter an integer number (base 10): ");
    ret = fgets(buf, 128, stdin);
    if(ret == NULL) {
        perror("fgets");
        return -1;
    }

    // remove the end of line character
    for(int i=0; i<strlen(buf); i++)
        if(buf[i] == '\n') {
            buf[i] = '\0';
            break;
        }

    return 0;
}
int convert_and_print(char *buf) {
    int result = atoi(buf);
    printf("you have entered: %d\n", result);

    return 0;
}

int main(int argc, char **argv) {
    char buf[128];

    if(get_string(buf, 128))
        return -1;

    if(convert_and_print(buf))
        return -1;

    return 0;
}
