The program [macro-conditional.c](macro-conditional.c) is a variant of the
program presented in the [previous exercize](../macro), where many debug
messages are printed on the standard output:


```shell
./macro-conditional
[DEBUG] Allocating memory
[DEBUG] Allocation successfull
[DEBUG] Filling array
[DEBUG] Generated 1000 random numbers
[DEBUG] Dividing numbers into bins
[DEBUG] Printing results
bin 0: [000 - 020[ ********************
bin 1: [020 - 040[ *******************
bin 2: [040 - 060[ ********************
bin 3: [060 - 080[ ********************
bin 4: [080 - 100[ *******************
[DEBUG] Printing done
[DEBUG] Memory freed
```

Update the program so that the display of the debug output happens only when
the macro `DEBUGMODE` is defined. Do not define the macro itself in the code,
we will rather use the
[-D](https://gcc.gnu.org/onlinedocs/gcc/Preprocessor-Options.html) gcc
parameter to do so at compile time:

```
gcc -DDEBUGMODE macro-conditional.c -o macro-conditional
./macro-conditional
# Debug output displayed

gcc macro-conditional.c -o macro-conditional
./macro-conditional
# Debug output suppressed
```


To check the correctness of your program, use the department VM image with check50 installed or alternatively CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `macro-conditional.c`. In a
terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2021-2022/week5-compilation/02-macro-conditional
```
