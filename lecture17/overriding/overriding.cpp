#include <stdio.h>
#include <stdlib.h>
#include <vector>

using namespace std;

class Vehicle {
public:
    virtual int get_number_of_wheels() = 0;
};

class Car : public Vehicle {
    /* ... */
};

class Bike : public Vehicle {
    /* ... */
};

int number_of_wheels(Vehicle *v) {
    return v->get_number_of_wheels();
}

int main(int argc, char **argv) {
    vector<Vehicle *> array;

    for(int i=0; i<10; i++) {
        if(rand() % 2)
            array.push_back(new Car());
        else
            array.push_back(new Bike());
    }

    for(int i=0; i<10; i++) {
        printf("array[%d] has %d wheels\n", i, get_number_of_wheels(array[i]));
        delete array[i];
    }

    return 0;
}
