import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("encapsulation.cpp")
    with open("encapsulation.cpp") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("encapsulation.cpp", exe_name="encapsulation", cc="g++")

@check50.check(exists)
def validate(sources_buf):
    pass

@check50.check(compiles)
def output_correct():
    check50.run("./encapsulation")\
            .stdout("Rectangle l: 10\.0+, w: 20\.0+, perimeter: 60\.0+")\
            .stdout("Circle r: 1\.0+, circumference: 6\.280+")\
            .exit()

