
Write a C program reading a string from the standard input and capitalise the first letter of each word.

```shell
./string2
input a string:
we swears, to serve the master of the precious
We Swears, To Serve The Master Of The Precious

./string2
input a string:
and following our will and wind we may just go where no one's been
And Following Our Will And Wind We May Just Go Where No One's Been
```

> **Capitalising letters.**
> See the `toupper` function: [https://linux.die.net/man/3/toupper](https://linux.die.net/man/3/toupper)

To check the correctness of your program, use a [Linux distribution with check50 installed](https://github.com/olivierpierre/comp26020-devcontainer) and write your solution in a file named `string2.c`.
In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week3-c-pointers-stdlib/13-string2
```