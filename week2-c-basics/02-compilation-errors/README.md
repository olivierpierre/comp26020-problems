The following program is supposed to print a line on the standard output but
compilation fails due to several errors:

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

!!! hint "Hint"
    Trying to build the program will have the compiler highlight the errors.

To check the correctness of your program, use a
[Linux distribution with check50 installed](https://github.com/olivierpierre/comp26020-devcontainer)
and write your solution in a file named `compilation-errors.c`. In a
terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2022-2023/week2-c-basics/02-compilation-errors
```
