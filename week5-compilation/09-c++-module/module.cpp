#include <stdio.h>

#define PAIR_MEMBER1   42
#define PAIR_MEMBER2   100

#define TRIO_MEMBER1    10
#define TRIO_MEMBER2    20
#define TRIO_MEMBER3    30

class Pair {
private:
    int _x;
    int _y;

public:
    Pair(int x, int y);
    int multiply();
    int add();
};

Pair::Pair(int x, int y) {
    _x = x;
    _y = y;
}

int Pair::multiply() {
    return _x * _y;
}

int Pair::add() {
    return _x + _y;
}

class Trio : public Pair {
private:
    int _z;

public:
    Trio(int x, int y, int z);
    int multiply();
    int add();
};

Trio::Trio(int x, int y, int z) : Pair(x, y) {
    _z = z;
}

int Trio::multiply() {
    return Pair::multiply() * _z;
}

int Trio::add() {
    return Pair::add() + _z;
}

int main(int argc, char **argv) {
    Pair p(PAIR_MEMBER1, PAIR_MEMBER2);
    Trio t(TRIO_MEMBER1, TRIO_MEMBER2, TRIO_MEMBER3);

    printf("multiply %d and %d: %d\n", PAIR_MEMBER1, PAIR_MEMBER2,
            p.multiply());
    printf("add %d and %d: %d\n", PAIR_MEMBER1, PAIR_MEMBER2, p.add());
    printf("multiply %d, %d and %d: %d\n", TRIO_MEMBER1, TRIO_MEMBER2,
            TRIO_MEMBER3, t.multiply());
    printf("add %d, %d and %d: %d\n", TRIO_MEMBER1, TRIO_MEMBER2,
            TRIO_MEMBER3, t.add());
}
