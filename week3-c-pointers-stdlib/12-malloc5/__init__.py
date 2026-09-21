import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("malloc5.c")
    with open("malloc5.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("malloc5.c", cc="gcc")

@check50.check(exists)
def validate(sources_buf):
    if "malloc" not in sources_buf:
        raise check50.Failure("Cannot find call to malloc")
    if "free" not in sources_buf:
        raise check50.Failure("Cannot find a call to free")

@check50.check(compiles)
def output_correct():
    check50.run("./malloc5")\
        .stdout(r"before realloc, array\[0\] \= 0")\
        .stdout(r"before realloc, array\[1\] \= 10")\
        .stdout(r"before realloc, array\[2\] \= 20")\
        .stdout(r"before realloc, array\[3\] \= 30")\
        .stdout(r"before realloc, array\[4\] \= 40")\
        .stdout(r"after realloc, array\[0\] \= 0")\
        .stdout(r"after realloc, array\[1\] \= 10")\
        .stdout(r"after realloc, array\[2\] \= 20")\
        .stdout(r"after realloc, array\[3\] \= 30")\
        .stdout(r"after realloc, array\[4\] \= 40")\
        .stdout(r"after realloc, array\[5\] \= 50")\
        .stdout(r"after realloc, array\[6\] \= 60")\
        .stdout(r"after realloc, array\[7\] \= 70")\
        .stdout(r"after realloc, array\[8\] \= 80")\
        .stdout(r"after realloc, array\[9\] \= 90")\
        .exit()

@check50.check(compiles)
def valgrind_memcheck():
    check50.c.valgrind("./malloc5").exit()

