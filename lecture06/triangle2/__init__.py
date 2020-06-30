import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("triangle2.c")
    with open("triangle2.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("triangle2.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./triangle2 0").stdout("").exit()
    check50.run("./triangle2 1").stdout("\*").exit()
    check50.run("./triangle2 3")\
            .stdout("\*")\
            .stdout("\*\*")\
            .stdout("\*")\
            .exit()
    check50.run("./triangle2 2")\
            .stdout("\*")\
            .stdout("\*\*")\
            .stdout("\*")\
            .exit()
    check50.run("./triangle2 5")\
            .stdout("\*")\
            .stdout("\*\*")\
            .stdout("\*\*\*")\
            .stdout("\*\*")\
            .stdout("\*")\
            .exit()
    check50.run("./triangle2 15")\
            .stdout("\*")\
            .stdout("\*\*")\
            .stdout("\*\*\*")\
            .stdout("\*\*\*\*")\
            .stdout("\*\*\*\*\*")\
            .stdout("\*\*\*\*\*\*")\
            .stdout("\*\*\*\*\*\*\*")\
            .stdout("\*\*\*\*\*\*\*\*")\
            .stdout("\*\*\*\*\*\*\*")\
            .stdout("\*\*\*\*\*\*")\
            .stdout("\*\*\*\*\*")\
            .stdout("\*\*\*\*")\
            .stdout("\*\*\*")\
            .stdout("\*\*")\
            .stdout("\*")\
            .exit()

