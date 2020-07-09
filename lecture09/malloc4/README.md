# Lecture 9 Problem 4

Consider the following program:
```c
#include <stdio.h>
#include <stdlib.h>

void *my_realloc(void *ptr, size_t old_size, size_t new_size) {
    /* complete here */
}

int main(int argc, char **argv) {
    /* first malloc space for 5 int */
    int *array = malloc(5 * sizeof(int));
    if(!array) return -1;

    for(int i=0; i<5; i++) {
        array[i] = i*10;
        printf("before realloc, array[%d] = %d\n", i, array[i]);
    }

    /* expand the size to 10 int */
    array = my_realloc(array, 5*sizeof(int), 10*sizeof(int));
    if(!array) return -1;

    for(int i=5; i<10; i++)
        array[i] = i*10;

    for(int i=0; i<10; i++)
        printf("after realloc, array[%d] = %d\n", i, array[i]);

    free(array);
    return 0;
}
```

Write the function `my_realloc` that changes the size of a buffer previously
allocated with `malloc` while preserving all or part of the buffer content
according to the requested size. The function parameters are:
- `ptr`: buffer address
- `old_size`: current size of the buffer
- `new_size`: new size requested

The expected output is:

```shell
before realloc, array[0] = 0
before realloc, array[1] = 10
before realloc, array[2] = 20
before realloc, array[3] = 30
before realloc, array[4] = 40
after realloc, array[0] = 0
after realloc, array[1] = 10
after realloc, array[2] = 20
after realloc, array[3] = 30
after realloc, array[4] = 40
after realloc, array[5] = 50
after realloc, array[6] = 60
after realloc, array[7] = 70
after realloc, array[8] = 80
after realloc, array[9] = 90
```

!!! note "Memory copy in C"
    Memory copy is achieved with the `memcpy` function that takes 3 arguments:
    the destination address, the source address, and the number of bytes to
    copy. To use it you'll need to `#include <string.h>`. See
    [here](https://man7.org/linux/man-pages/man3/memcpy.3.html) for more info.

!!! note "Realloc"
    Although this functionality already exists in the form of the standard
    function `realloc` (see
    [here](https://man7.org/linux/man-pages/man3/realloc.3.html) -- for the
    sake of the exercize it is asked to implement it manually here.

To check the correctness of your program, use CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `malloc4.c`. In a terminal,
with that file in the local directory, check with this command:
```shell
check50 -l --log olivierpierre/comp26020-problems/master/lecture09/malloc4
```
