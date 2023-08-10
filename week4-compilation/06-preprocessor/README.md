Consider the program constituted of the following two source files:
[preprocessor.c](preprocessor.c) and [preprocessor.h](preprocessor.h).

This program fails to compile due to missing header inclusions. Correct these
issues by writing the proper include preprocessor directives. The expected
output is:

```
./preprocessor
Please enter the amount of random number to generate:
10000000
Generated 10000000 numbers in 0.084871 seconds
```

To check the correctness of your program, use a
[Linux distribution with check50 installed](https://github.com/olivierpierre/comp26020-devcontainer).
In a terminal, with the source file in the local directory, check with this
command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2022-2023/week5-compilation/07-preprocessor
```
