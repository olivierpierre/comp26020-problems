Write a program that takes up to 10 integers as command line parameters. These
parameters are converted to integer types into an array of `int` named `array`.
Then, the program sorts the array by increasing value and prints the resulat as
follows:

```shell
./array2 5 4 6 2 1 3 
1 2 3 4 5 6

./array2 5 5 120
5 5 120
```

To check the correctness of your program, use the department VM image with check50 installed or alternatively CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `array2.c`. In a terminal,
with that file in the local directory, check with this command:
```shell
check50 -l --log olivierpierre/comp26020-problems/2020-2021/week2-c-basics/11-array2
```
