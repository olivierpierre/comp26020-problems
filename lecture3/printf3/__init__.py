import check50
import check50.c

@check50.check()
def exists():
    check50.exists("printf3.c")

@check50.check(exists)
def compiles():
    check50.c.compile("printf3.c", cc="gcc")

@check50.check(compiles)
def large_c_printed():
    check50.run("./printf3").stdout("    ######\n").stdout("  ##      ##\n").stdout(" #\n").stdout(" #\n").stdout(" #\n").stdout(" #\n").stdout(" #\n").stdout("  ##      ##\n").stdout("    ######\n").exit()
