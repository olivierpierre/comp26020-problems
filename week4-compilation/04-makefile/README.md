Consider the program compiled from the following files:

- [main.c](./comp26020-problems/week4-compilation/04-makefile/main.c)
- [module1.c](./comp26020-problems/week4-compilation/04-makefile/module1.c) and the corresponding header [module1.h](./comp26020-problems/week4-compilation/04-makefile/module1.h)
- [module2.c](./comp26020-problems/week4-compilation/04-makefile/module2.c) and the corresponding header [module2.h](./comp26020-problems/week4-compilation/04-makefile/module2.h)

Write a `Makefile` automating the compilation of this program.
It should contain intermediate rules compiling 1) C source files into object file and 2) linking object files into the final executable which name should be `prog`.
Include also a `clean` rule to delete the executable and intermediate object files.

You can download all the aforementioned source filed in a compressed archive [here](./comp26020-problems/week4-compilation/04-makefile/src.zip).

To check the correctness of your program, use a use a [Linux distribution](https://github.com/olivierpierre/comp26020-devcontainer) with [check50 installed](exercise-set-1.html#installing-check50).
In a terminal, with all source files as well as the Makefile in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week4-compilation/04-makefile
```
