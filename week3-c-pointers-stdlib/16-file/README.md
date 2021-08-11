Write a C program taking as command line parameter A) a file name `f` and B) a
word `w`. The program then creates the file `f-processed` which is a copy of
`f` where all occurences of the word `w` have been deleted. Here is an example
of execution:

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

You can create `sample-file-1` with the following content:
```shell
hello world
this is a test file containing the word hello several times
some lines do not contain that word
while others do: hello
```

To check the correctness of your program, use the department VM image with check50 installed or alternatively CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `file.c`. In a terminal,
with that file in the local directory, check with this command:
```shell
check50 -l --log olivierpierre/comp26020-problems/2020-2021/week3-c-pointers-stdlib/16-file
```
Make sure that `sample-file-1` is in the current directory alongside `file.c`
