Write a C program taking an integer `n` as command line parameter, allocating an array of integer of size `n`, and filling that array with random integers -- each between 0 and 100.
Next, a second array of size `n` is created and the content of the first array is copied into the second one with a single call to `memcpy`.
Finally, both arrays are printed.
Example output:

```shell
./memcpy 10
array1: 32 32 54 12 52 56 8 30 44 94
array2: 32 32 54 12 52 56 8 30 44 94

./memcpy 15
array1: 32 32 54 12 52 56 8 30 44 94 44 39 65 19 51
array2: 32 32 54 12 52 56 8 30 44 94 44 39 65 19 51
```

> **Random Numbers.**
> See the `rand` function: [https://linux.die.net/man/3/rand](https://linux.die.net/man/3/rand).
> For example to get a random integer between 0 and 9 (included): `int random_int = rand()%10`.

To check the correctness of your program, use a [Linux distribution with check50 installed](https://github.com/olivierpierre/comp26020-devcontainer) and write your solution in a file named `memcpy.c`.
In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week3-c-pointers-stdlib/14-memcpy
```