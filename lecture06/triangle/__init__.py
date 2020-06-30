import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("triangle.c")
    with open("triangle.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("triangle.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./triangle 0").stdout("").exit()
    check50.run("./triangle 1").stdout("*").exit()
#    check50.run("./triangle 2").stdout("*").stdout("**").exit()
#    check50.run("./triangle 5")\
#            .stdout("*")\
#            .stdout("**")\
#            .stdout("***")\
#            .stdout("****")\
#            .stdout("*****")\
#            .exit()
#    check50.run("./triangle 15")\
#            .stdout("*")\
#            .stdout("**")\
#            .stdout("***")\
#            .stdout("****")\
#            .stdout("*****")\
#            .stdout("******")\
#            .stdout("*******")\
#            .stdout("********")\
#            .stdout("*********")\
#            .stdout("**********")\
#            .stdout("***********")\
#            .stdout("************")\
#            .stdout("*************")\
#            .stdout("**************")\
#            .stdout("***************")\
#            .exit()

