Enumerations can be used in C in combination with bitwise operations to define
*flags*, i.e. set of properties attached to objects, each object being able to
have 0 or several properties enabled.

Consider the following program:

```c
#include <stdio.h>

typedef enum {
    /* define FLAG1, FLAG2, FLAG3, FLAG4 */
} flags;

void print_flags(flags f) {

    if(f & FLAG1)
        printf("FLAG1 enabled\n");
    if(f & FLAG2)
        printf("FLAG2 enabled\n");
    if(f & FLAG3)
        printf("FLAG3 enabled\n");
    if(f & FLAG4)
        printf("FLAG4 enabled\n");
}

int main(int argc, char **argv) {
    flags f1 = FLAG1 | FLAG2;
    flags f2 = FLAG1 | FLAG2 | FLAG3;

    printf("f1:\n");
    print_flags(f1);

    printf("f2:\n");
    print_flags(f2);

    return 0;
}
```

The goal of the exercise is to write the definition of `flags` so that the
program behaves correctly, i.e. it should produce the following output:

```shell
./enum2
f1:
FLAG1 enabled
FLAG2 enabled
f2:
FLAG1 enabled
FLAG2 enabled
FLAG3 enabled
```

!!! note "Custom typedef values"
    Within a `typedef` definition, use `=` to set a particular integer value
    for an identifier, for example `FLAG1 = 42,`

!!! note "Bitwise operations in C"
    C offers operators working on the bitwise representation of variables:

    - bitwise AND: `&` and OR `|`
    - bitwise shift, left `<<` and right `>>`
    - etc. For more information see the *Bitwise logic and shifts operators*
      sections
      [here](https://en.cppreference.com/w/c/language/operator_arithmetic)

To check the correctness of your program, use the department VM image with check50 installed or alternatively CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `enum2.c`. In a terminal,
with that file in the local directory, check with this command:
```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2021-2022/week2-c-basics/17-enum2
```
