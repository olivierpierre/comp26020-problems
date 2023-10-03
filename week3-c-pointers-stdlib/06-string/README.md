Write a C program reading two strings from the standard input using `fgets`,
and indicating if the strings are similar or not. Output examples:

```shell
./string
input string1:
test
input string2:
test
strings are similar

./string
input string1:
hello world!
input string2:
goodbye
strings are different
```

To check the correctness of your program, use a
[Linux distribution with check50 installed](https://github.com/olivierpierre/comp26020-devcontainer)
and write your solution in a file named `string.c`. In a
terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2023-2024/week3-c-pointers-stdlib/11-string
```
