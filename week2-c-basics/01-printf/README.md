Write a C program displaying a large 11x9 characters 'C' using dashes.
The expected output is:

```c
   ######
 ##      ##
#
#
#
#
#
 ##      ##
   ######
```

To check the correctness of your program, use a use a [Linux distribution](https://github.com/olivierpierre/comp26020-devcontainer) with [check50 installed](exercise-set-1.html#installing-check50) and write your solution in a file named **`printf.c`**. In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week2-c-basics/01-printf
```