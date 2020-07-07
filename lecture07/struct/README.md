# Lecture 7 Problem 1

Consider the following structure:

```c
struct timestamp {
    unsigned int hour;
    unsigned int minute;
    unsigned int second;
}
```

Using this structure, write a C program adding two timestamps and displaying
the result on the standard output. The program takes 6 command line parameters
corresponding to the two timestamps. The addition is realized in a function
named `add_timestamps` that takes 2 timestamp parameters and return the
sum as a timestamp. Here are some output examples:

```shell
# 5h11m44s + 12h30m3s = 17h41m47s
./timestamp 5 11 44 12 30 3
17 41 47
./timestamp 10 30 50 1 5 15
11 36 05
./timestamp 14 12 5 22 5 0
36 17 5
```

To check the correctness of your program, use CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `struct.c`. In a terminal,
with that file in the local directory, check with this command:
```shell
check50 -l --log olivierpierre/comp26020-problems/master/lecture07/struct
```
