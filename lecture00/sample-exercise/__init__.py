import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("sample-exercise.c")
    with open("sample-exercise.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("sample-exercise.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./sample-exercise").stdout("").exit()
