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
    for_re = "for\s*\(.*;.*;.*\)"
    while_re = "while\s*\(.*\)"
    if not re.search(for_re, sources_buf) and not re.search(while_re, sources_buf):
        raise check50.Failure("Did not found a for loop in sources")

@check50.check(compiles)
def output_correct():
    check50.run("./array2 1 2 3 4 5 6")\
            .stdout("1 is odd")\
            .stdout("2 is even")\
            .stdout("3 is odd")\
            .stdout("4 is even")\
            .stdout("5 is odd")\
            .stdout("6 is even")\
            .exit()
    check50.run("./array2 5 5 120")\
            .stdout("5 is odd")\
            .stdout("5 is odd")\
            .stdout("120 is even")\
            .exit()
    check50.run("./array2 11654 16544 78789 516 7879 4658 546 54687 787 88")\
            .stdout("11654 is even")\
            .stdout("16544 is even")\
            .stdout("78789 is odd")\
            .stdout("516 is even")\
            .stdout("7879 is odd")\
            .stdout("4658 is even")\
            .stdout("546 is even")\
            .stdout("54687 is odd")\
            .stdout("787 is odd")\
            .stdout("88 is even")\
            .exit()
    check50.run("./array2").stdout("").exit()
