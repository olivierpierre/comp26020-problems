The objective is to break down the program [module.c](module.c) into several
modules:

- `module1.c` and the corresponding header `module1.h`, containing
   `module1_function1` and `module1_function2`
- `module2.c` and `module2.h` containing `module2_function1`
- `module3.c` and `module3.h` containing `module3_function1` and `module3_enum`
- `main.c` containing the `main` function.

Take care of including in C files only the necessary headers. The expected
output is:

```shell
./module
module3_function1 called with parameter CASE2
res1: 84
res2: 1.000000
res3: 1595255563434
```

To check the correctness of your program, use the department VM image with check50 installed or alternatively CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io). In a terminal, with all the mentioned source files in
the local directory, check with this command:
```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2021-2022/week5-c++/03-module
```
