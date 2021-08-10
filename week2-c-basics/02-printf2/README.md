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

To check the correctness of your program, use the department VM image with check50 installed or alternatively CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `printf2.c`. In a terminal,
with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2021-2022/week2-c-basics/02-printf2
```
