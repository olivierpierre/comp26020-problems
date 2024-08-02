Write a C program taking an odd integer `n` as parameter and printing an isosceles triangle on the standard output, with the triangle's base length being defined by `n`.
Example of execution are:

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

When the integer parameter `n` is even, the program corrects it to the next odd number by simply incrementing it.

To check the correctness of your program, use a [Linux distribution with check50 installed](https://github.com/olivierpierre/comp26020-devcontainer) and write your solution in a file named **`triangle2.c`**.
In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week2-c-basics/16-triangle2
```