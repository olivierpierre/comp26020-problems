The following code fails to compile due to a missing variable declaration:

```c
#include <stdio.h>

int main() {

    variable = -725230241886380040;

    printf("variable is %lld\n", variable);

    return 0;
}
```

Edit the code to have it compile and run successfully. The expected output is:
```
variable is -725230241886380040
```

To check the correctness of your program, use the department VM image with check50 installed or alternatively CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `types.c`. In a terminal,
with that file in the local directory, check with this command:

```shell
check50 -l --log olivierpierre/comp26020-problems/2020-2021/week2-c-basics/06-types
```
