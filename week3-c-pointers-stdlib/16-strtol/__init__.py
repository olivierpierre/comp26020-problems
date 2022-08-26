import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("strtol.c")
    with open("strtol.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("strtol.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./strtol")\
            .stdout("please enter an integer number (base 10): \n")\
            .stdin("42")\
            .stdout("you have entered: 42")\
            .exit()

