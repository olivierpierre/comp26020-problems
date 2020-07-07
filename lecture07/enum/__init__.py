import check50
import check50.c
import re

re1 = "enum\s*{\s*JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER\s*}.*;"

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

@check50.check(compiles)
def output_correct():
    check50.run("./enum").stdout("JANUARY")\
            .stdout("FEBRUARY")\
            .stdout("MARCH")\
            .stdout("APRIL")\
            .stdout("MAY")\
            .stdout("JUNE")\
            .stdout("JULY")\
            .stdout("AUGUST")\
            .stdout("SPETEMBER")\
            .stdout("OCTOBER")\
            .stdout("NOVERMBER")\
            .stdout("DECEMBER")\
            .exit()
