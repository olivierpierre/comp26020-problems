#include <stdio.h>
#include "module1.h"
#include "module2.h"

int main(int argc, char **argv) {
    printf("Hello, this is main\n");
    f1();
    f2();
    return 0;
}
