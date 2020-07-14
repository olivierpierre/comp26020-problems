import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("preprocessor.c")
    check50.exists("preprocessor.h")
    with open("preprocessor.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("preprocessor.c", cc="gcc", std="gnu99")

@check50.check(exists)
def validate(sources_buf):
    if '\#include\s+\"preprocessor\.h\"' not in sources_buf:
        raise check50.Failure("preprocessor.h not included in preprocessor.c")

@check50.check(compiles)
def output_correct():
    check50.run("./preprocessor")\
            .stdout("Please enter the amount of random number to generate:")\
            .stdin("10000000")\
            .stdout("Generated 10000000 numbers in [0-9]+\.[0-9]+ seconds")\
            .exit()

