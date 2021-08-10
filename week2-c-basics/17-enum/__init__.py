import check50
import check50.c
import re

re1 = "enum\s*{\s*MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY|\s*}.*;"
re2 = "enum\s+day\s+d"
re3 = "\n\s*case\s+__DAY__\s*:"

@check50.check()
def exists():
    check50.exists("enum.c")
    with open("enum.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("enum.c", cc="gcc")

@check50.check(exists)
def has_enum(sources_buf):
    if not re.search(re1, sources_buf, re.DOTALL | re.MULTILINE):
        raise check50.Failure("Can't find the enum definition")

@check50.check(exists)
def declare_enum_var(sources_buf):
    if not re.search(re2, sources_buf):
        raise check50.Failure("Can't find a variable declared with the enum type")

@check50.check(exists)
def cases_enum(sources_buf):
    if not re.search(re3, sources_buf):
        raise check50.Failure("Can't find usage of the enum value in case statements")

@check50.check(compiles)
def output_correct():
    check50.run("./enum").stdout("Today is: Wednesday")\
            .exit()
