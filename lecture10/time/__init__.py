import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("time.c")
    with open("time.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("time.c", cc="gcc", std="=gnu99")

@check50.check(compiles)
def output_correct():
    check50.run("./time 3")\
            .stdout("sleep duration: 3.[0-9]+")\
            .exit()
    check50.run("./time 5")\
            .stdout("sleep duration: 5.[0-9]+")\
            .exit()

