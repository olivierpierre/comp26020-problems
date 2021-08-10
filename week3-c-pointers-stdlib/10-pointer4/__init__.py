import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("pointer4.c")
    with open("pointer4.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("pointer4.c", cc="gcc")

@check50.check(exists)
def validate(sources_buf):
    if "]" in sources_buf or "[" in sources_buf:
        raise check50.Failure("There should be no '[' or ']' in the sources")
    if "%s" in sources_buf:
        raise check50.Failure("There should be no '%s' in the sources")

@check50.check(compiles)
def output_correct():
    check50.run("./pointer4").stdout("hello, world!").exit()
