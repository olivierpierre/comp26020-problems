Write a C program using `malloc` to allocate an array able to contain 10 `int`, fill this array with the 10 first natural number (starting with 0).
The expected output is:

```shell
./malloc4
0
1
2
3
4
5
6
7
8
9
```

To check the correctness of your program, use a use a [Linux distribution](https://github.com/olivierpierre/comp26020-devcontainer) with [check50 installed](exercise-set-1.html#installing-check50) and write your solution in a file named `malloc4.c`.
In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week3-c-pointers-stdlib/11-malloc4
```