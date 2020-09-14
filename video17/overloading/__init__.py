import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("overloading.cpp")
    with open("overloading.cpp") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("overloading.cpp", exe_name="overloading", cc="g++")

@check50.check(exists)
def validate(sources_buf):
    pass

@check50.check(compiles)
def output_correct():
    check50.run("./overloading")\
        .stdout("(4+5i) + (9+11i) = (13+16i)", regex=False)\
        .stdout("4 \+ 9 = 13")\
        .stdout("5.800000 \+ 11.200000 = 17.000000")\
        .exit()

