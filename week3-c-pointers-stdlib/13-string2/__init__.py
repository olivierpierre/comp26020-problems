import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("string2.c")
    with open("string2.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("string2.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./string2")\
            .stdout("input a string:")\
            .stdin("and following our will and wind we may just go where no one's been")\
            .stdout("And Following Our Will And Wind We May Just Go Where No One's Been")\
            .exit()
    check50.run("./string2")\
            .stdout("input a string:")\
            .stdin("It feels like chasing shadows in the night")\
            .stdout("It Feels Like Chasing Shadows In The Night")\
            .exit()

@check50.check(compiles)
def valgrind_memcheck():
    check50.c.valgrind("./string2")\
            .stdout("input a string:")\
            .stdin("we swears, to serve the master of the precious")\
            .stdout("We Swears, To Serve The Master Of The Precious")\
            .exit()

