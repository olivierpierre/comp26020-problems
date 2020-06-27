import check50
import check50.c

@check50.check()
def exists():
    check50.exists("goodbye.c")

@check50.check(exists)
def compiles():
    check50.c.compile("goodbye.c", cc="gcc", "-O3")

@check50.check(compiles)
def goodbye_printed():
    check50.run("./goodbye").stdout("[Gg]oodbye, [Ww]orld!", regex=True).exit()
