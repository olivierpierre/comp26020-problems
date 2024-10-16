Write a C program taking a year as command line parameter and printing out on the standard output if this year is leap or not.

To determine if a year is leap, you can use the following algorithm (taken from [Wikipedia](https://en.wikipedia.org/wiki/Leap_year#Algorithm)):

```
if (year is not divisible by 4) then (it is a common year)
else if (year is not divisible by 100) then (it is a leap year)
else if (year is not divisible by 400) then (it is a common year)
else (it is a leap year)
```

The output format should be as described in these examples:
```bash
./leap 2000
2000 is a leap year
./leap 2100
2100 is not a leap year
```

To check the correctness of your program, use a use a [Linux distribution](https://github.com/olivierpierre/comp26020-devcontainer) with [check50 installed](exercise-set-1.html#installing-check50) and write your solution in a file named **`leap.c`**.
In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2024-2025/week2-c-basics/08-leap
```