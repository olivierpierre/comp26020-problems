Consider the program constituted of the following two source files: [preprocessor.c](./comp26020-problems/week4-compilation/06-preprocessor/preprocessor.c) and [preprocessor.h](./comp26020-problems/week4-compilation/06-preprocessor/preprocessor.h).

This program fails to compile due to missing header inclusions.
Correct these issues by writing the proper include preprocessor directives.
The expected output is:

```
./preprocessor
Please enter the amount of random number to generate:
10000000
Generated 10000000 numbers in 0.084871 seconds
```

To check the correctness of your program, use a [suitable development environment](https://github.com/olivierpierre/comp26020-devcontainer/blob/master/README.md) with [check50 installed](exercise-set-1.html#installing-check50).
In a terminal, with the source file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/main/week4-compilation/06-preprocessor
```

**Submission:** once your work is ready please submit it [here](https://comp26020.uom.pierreolivier.eu/).