The following code fails to compile due to a missing variable declaration:

```c
#include <stdio.h>

int main() {

    variable = 10;

    printf("variable is %u\n", variable);

    return 0;
}
```

Edit the code to have it compile and run successfully. The expected output is:
```
variable is 10
```

To check the correctness of your program, use the department VM image with check50 installed or alternatively CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `types.c`. In a terminal,
with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2022-2023/week2-c-basics/05-types
```
