# Video 8 Problem 2

Consider the following program:

```c
#include <stdio.h>
#include <stdlib.h>

int add(int a, int b) {
    return a + b;
}

int main(int argc, char **argv) {
    if(argc == 3) {
        int a = atoi(argv[1]);
        int b = atoi(argv[2]);

        printf("%d + %d = %d\n", a, b, add(a, b));
    }
    return 0;
}
```

Modify the function `add` and its invocation so that it takes two `int` pointer
parameters. Examples of output:

```shell
./pointer2 10 20
10 + 20 = 30

./pointer2 154 -12
154 + -12 = 142
```

To check the correctness of your program, use CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `pointer2.c`. In a terminal,
with that file in the local directory, check with this command:
```shell
check50 -l --log olivierpierre/comp26020-problems/master/video08/pointer2
```
