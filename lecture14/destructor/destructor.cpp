#include <stdio.h>

class Pair {
private:
    int x;
    int y;
public:
    Pair(int x, int y);
    void print();
};

Pair::Pair(int x, int y) {
    this->x = x;
    this->y = y;
}

void Pair::print() {
    printf("Pair x: %d, y: %d\n", x, y);
}

class TopLevel {
private:
    Pair *p;
    int val;
public:
    TopLevel(int x, int y, int val);
    void print();
};

TopLevel::TopLevel(int x, int y, int val) {
    this->val = val;
    this->p = new Pair(x, y);
}

void TopLevel::print() {
    printf("Toplevel val: %d, with pair:\n", val);
    p->print();
}

int main(int argc, char **argv) {
    TopLevel t(10, 20, 30);
    t.print();
    return 0;
}
