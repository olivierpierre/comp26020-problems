Write a simple program printing the size of `int` variables, followed on the
next line by the size of `double` variables, followed on a third line by the
size of `unsigned long long int` variables. On a last line, print the value of
the multiplication of these 3 sizes. The expected output (on a modern 64 bits
machine) is:

```
4
8
8
256
```

To check the correctness of your program, use the department VM image with check50 installed or alternatively CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `sizes.c`. In a terminal,
with that file in the local directory, check with this command:

```shell
check50 -l --log olivierpierre/comp26020-problems/2020-2021/week2-c-basics/05-sizes
```
