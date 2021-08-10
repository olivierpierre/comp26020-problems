Consider the following program printing a string to the standard output
character by character:

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

Alter the loop so as to use a `char *` pointer as the iterator and as the way
to access characters within the string for printing. The source code should
contain no square bracket. The expected output is:

```shell
./pointer4
hello, world!
```

To check the correctness of your program, use the department VM image with check50 installed or alternatively CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `pointer4.c`. In a terminal,
with that file in the local directory, check with this command:
```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2021-2022/week3-c-pointers-stdlib/10-pointer4
```
