import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("string2.c")
    with open("string2.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("string2.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./string2")\
            .stdout("input string1:")\
            .stdin("test")\
            .stdout("input string2:")\
            .stdin("test")\
            .stdout("strings are similar")\
            .exit()
    check50.run("./string2")\
            .stdout("input string1:")\
            .stdin("testtest")\
            .stdout("input string2:")\
            .stdin("test")\
            .stdout("strings are different")\
            .exit()

@check50.check(compiles)
def valgrind_memcheck():
    check50.c.valgrind("./string2")\
            .stdout("input string1:")\
            .stdin("abcd")\
            .stdout("input string2:")\
            .stdin("efgh")\
            .stdout("strings are different")\
            .exit()

