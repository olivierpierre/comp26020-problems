# Video 13 Problem 1

In C, characters are encoded in memory using ascii code. Knowing that there
is a constant offset between the code for a given letter in lowecase and the
code for that letter in capital, complete the `capitalize` function in the
program [ascii.c](ascii.c) presented below:

```c
#include <stdio.h>

char *alphabet = "abcdefghijklmnopqrstuvwxyz";

char capitalize(char c) {
    /* complete here */
}

int main(int argc, char **argv) {
    for(int i=0; i<26; i++)
        printf("capital %c: %c\n",
            alphabet[i], capitalize(alphabet[i]));

    return 0;
}
```

!!! note "Ascii code in C" 
     - When printed as an integer with the `%d` marker, the ascii code for a
       given `char` variable can be displayed.
     - You can also check out some ascii tables such as 
       [this one](http://www.asciitable.com/).

The expected output is:

```shell
capital a: A
capital b: B
capital c: C
capital d: D
capital e: E
capital f: F
# ...
capital z: Z
```

To check the correctness of your program, use CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `ascii.c`. In a terminal,
with that file in the local directory, check with this command:
```shell
check50 -l --log olivierpierre/comp26020-problems/master/video13/ascii
```
