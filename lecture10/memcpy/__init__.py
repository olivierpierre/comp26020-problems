import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("memcpy.c")
    with open("memcpy.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("memcpy.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./memcpy 10")\
            .stdout("array1:( [0-9]+){10}", regex=True)\
            .stdout("array2:( [0-9]+){10}", regex=True)\
            .exit()
    check50.run("./memcpy 20")\
            .stdout("array1:( [0-9]+){20}", regex=True)\
            .stdout("array2:( [0-9]+){20}", regex=True)\
            .exit()

@check50.check(compiles)
def valgrind_memcheck():
    check50.c.valgrind("./memcpy 20")\
            .stdout("array1:( [0-9]+){20}", regex=True)\
            .stdout("array2:( [0-9]+){20}", regex=True)\
            .exit()

