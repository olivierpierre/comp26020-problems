import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("pointer.c")
    with open("pointer.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("pointer.c", cc="gcc")

@check50.check(exists)
def function_call(sources_buf):
    if not re.search("add\s*\(.*\*.*,.*\*.*\)", sources_buf):
        raise check50.Failure("The add function does not seem to be defined"
                "with pointer parameters")

@check50.check(compiles)
def output_correct():
    check50.run("./pointer 10 20").stdout("10 \+ 20 = 30").exit()
    check50.run("./pointer 114324 412443").stdout("114324 \+ 412443 = 526767").exit()
    check50.run("./pointer -46546 6544").stdout("-46546 \+ 6544 = -40002").exit()
