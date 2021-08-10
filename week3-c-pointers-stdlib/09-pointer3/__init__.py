import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("pointer3.c")
    with open("pointer3.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("pointer3.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./pointer3 5")\
            .stdout("Variable contains 5 and is located @0x[0-9a-f]+",
                    regex=True)\
            .exit()
    check50.run("./pointer3 156")\
            .stdout("Variable contains 156 and is located @0x[0-9a-f]+",
                    regex=True)\
            .exit()
    check50.run("./pointer3 42")\
            .stdout("Variable contains 42 and is located @0x[0-9a-f]+",
                    regex=True)\
            .exit()
