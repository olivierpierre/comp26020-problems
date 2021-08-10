import check50
import check50.c

@check50.check()
def exists():
    check50.exists("compilation-errors.c")

@check50.check(exists)
def compiles():
    check50.c.compile("compilation-errors.c", cc="gcc")

@check50.check(compiles)
def correct_output():
    check50.run("./compilation-errors").stdout("This should work!").exit()
