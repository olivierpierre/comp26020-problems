Write a simple program printing the size of `int` variables, followed on the next line by the size of `double` variables, followed on a third line by the size of `unsigned long long int` variables.
On a last line, print the value of the multiplication of these 3 sizes. The expected output (on a modern 64 bits machine) is:

```
4
8
8
256
```

To check the correctness of your program, use a use a [Linux distribution](https://github.com/olivierpierre/comp26020-devcontainer) with [check50 installed](exercise-set-1.html#installing-check50) and write your solution in a file named **`sizes.c`**.
In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week2-c-basics/04-sizes
```
