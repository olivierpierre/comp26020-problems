#include <stdio.h>

#include "Employee.h"

int main(int argc, char **argv) {
    Consultant c(1234, "James", "15/01/2022", "Aerodynamics");
    Manager m(1212, "Stella", 10);
    Director d(1678, "Elon", 42);

    c.consult();
    m.take_important_decision();
    d.take_very_important_decision();
    return 0;
}
