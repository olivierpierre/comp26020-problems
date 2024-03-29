import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("malloc2.c")
    with open("malloc2.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("malloc2.c", cc="gcc")

@check50.check(exists)
def validate(sources_buf):
    if "malloc" not in sources_buf:
        raise check50.Failure("Cannot find call to malloc")
    if "free" not in sources_buf:
        raise check50.Failure("Cannot find a call to free")

@check50.check(compiles)
def output_correct():
    check50.run("./malloc2 3 5")\
        .stdout("0 1 2 3 4")\
        .stdout("5 6 7 8 9")\
        .stdout("10 11 12 13 14")\
        .exit()

    check50.run("./malloc2 4 4")\
        .stdout("0 1 2 3")\
        .stdout("4 5 6 7")\
        .stdout("8 9 10 11")\
        .stdout("12 13 14 15")\
        .exit()

    check50.run("./malloc2 5 10")\
        .stdout("0 1 2 3 4 5 6 7 8 9")\
        .stdout("10 11 12 13 14 15 16 17 18 19")\
        .stdout("20 21 22 23 24 25 26 27 28 29")\
        .stdout("30 31 32 33 34 35 36 37 38 39")\
        .stdout("40 41 42 43 44 45 46 47 48 49")\
        .exit()

@check50.check(compiles)
def valgrind_memcheck():
    check50.c.valgrind("./malloc2").exit()

