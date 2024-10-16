Consider the following [program](./comp26020-problems/week3-c-pointers-stdlib/01-pointer/pointer.c):

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

Modify the function `add` and its invocation so that it takes two `int` pointer parameters. Examples of output:

```shell
./pointer 10 20
10 + 20 = 30

./pointer 154 -12
154 + -12 = 142
```

To check the correctness of your program, use a use a [Linux distribution](https://github.com/olivierpierre/comp26020-devcontainer) with [check50 installed](exercise-set-1.html#installing-check50) and write your solution in a file named `pointer.c`.
In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week3-c-pointers-stdlib/01-pointer
```
