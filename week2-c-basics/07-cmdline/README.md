Write a C program that takes 3 floating point numbers as command line parameters and displays on the standard output the value of the multiplication of these 3 numbers. Examples of execution:

```shell
./cmdline 1.0 2.0 3.0
6.000000

./cmdline 1.45 2.78 3.25
13.100750
```

> **Warning**.
> Use the type `double` rather than `float` to hold these values in order to pass the checks.

To check the correctness of your program, use a [Linux distribution with check50 installed](https://github.com/olivierpierre/comp26020-devcontainer) and write your solution in a file named **`cmdline.c`**.
In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week2-c-basics/07-cmdline
```
