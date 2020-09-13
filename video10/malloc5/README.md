# Video 10 Problem 5

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
./malloc5
0 2 4 6 8 10 12 14 16 18
```

To check the correctness of your program, use CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `malloc5.c`. In a terminal,
with that file in the local directory, check with this command:
```shell
check50 -l --log olivierpierre/comp26020-problems/master/video10/malloc5
```
