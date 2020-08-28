import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("inheritance.cpp")
    with open("inheritance.cpp") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("inheritance.cpp", exe_name="inheritance", cc="g++")

@check50.check(exists)
def validate(sources_buf):
    if not re.search("class\s+Vehicle" in sources_buf):
        raise check50.Failure("Could not find class Vehicle")
    if not re.search("class\s+Car\s+:\s+public\s+Vehicle" in sources_buf):
        raise check50.Failure("Could not find class Car or class Car does not "\
                "inheritates from a parent")
    if not re.search("class\s+Motorbike\s+:\s+public\s+Vehicle" in sources_buf):
        raise check50.Failure("Could not find class Motorbike or class "\
                "Motorbike does not inheritates from a parent")

@check50.check(compiles)
def output_correct():
    check50.run("./inheritance")\
            .stdout("v's mileage is: 20000")\
            .stdout("c1's mileage is: 10000, steering wheels: 2")\
            .stdout("c2's mileage is: 5000, steering wheels: 4")\
            .stdout("m's mileage is:  50000, cc class: 500")\
            .exit()

