Write a C program that takes 3 floating point numbers as command line
parameters and displays on the standard boutput the value of the multiplication
of these 3 numbers. Examples of execution:

```shell
./cmdline 1.0 2.0 3.0
6.000000

./cmdline 1.45 2.78 3.25
13.100750
```

!!! warning "Warning"
    Use the type `double` rather than `float` to hold these values in order to
    pass the checks.

To check the correctness of your program, use a Linux distribution with
check50 installed or alternatively CS50 [sandbox](https://sandbox.cs50.io/) or
[IDE](https://code.cs50.io/) and write it in a file named `cmdline.c`. In a terminal,
with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2022-2023/week2-c-basics/07-cmdline
```
