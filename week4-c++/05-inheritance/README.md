The program [inheritance.cpp](inheritance.cpp) creates a few objects from classes `Vehicle`,
`Car` and `Motorbike`:
```cxx
#include <stdio.h>

/* Class definition and member function implementation here */

int main(int argc, char **argv) {
    Vehicle v(20000);  // a Vehicle with mileage = 20000 miles
    Car c1(10000, 2);  // a Car with mileage = 10000 miles and 2 steering wheels
    Car c2(5000, 4);   // a Car with mileage = 5000 miles and 4 steering wheels
    Motorbike m(50000, 500); // a Motorbike with mileage = 50000 miles and class 500cc

    printf("v's mileage is: %d\n", v.get_mileage());
    printf("c1's mileage is: %d, steering wheels: %d\n", c1.get_mileage(),
            c1.get_steering_wheels());
    printf("c2's mileage is: %d, steering wheels: %d\n", c2.get_mileage(),
            c2.get_steering_wheels());
    printf("m's mileage is:  %d, cc class: %d\n", m.get_mileage(),
            m.get_cc_class());

    return 0;
}
```

Edit the file to include the definition of the classes as well as the
implementation of constructors and relevant member functions knowing that:

- `Vehicle` has a member variable `_mileage`
- `Car` inheritates from `Vehicle` and has a member variable `_steering_wheels`
- `Motorbike` inheritates from `Vehicle` and has a member variable `_cc_class`

Expected output:
```shell
./inheritance
v's mileage is: 20000
c1's mileage is: 10000, steering wheels: 2
c2's mileage is: 5000, steering wheels: 4
m's mileage is:  50000, cc class: 500
```

To check the correctness of your program, use the department VM image with check50 installed or alternatively CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `inheritance.cpp`. In a
terminal, with that file in the local directory, check with this command:
```shell
check50 -l --log olivierpierre/comp26020-problems/2020-2021/week4-c++/05-inheritance
```
