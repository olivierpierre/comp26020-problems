import check50
import check50.c
import re

re1 = "struct\s+timestamp\s*{\s*unsigned int hour;\s*unsigned int minute;\s*unsigned int second;\s*};"
re2 = "typedef\s+struct\s+.+\s*{\s*unsigned int hour;\s*unsigned int minute;\s*unsigned int second;\s*}\s*.+;"

@check50.check()
def exists():
    check50.exists("struct.c")
    with open("struct.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("struct.c", cc="gcc")

@check50.check(exists)
def has_struct(sources_buf):
    if not re.search(re1, sources_buf, re.DOTALL | re.MULTILINE) and \
            not re.search(re2, sources_buf, re.DOTALL | re.MULTILINE):
        raise check50.Failure("Can't find usage of the timestamp struct")

@check50.check(exists)
def has_function(sources_buf):
    if not re.search("add_timestamps\(.*\)", sources_buf,
            re.DOTALL | re.MULTILINE):
        raise check50.Failure("Can't find the add_timestamps function")

@check50.check(compiles)
def output_correct():
    check50.run("./struct 14 12 5 22 5 0").stdout("36 17 5").exit()
    check50.run("./struct 10 30 50 1 5 15").stdout("11 36 05").exit()
    check50.run("./struct 5 11 44 12 30 3").stdout("17 41 47").exit()
    check50.run("./struct 51 8 4 15 2 31").stdout("66 10 35").exit()
    check50.run("./struct 0 0 0 0 0 0").stdout("0 0 0").exit()
