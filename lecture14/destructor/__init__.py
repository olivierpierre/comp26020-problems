import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("destructor.cpp")
    with open("destructor.cpp") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("destructor.cpp", exe_name="destructor", cc="g++")

@check50.check(compiles)
def valgrind_memcheck():
    check50.c.valgrind("./destructor").exit()

@check50.check(compiles)
def output_correct():
    check50.run("./destructor")\
            .stdout("Toplevel val: 30, with pair:")\
            .stdout("Pair x: 10, y: 20")\
            .exit()

