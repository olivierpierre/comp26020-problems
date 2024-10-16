The program [macro.c](./comp26020-problems/week4-compilation/01-macro/macro.c) generates a series of random numbers and outputs the distribution of their value into several bins:

```shell
./macro
bin 0: [000 - 020[ *******************
bin 1: [020 - 040[ *******************
bin 2: [040 - 060[ *******************
bin 3: [060 - 080[ **********************
bin 4: [080 - 100[ ******************
```

There are several redundant hardcoded numbers in the code of `macro.c` that should rather be defined as macros (constants) to ease the code clarity and the possibilities of evolution.
Fix this problem by introducing at least 2 macros:

- `SAMPLE_SIZE` defining the size (i.e. number of integers) of the array manipulated by the program -- currently 1000 in the provided code sample
- `MAX_VAL` defining the value that the generated random integers can take as the range `[0 - MAX_VAL[`, currently 100 in the code sample.

Define these macros to be 10 for `SAMPLE_SIZE` and 50 for `MAX_VAL`.
An example of expected output is:

```
./macro
bin 0: [000 - 010[ 
bin 1: [010 - 020[ **********
bin 2: [020 - 030[ ********************
bin 3: [030 - 040[ **************************************************
bin 4: [040 - 050[ ********************
```

To check the correctness of your program, use a use a [Linux distribution](https://github.com/olivierpierre/comp26020-devcontainer) with [check50 installed](exercise-set-1.html#installing-check50) and write your solution in a file named `macro.c`.
In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week4-compilation/01-macro
```