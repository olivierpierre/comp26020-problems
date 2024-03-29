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
./pointer 10 20
10 + 20 = 30

./pointer 154 -12
154 + -12 = 142
```

To check the correctness of your program, use a
[Linux distribution with check50 installed](https://github.com/olivierpierre/comp26020-devcontainer)
and write your solution in a file named `pointer.c`. In a
terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2023-2024/week3-c-pointers-stdlib/01-pointer
```
