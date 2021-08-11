The program below uses integer to represent days of the week, 0
corresponding to Monday, 1 to Tuesday, etc.

```c
#include <stdio.h>

int main(int argc, char **argv) {
    int d = 2;

    printf("Today is: ");
    switch(d) {
        case 0:
            printf("Monday\n");
            break;
        case 1:
            printf("Tuesday\n");
            break;
        case 2:
            printf("Wednesday\n");
            break;
        case 3:
            printf("Thursday\n");
            break;
        case 4:
            printf("Friday\n");
            break;
        case 5:
            printf("Saturday\n");
            break;
        case 6:
            printf("Sunday\n");
            break;

        default:
            printf("Unknown day...\n");
    }
    return 0;
}
```

Replace the use of integers with that of an enumeration named `enum day`,
defining constants for days: `MONDAY`, `TUESDAY`, etc.

The expected output is:

```bash
./enum
Today is: Wednesday
```

To check the correctness of your program, use the department VM image with check50 installed or alternatively CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `enum.c`. In a terminal,
with that file in the local directory, check with this command:
```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2021-2022/week2-c-basics/12-enum
```