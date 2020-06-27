# Lecture 4 Problem 1

Write a simple program printing the size of `int` variables, followed on the
next line by the size of `double` variables, followed on a third line by the
size of `unsigned long long` variables. On a last line, print the value of
the multiplication of these 3 sizes. The expected output (on a modern 64 bits
machine) is:

```
4
8
8
256
```

The source file should be named `sizes.c`.

To check the correctness of your program, use CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `goodbye.c`. In a terminal,
with that file in the local directory, check with this command:

```shell
check50 -l --log olivierpierre/comp26020-problems/master/lecture04/sizeof
```
