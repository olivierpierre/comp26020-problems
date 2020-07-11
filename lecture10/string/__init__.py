import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("string.c")
    with open("string.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("string.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./string")\
            .stdout("input a string:")\
            .stdin("test")\
            .stdout("you entered: test")\
            .exit()

@check50.check(compiles)
def valgrind_memcheck():
    check50.c.valgrind("./string").exit()

