#include <stdio.h>

class Pair {
public:
    int x;
    int y;
};

int main(int argc, char **argv) {
    Pair p;

    p.x = 10;
    p.y = 20;

    printf("p.x is %d, p.y is %d\n", p.x, p.y);

    return 0;
}
