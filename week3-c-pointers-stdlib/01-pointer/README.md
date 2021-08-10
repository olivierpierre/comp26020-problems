Write a program that takes an integer as parameter and places it in a variable
of type `int`. The program then proceeds to print the value as well as the
address of the variable as follows:

```shell
./pointer 5
Variable contains 5 and is located @0x7ffcc6d1d7fc

./pointer 93
Variable contains 93 and is located @0x7fffec3b3dfc
```

!!! note "Printing pointers"
    Pointer can be printed in hexadecimal and prefixed with `0x` using the
    `%p` format specifier for `printf`.

To check the correctness of your program, use the department VM image with check50 installed or alternatively CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `pointer.c`. In a terminal,
with that file in the local directory, check with this command:
```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2021-2022/week3-c-pointers-stdlib/01-pointer
```
