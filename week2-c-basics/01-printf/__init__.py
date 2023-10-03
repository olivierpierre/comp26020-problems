import check50
import check50.c

@check50.check()
def exists():
    check50.exists("printf.c")

@check50.check(exists)
def compiles():
    check50.c.compile("printf.c", cc="gcc")

@check50.check(compiles)
def large_c_printed():
    check50.run("./printf").stdout("    ######\n  ##      ##\n #\n #\n #\n #\n #\n  ##      ##\n    ######\n").exit()
