The following program, [bug.c](./comp26020-problems/week4-compilation/08-bug/bug.c), contains several memory corruption bugs:

```c
#include <stdio.h>
#include <stdlib.h>

int array[1000];

int main(int argc, char **argv) {
	int x;

	for(int i = 0; i < 10000; i++){
		int ran_num = rand()% 1000;
		array[i] = ran_num;
	}

	printf("Please enter an integer between 0 and 9999: ");
	scanf("%d", x);

	printf("array[%d] = %d\n", x, array[x]);
}
```

Use GDB to debug this program and fix the bugs. An example of expected execution is as follows:

```shell
Please enter an integer between 0 and 9999: 10
array[10] = 362
```

Note that you won't necessarily get 362 as the array's content is generated randomly, the important part is that the program does not segfault.

To check the correctness of your program, use a use a [Linux distribution](https://github.com/olivierpierre/comp26020-devcontainer) with [check50 installed](exercise-set-1.html#installing-check50) and write your solution in a file named `bug.c`.
In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week4-compilation/08-bug
```
