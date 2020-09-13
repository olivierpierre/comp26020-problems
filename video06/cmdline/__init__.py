import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("cmdline.c")
    with open("cmdline.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("cmdline.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./cmdline 1.0 2.0 3.0").stdout("6.000000").exit()
    check50.run("./cmdline 1.45 2.78 3.25").stdout("13.100750").exit()
    check50.run("./cmdline 15.5 56.89 32.225").stdout("28415.843875").exit()
    check50.run("./cmdline 5.45 6.9 325.225").stdout("12230.086125").exit()
