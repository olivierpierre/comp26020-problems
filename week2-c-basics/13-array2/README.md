Write a program that takes up to 10 integers as command line parameters. These
parameters are converted to integer types into an array of `int` named `array`.
Then, the program iterates over the array and outputs if each number is even or
odd as follows:

```shell
./array2 1 2 3 4 5 6 
1 is odd 
2 is even 
3 is odd 
4 is even 
5 is odd 
6 is even

./array2 5 5 120
5 is odd
5 is odd
120 is even
```

!!! note "Modulo in C"
    The modulo operator in C is `%`, for example: `42 % 2` evaluates to `0`
    and `41 % 2` evaluates to `1`.

To check the correctness of your program, use the department VM image with check50 installed or alternatively CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `array2.c`. In a terminal,
with that file in the local directory, check with this command:
```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2021-2022/week2-c-basics/13-array2
```