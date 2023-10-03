import check50
import check50.c
import re

regex = re.compile("   ######[ ]*\n ##      ##[ ]*\n#[ ]*\n#[ ]*\n#[ ]*\n#[ ]*\n#[ ]*\n ##      ##[ ]*\n   ######[ ]*")

@check50.check()
def exists():
    check50.exists("printf.c")

@check50.check(exists)
def compiles():
    check50.c.compile("printf.c", cc="gcc")

@check50.check(compiles)
def large_c_printed():
    out = check50.run("./printf").stdout()
    if not regex.match(out):
        raise check50.Failure("Incorrect output")
