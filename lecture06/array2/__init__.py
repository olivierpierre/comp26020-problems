import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("array2.c")
    with open("array2.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("array2.c", cc="gcc")

@check50.check(exists)
def has_atoi(sources_buf):
    if "atoi" not in sources_buf:
        raise check50.Failure("Found no call to the string to int conversion "
                "function")

@check50.check(exists)
def has_array(sources_buf):
    if "array[" not in sources_buf:
        raise check50.Failure("Did not found array[] in sources")

@check50.check(exists)
def has_for_loop(sources_buf):
    for_re = "for\(.*;.*;.*\)"
    while_re = "wile\(.*\)"
    if not re.search(for_re, sources_buf) and not re.search(while_re, sources_buf):
        raise check50.Failure("Did not found a for/while loop in sources")

@check50.check(compiles)
def output_correct():
    check50.run("./array2 6 5 4 3 2 1").stdout("1 2 3 4 5 6").exit()
