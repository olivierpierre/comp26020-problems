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
    if re.search("printf\(.*,\s*.*lm3.*\)", sources_buf):
        raise check50.Failure("Do not use lm3 in printf parameters")
    if re.search("printf\(.*,\s*.*lm2.*\)", sources_buf):
        raise check50.Failure("Do not use lm2 in printf parameters")

@check50.check(compiles)
def output_correct():
    check50.run("./pointer4").stdout("third member value is: 3").exit()
