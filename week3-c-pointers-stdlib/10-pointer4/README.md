Consider the following program printing a string to the standard output character by character:

```c
#include <stdio.h>

int main(int argc, char **argv) {
    char *string = "hello, world!\n";

    int i = 0;
    while(string[i] != '\0')
        printf("%c", string[i++]);

    return 0;
}
```

Alter the loop to use a `char *` pointer as the iterator and as the way to access characters within the string for printing.
The source code should contain no square bracket.
The expected output is:

```shell
./pointer4
hello, world!
```

To check the correctness of your program, use a [suitable development environment](https://github.com/olivierpierre/comp26020-devcontainer/blob/master/README.md) with [check50 installed](exercise-set-1.html#installing-check50)
and write your solution in a file named **`pointer4.c`**. In a
terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/main/week3-c-pointers-stdlib/10-pointer4
```

**Submission:** once your work is ready please submit it [here](https://comp26020.uom.pierreolivier.eu/).