#include <stdio.h>
#include <stdlib.h>

struct s_rectangle {
    unsigned long long int width;
    unsigned long long int length;
};

void print_rectangle(struct s_rectangle r) {
    printf("Rectangle is %llu x %llu\n", r.width, r.length);
}

int main(int argc, char **argv) {
    struct s_rectangle r;
    unsigned long long int width;
    unsigned long long int length;

    if(argc == 3) {
        width = atoll(argv[1]);
        length = atoll(argv[2]);

        r.width = width;
        r.length = length;

        print_rectangle(r);
    }

    return 0;
}
