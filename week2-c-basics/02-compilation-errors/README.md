The following [program](./comp26020-problems/week2-c-basics/02-compilation-errors/compilation-errors.c) is supposed to print a line on the standard output, but compilation fails due to several errors:

```c
#include <tdio.h>

void man() {
    printf("This should work!\n");
    retur 0;
}
```

Correct the program to have it display the following output:
```shell
This should work!
```

> Hint: trying to build the program will have the compiler highlight the errors.

To check the correctness of your program, use a use a [Linux distribution](https://github.com/olivierpierre/comp26020-devcontainer) with [check50 installed](exercise-set-1.html#installing-check50) and write your solution in a file named **`compilation-errors.c`**.
In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week2-c-basics/02-compilation-errors
```