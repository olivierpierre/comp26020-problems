Write a C program taking an integer `n` as command line parameter and sleeping
for `n` seconds. The execution time of the `sleep` function is measured and
displayed. Examples output:

```shell
./time 3
sleep duration: 3.000082 seconds

./time 5
sleep duration: 5.000108 seconds
```

To check the correctness of your program, use a Linux distribution with
check50 installed or alternatively CS50 [sandbox](https://sandbox.cs50.io/) or
[IDE](https://code.cs50.io/) and write it in a file named `time.c`. In a terminal,
with that file in the local directory, check with this command:
```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2022-2023/week3-c-pointers-stdlib/07-time
```
