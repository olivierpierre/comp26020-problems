Write a C program taking an integer as parameter and printing a right-angled triangle on the command line which legs size is defined by the integer parameter.
Here are some examples of execution:

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

To check the correctness of your program, use a use a [Linux distribution](https://github.com/olivierpierre/comp26020-devcontainer) with [check50 installed](exercise-set-1.html#installing-check50) and write your solution in a file named **`triangle.c`**.
In a terminal, with that file in the local directory, check with this command:


```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week2-c-basics/15-triangle
```
