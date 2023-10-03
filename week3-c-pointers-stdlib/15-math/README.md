Write a C program reading a `double` with `scanf` and asking the user if he
wants this number to be floored or ceiled. Next, the program performs the 
requested operation and displays the result. Output examples:

```shell
./math
Input a number:
12.4
Input 0 for ceil, 1 for floor
0
13.000000

./math
Input a number:
45.87
Input 0 for ceil, 1 for floor
1
45.000000
```

To check the correctness of your program, use a
[Linux distribution with check50 installed](https://github.com/olivierpierre/comp26020-devcontainer)
and write your solution in a file named `math.c`. In a
terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2023-2024/week3-c-pointers-stdlib/15-math
```
