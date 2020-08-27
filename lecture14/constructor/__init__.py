import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("constructor.cpp")
    with open("constructor.cpp") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("constructor.cpp", cc="g++")

@check50.check(exists)
def validate(sources_buf):
    pass

@check50.check(compiles)
def output_correct():
    check50.run("./constructor")\
            .stdout("p.x is 10, p.y is 20")\
            .exit()

