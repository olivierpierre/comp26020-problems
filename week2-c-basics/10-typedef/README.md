The program below prints the dimensions of a rectangle passed from the command
line arguments:

```c
#include <stdio.h>
#include <stdlib.h>

struct s_rectangle {
    unsigned long long int width;
    unsigned long long int length;
};

void print_rectangle(struct s_rectangle r) {
    printf("Rectangle is %llu x %llu\n", r.width, r.length);
}

int main(int argc, char **argv) {
    struct s_rectangle r;
    unsigned long long int width;
    unsigned long long int length;

    if(argc == 3) {
        width = atoll(argv[1]);
        length = atoll(argv[2]);

        r.width = width;
        r.length = length;

        print_rectangle(r);
    }

    return 0;
}
```

Modify this program to use `typedef` to alias:

- `struct s_rectangle` into `rectangle`
- `unsigned long long int` into `ull`

To check the correctness of your program, use a
[Linux distribution with check50 installed](https://github.com/olivierpierre/comp26020-devcontainer)
and write your solution in a file named `typedef.c`. In a
terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/2023-2024/week2-c-basics/10-typedef
```
