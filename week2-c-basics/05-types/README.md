The following [code](./comp26020-problems/week2-c-basics/05-types/types.c) fails to compile due to a missing variable declaration:

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

To check the correctness of your program, use a [Linux distribution with check50 installed](https://github.com/olivierpierre/comp26020-devcontainer) and write your solution in a file named **`types.c`**.
In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week2-c-basics/05-types
```