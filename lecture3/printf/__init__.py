 
import check50
import check50.c

@check50.check()
def exists():
    """hello.c exists."""
    check50.exists("hello.c")

@check50.check(exists)
def compiles():
    """hello.c compiles."""
    check50.c.compile("hello.c", lcs50=False)

@check50.check(compiles)
def goodbye_printed():
    """prints 'Goodbye, world!' """
    check50.run("./hello")..stdout("Goodbye, world!").exit()
