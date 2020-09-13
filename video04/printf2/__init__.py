import check50
import check50.c

@check50.check()
def exists():
    check50.exists("printf2.c")

@check50.check(exists)
def compiles():
    check50.c.compile("printf2.c", cc="gcc")

@check50.check(compiles)
def correct_output():
    check50.run("./printf2").stdout("This should work!").exit()
