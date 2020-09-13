# Video 10 Problem 3

Write a C program that takes two integer as command line parameter, `x` and
`y`, and prints on the standard output `y` lines of `x` integers corresponding
to the first (`x * y`) natural integers. The numbers should be stored in a
2-dimensional array allocated with `malloc` before being printed.

```shell
# 3 rows, 4 columns
./malloc3 3 4
0 1 2 3
4 5 6 7
8 9 10 11

./malloc3 2 5
0 1 2 3 4
5 6 7 8 9

./malloc3 10 11
0 1 2 3 4 5 6 7 8 9 10
11 12 13 14 15 16 17 18 19 20 21
22 23 24 25 26 27 28 29 30 31 32
33 34 35 36 37 38 39 40 41 42 43
44 45 46 47 48 49 50 51 52 53 54
55 56 57 58 59 60 61 62 63 64 65
66 67 68 69 70 71 72 73 74 75 76
77 78 79 80 81 82 83 84 85 86 87
88 89 90 91 92 93 94 95 96 97 98
99 100 101 102 103 104 105 106 107 108 109
```

To check the correctness of your program, use CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `malloc3.c`. In a terminal,
with that file in the local directory, check with this command:
```shell
check50 -l --log olivierpierre/comp26020-problems/master/video10/malloc3
```
