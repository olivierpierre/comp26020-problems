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
    re1 = "long\s+long\s+(signed\s+)?(int\s+)?variable"
    re2 = "(signed\s+)?long\s+long\s+(int\s+)?variable"
    re3 = "long\s+long\s+(unsigned\s+)?(int\s+)?variable"
    re4 = "(unsigned\s+)?long\s+long\s+(int\s+)?variable"

    if re.search(re3, sources_buf) or re.search(re4, sources_buf):
        raise check50.Failure("Could not find a declaration with the correct "
                "type")

    if not re.search(re1, sources_buf) and not re.search(re2, sources_buf):
        raise check50.Failure("Could not find a declaration with the correct "
                "type")

@check50.check(compiles)
def output_correct():
    check50.run("./types").stdout("-725230241886380040").exit()
