import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("array.c")
    with open("array.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("array.c", cc="gcc")

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
    for_re = "for\s*\(.*;.*;.*\)"
    while_re = "while\s*\(.*\)"
    if not re.search(for_re, sources_buf) and not re.search(while_re, sources_buf):
        raise check50.Failure("Did not found a for/while loop in sources")

@check50.check(compiles)
def output_correct():
    check50.run("./array 6 5 4 3 2 1").stdout("1 2 3 4 5 6").exit()
    check50.run("./array 5 5 120").stdout("5 5 120").exit()
    check50.run("./array 4654 87987 16515 4987 465416 4984 4654 498498 "
            "16516 897484")\
                    .stdout("4654 4654 4984 4987 16515 16516 87987 465416 "
                            "498498 897484").exit()
