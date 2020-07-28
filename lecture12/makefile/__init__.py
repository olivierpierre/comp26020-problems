import check50
import check50.c
import re
import os.path

@check50.check()
def exists():
    check50.exists("main.c")
    check50.exists("module1.c")
    check50.exists("module2.c")
    check50.exists("module1.h")
    check50.exists("module2.h")
    check50.exists("Makefile")
    with open("Makefile") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def validate(sources_buf):
    pass

@check50.check(exists)
def output_correct():
    check50.run("make").exit()
    check50.exists("main.o")
    check50.exists("module1.o")
    check50.exists("module2.o")
    check50.exists("prog")

    check50.run("make")\
            .stdout("make: Nothing to be done for .*")\
            .exit()

    check50.run("touch module1.c && make")\
            .stdout(".*module1.*")\
            .stdout(".*module1.*")\
            .exit()

    check50.run("make clean")\
            .exit()
    if os.path.exists("prog"):
        raise check50.Failure("Bad make clean rule")
