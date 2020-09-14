#include <stdio.h>

#include "Employee.h"

int main(int argc, char **argv) {
    Consultant c(1234, "James", "15/01/2022", "Aerodynamics");
    Manager m(1212, "Stella", 10);
    Director d(1678, "Elon", 42);

    // Should print "[1234 - James] I'm consulting on Aerodynamics until 15/01/2022":
    c.consult();

    // Should print "[1212 - Stella] I'm taking an important decision in office 10"
    m.take_important_decision();

    // Should print "[1678 - Elon] I'm taking an very important decision in office 42"
    d.take_very_important_decision();
    return 0;
}
