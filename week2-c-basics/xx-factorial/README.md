Write a C program taking an integer as command line parameter and displaying
the factorial of that integer on the standard output as follows:
```
./factorial 10
10! = 3628800

./factorial 15
15! = 1307674368000

./factorial 1
1! = 1
```

We assume that the parameter value can be up to 20, the maximum number which
factorial can be stored in a 64 bits unsigned integer.

To check the correctness of your program, use the department VM image with check50 installed or alternatively CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `factorial.c`. In a
terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2021-2022/week2-c-basics/12-factorial
```
