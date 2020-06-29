# Lecture 5 Problem 5

Write a C program taking an integer as parameter and printing a right-angled
triangle on the command line which legs size is defined by the integer
parameter. Here are some examples of execution:

```
./triangle 2
*
**

./triangle 5
*
**
***
****
*****

./triangle 15
*
**
***
****
*****
******
*******
********
*********
**********
***********
************
*************
**************
***************
```

To check the correctness of your program, use CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `triangle.c`. In a
terminal, with that file in the local directory, check with this command:

```shell
check50 -l --log olivierpierre/comp26020-problems/master/lecture05/triangle
```
