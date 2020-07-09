import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("malloc.c")
    with open("malloc.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("malloc.c", cc="gcc")

@check50.check(exists)
def validate(sources_buf):
    if not re.search("[a-zA-Z1-9_]+\s*=\s*malloc\(.*sizeof.*\)", sources_buf):
        raise check50.Failure("Cant find call to malloc or sizeof")
    if not re.search("free\(.*\)", sources_buf):
        raise check50.Failure("Cant find call to free")

@check50.check(compiles)
def output_correct():
    check50.run("./malloc")\
            .stdout("0")\
            .stdout("1")\
            .stdout("2")\
            .stdout("3")\
            .stdout("4")\
            .stdout("5")\
            .stdout("6")\
            .stdout("7")\
            .stdout("8")\
            .stdout("9")\
            .exit()

@check50.check(compiles)
def valgrind_memcheck():
    check50.c.valgrind("./malloc").exit()

