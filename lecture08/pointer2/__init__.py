import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("pointer2.c")
    with open("pointer2.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("pointer2.c", cc="gcc")

@check50.check(exists)
def function_call(sources_buf):
    if not re.search("add\s*\(.*\*.*,.*\*.*\)", sources_buf):
        raise check50.Failure("The add function does not seem to be defined"
                "with pointer parameters")

@check50.check(compiles)
def output_correct():
    check50.run("./pointer2 10 20").stdout("10 \+ 20 = 30").exit()
