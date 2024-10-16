Fix the memory leak contained in the following program:

```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    int *a = malloc(10 * sizeof(int));
    if(!a) return -1;

    for(int i=0; i<10; i++)
        a[i] = i*2;

    int *b = a;

    for(int i=0; i<10; i++)
        printf("%d ", b[i]);
    printf("\n");

    return 0;
}
```

The expected output is:
```shell
./malloc3
0 2 4 6 8 10 12 14 16 18
```

To check the correctness of your program, use a use a [Linux distribution](https://github.com/olivierpierre/comp26020-devcontainer) with [check50 installed](exercise-set-1.html#installing-check50) and write your solution in a file named `malloc3.c`.
In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week3-c-pointers-stdlib/05-malloc3
```