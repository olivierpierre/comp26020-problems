import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("bug.c")
    with open("bug.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("bug.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./bug")\
            .stdout("Please enter an integer between 0 and 9999:")\
            .stdin("12")\
            .stdout("array\[12\] = [0-9]+")\
            .exit()

