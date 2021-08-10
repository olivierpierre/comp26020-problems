Write a program taking a list of integers as command line parameters, storing
them in an array allocated with `malloc`, and sorting that array in increasing
order.

Output examples:

```shell
./malloc2 5 4 3 2 1
1 2 3 4 5 

./malloc2 546 874 18 13 87 54 4651 54 877 8 46351 87 654 657 654
8 13 18 54 54 87 87 546 654 654 657 874 877 4651 46351
```

To check the correctness of your program, use the department VM image with check50 installed or alternatively CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `malloc2.c`. In a terminal,
with that file in the local directory, check with this command:
```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2021-2022/week3-c-pointers-stdlib/06-malloc2
```
