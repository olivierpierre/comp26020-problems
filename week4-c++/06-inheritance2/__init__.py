import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("inheritance2.cpp")
    with open("inheritance2.cpp") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("inheritance2.cpp", exe_name="inheritance2", cc="g++")

@check50.check(exists)
def validate(sources_buf):
    pass

@check50.check(compiles)
def output_correct():
    check50.run("./inheritance2")\
            .stdout("derived method called, z: 5. Now calling base_method")\
            .stdout("base_method called, x: 3, y: 4")\
            .exit()

