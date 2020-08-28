# Lecture 15 Problem 1

The program [constructor.cpp](constructor.cpp) defines a class `Pair` with
2 variable members:

```cxx
#include <stdio.h>

class Pair {
public:
    int x;
    int y;
};

int main(int argc, char **argv) {
    Pair p;

    p.x = 10;
    p.y = 20;

    printf("p.x is %d, p.y is %d\n", p.x, p.y);

    return 0;
}
```

Rewrite the class Pair definition to use a constructor rather than the manual
and per-member initialization done in the main function. The expected output
should be:

```sh
./constructor
p.x is 10, p.y is 20
```

To check the correctness of your program, use CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `constructor.cpp`. In a
terminal, with that file in the local directory, check with this command:
```shell
check50 -l --log olivierpierre/comp26020-problems/master/lecture15/constructor
```
