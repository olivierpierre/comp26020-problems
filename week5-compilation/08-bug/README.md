The following program, [bug.c](bug.c), contains several memory corruption bugs:

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

Use GDB to debug this program and fix the bugs. An example of expected
execution is as follows:

```shell

```

To check the correctness of your program, use CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `bug.c`. In a terminal,
with that file in the local directory, check with this command:
```shell
check50 -l --log olivierpierre/comp26020-problems/master/week5-c++/08-bug
```
