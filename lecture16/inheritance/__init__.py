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
    pass

@check50.check(compiles)
def output_correct():
    check50.run("./inheritance")\
            .stdout("v's mileage is: 20000")\
            .stdout("c1's mileage is: 10000, steering wheels: 2")\
            .stdout("c2's mileage is: 5000, steering wheels: 4")\
            .stdout("m's mileage is:  50000, cc class: 500")\
            .exit()

