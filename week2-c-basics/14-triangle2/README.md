Write a C program taking an odd integer `n` as parameter and printing an isoscele
triangle on the standard output, with the triangle's base length being defined
by `n`. Example of excutions are:

```
./triangle 3
*
**
*

./triangle 5
*
**
***
**
*

./triangle 15
*
**
***
****
*****
******
*******
********
*******
******
*****
****
***
**
*
```

When the integer parameter `n` is even, the program corrects it to the next
odd number by simply incrementing it.

To check the correctness of your program, use CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `triangle2.c`. In a
terminal, with that file in the local directory, check with this command:

```shell
check50 -l --log olivierpierre/comp26020-problems/master/week2-c-basics/14-triangle2
```
