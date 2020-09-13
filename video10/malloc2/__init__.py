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
    check50.run("./malloc2 5 4 3 2 1").stdout("1 2 3 4 5").exit()

    check50.run("./malloc2 546 874 18 13 87 54 4651 54 877 8 46351 87 654 657 654")\
        .stdout("8 13 18 54 54 87 87 546 654 654 657 874 877 4651 46351")\
        .exit()

    check50.run("./malloc2 546 874 18 13 87 54 4651 54 877 8 46351 87 654 657 654 546 87 45 67 6 546 85746 984 4 5646 68 47 654 654 6 87674")\
        .stdout("4 6 6 8 13 18 45 47 54 54 67 68 87 87 87 546 546 546 654 654 654 654 657 874 877 984 4651 5646 46351 85746 87674")\
        .exit()

@check50.check(compiles)
def valgrind_memcheck():
    check50.c.valgrind("./malloc2").exit()

