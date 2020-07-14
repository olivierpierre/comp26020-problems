# Lecture 11 Problem 2

The program [macro.c](macro.c) generates a series of random numbers and outputs
the distribution of their value into several bins:

```shell
./macro
bin 0: [000 - 020[ *******************
bin 1: [020 - 040[ *******************
bin 2: [040 - 060[ *******************
bin 3: [060 - 080[ **********************
bin 4: [080 - 100[ ******************
```

There are several redundant hardcoded numbers in the code of `macro.c` that
should rather be defined as macros (constants) to ease the code clarity
and the possibilities of evolution. Fix this problem by introducing at least
3 macros:
- 


To check the correctness of your program, use CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `math.c`. In a terminal,
with that file in the local directory, check with this command:
```shell
check50 -l --log olivierpierre/comp26020-problems/master/lecture10/math
```
