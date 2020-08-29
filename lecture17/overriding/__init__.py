import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("overriding.cpp")
    with open("overriding.cpp") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("overriding.cpp", exe_name="overriding", cc="g++")

@check50.check(exists)
def validate(sources_buf):
    pass

@check50.check(compiles)
def output_correct():
    check50.run("./overriding")\
        .stdout("array\[0\] has [24]+ wheels")\
        .stdout("array\[1\] has [24]+ wheels")\
        .stdout("array\[2\] has [24]+ wheels")\
        .stdout("array\[3\] has [24]+ wheels")\
        .stdout("array\[4\] has [24]+ wheels")\
        .stdout("array\[5\] has [24]+ wheels")\
        .stdout("array\[6\] has [24]+ wheels")\
        .stdout("array\[7\] has [24]+ wheels")\
        .stdout("array\[8\] has [24]+ wheels")\
        .stdout("array\[9\] has [24]+ wheels")\
        .exit()

