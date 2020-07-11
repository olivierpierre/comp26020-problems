import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("math.c")
    with open("math.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("math.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./math")\
            .stdout("Input a number:")\
            .stdin("12.4")\
            .stdout("Input 0 for ceil, 1 for floor")\
            .stdin("0")\
            .stdout("13.000000")\
            .exit()
    check50.run("./math")\
            .stdout("Input a number:")\
            .stdin("442.8")\
            .stdout("Input 0 for ceil, 1 for floor")\
            .stdin("1")\
            .stdout("422.000000")\
            .exit()

