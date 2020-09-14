import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("leap.c")
    with open("leap.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("leap.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./leap 1994").stdout("1994 is not a leap year").exit()
    check50.run("./leap 0").stdout("0 is a leap year").exit()
    check50.run("./leap 2000").stdout("2000 is a leap year").exit()
    check50.run("./leap 2100").stdout("2100 is not a leap year").exit()
    check50.run("./leap 2300").stdout("2300 is not a leap year").exit()
    check50.run("./leap 1715").stdout("1715 is not a leap year").exit()
    check50.run("./leap 1716").stdout("1716 is a leap year").exit()

