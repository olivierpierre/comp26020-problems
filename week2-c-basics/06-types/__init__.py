import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("types.c")
    with open("types.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("types.c", cc="gcc")

@check50.check(exists)
def check_type(sources_buf):
    re1 = "^\s*unsigned\s+(int\s+)?variable"

    if not re.search(re1, sources_buf):
        print(sources_buf)
        raise check50.Failure("Could not find a declaration with the correct "
                "type")

@check50.check(compiles)
def output_correct():
    check50.run("./types").stdout("10").exit()
