#include <stdio.h>

/* Class definition and member function implementation here */

int main(int argc, char **argv) {
    Vehicle v(20000);  // a Vehicle with mileage = 20000 miles
    Car c1(10000, 2);  // a Car with mileage = 10000 miles and 2 steering wheels
    Car c2(5000, 4);   // a Car with mileage = 5000 miles and 4 steering wheels
    Motorbike m(50000, 500); // a Motorbike with mileage = 50000 miles and class 500cc

    printf("v's mileage is: %d\n", v.get_mileage());
    printf("c1's mileage is: %d, steering wheels: %d\n", c1.get_mileage().
            c1.get_steering_wheels());
    printf("c2's mileage is: %d, steering wheels: %d\n", c2.get_mileage().
            c2.get_steering_wheels());
    printf("m's mileage is:  %d, cc class: %d\n", m.get_mileage(),
            m.get_cc_class());

    return 0;
}
