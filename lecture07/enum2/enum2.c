#include <stdio.h>

typedef enum {
    /* define FLAG1, FLAG2, FLAG3, FLAG4 */
} flags;

void print_flags(flags f) {

    if(f & FLAG1)
        printf("FLAG1 enabled\n");
    if(f & FLAG2)
        printf("FLAG2 enabled\n");
    if(f & FLAG3)
        printf("FLAG3 enabled\n");
    if(f & FLAG4)
        printf("FLAG4 enabled\n");
}

int main(int argc, char **argv) {
    flags f1 = FLAG1 | FLAG2;
    flags f2 = FLAG1 | FLAG2 | FLAG3;

    printf("f1:\n");
    print_flags(f1);

    printf("f2:\n");
    print_flags(f2);

    return 0;
}
