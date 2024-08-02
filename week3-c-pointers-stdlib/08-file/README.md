Write a C program taking as command line parameter A) a file name `f` and B) a word `w`.
The program then creates the file `f-processed` which is a copy of `f` where all occurrences of the word `w` have been deleted.
Here is an example of execution:

```shell
cat sample-file-1
hello world
this is a test file containing the word hello several times
some lines do not contain that word
while others do: hello

./file sample-file-1 hello

cat sample-file-1-processed
 world
this is a test file containing the word  several times
some lines do not contain that word
while others do: 
```

You download `sample-file-1` [here](./comp26020-problems/week3-c-pointers-stdlib/08-file/sample-file-1).

To check the correctness of your program, use a [Linux distribution with check50 installed](https://github.com/olivierpierre/comp26020-devcontainer) and write your solution in a file named `file.c`.
In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week3-c-pointers-stdlib/08-file
```
Make sure that `sample-file-1` is in the current directory alongside `file.c`
