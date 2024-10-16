The program [strtol.c](strtol.c) converts a string entered by the user into an integer and prints it on the standard output.
The conversion is realised with `atoi`, and as such it is not robust in case of malformed strings as well as under/overflows.

Modify the implementation of the function `convert_and_print` in this program to use `strtol` for the conversion rather than `atoi`, and make the program more robust against improper inputs.
Output examples:

```shell
$ ./strtol
please enter an integer number (base 10): 1234
you have entered: 1234

$ ./strtol
please enter an integer number (base 10): foo
invalid string

$ ./strtol
please enter an integer number (base 10): 100000000000000000000
under/overflow

$ ./strtol 
please enter an integer number (base 10): -100000000000000000000
under/overflow
```

To check the correctness of your program, use a use a [Linux distribution](https://github.com/olivierpierre/comp26020-devcontainer) with [check50 installed](exercise-set-1.html#installing-check50) and write your solution in a file named `strtol.c`.
In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week3-c-pointers-stdlib/16-strtol
```
