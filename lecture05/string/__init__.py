import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("string.c")
    with open("string.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("string.c", cc="gcc")

@check50.check(exists)
def has_right_size(sources_buf):
    string_re = "char\s+string\[([0-9]+)\];"
    res = re.search(string_re, sources_buf)

    if not res:
        raise check50.Failure("Cannot determine the string size")

    size = int(res.groups[0])
    if size < 9:
        raise check50.Failure("String size not large enough")

@check50.check(exists)
def has_termination_chracter():
    string_re = "string\[9\]\s*=\s*'\\0'"
    if not re.search(string_re, sources_buf):
        raise check50.failure("Cannot find string termination character")

@check50.check(compiles)
def output_correct():
    check50.run("./string").stdout("hi there").exit()
