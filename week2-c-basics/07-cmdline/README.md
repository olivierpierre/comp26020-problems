Write a C program that takes 3 floating point numbers as command line parameters and displays on the standard output the value of the multiplication of these 3 numbers. Examples of execution:

```shell
./cmdline 1.0 2.0 3.0
6.000000

./cmdline 1.45 2.78 3.25
13.100750
```

> **Warning**.
> Use the type `double` rather than `float` to hold these values in order to pass the checks.

To check the correctness of your program, use a [suitable development environment](https://github.com/olivierpierre/comp26020-devcontainer/blob/master/README.md) with [check50 installed](exercise-set-1.html#installing-check50) and write your solution in a file named **`cmdline.c`**.
In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/main/week2-c-basics/07-cmdline
```

**Submission:** once your work is ready please submit it [here](https://comp26020.uom.pierreolivier.eu/).