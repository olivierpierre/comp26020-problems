The program [module.cpp](module.cpp) contains two classes managing pairs and
trios of integers and the multiply/addition operations that can be performed
on these. The goal of the exercise is to break down `module.cpp` into several
files:

- `Pair.h` and `Pair.cpp` managing the pair class
- `Trio.h` and `Trio.cpp` managing the trio class
- `main.cpp` containing the rest of the program

The expected output is:
```shell
./module
multiply 42 and 100: 4200
add 42 and 100: 142
multiply 10, 20 and 30: 6000
add 10, 20 and 30: 60
```

To check the correctness of your program, use the department VM image with check50 installed or alternatively CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io). In a terminal, with all the mentioned source files in
the local directory, check with this command:
```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2021-2022/week5-compilation/06-c++-module
```
