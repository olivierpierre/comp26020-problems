import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("constructor.cpp")
    with open("constructor.cpp") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("constructor.cpp", exe_name="constructor", cc="g++")

@check50.check(exists)
def validate(sources_buf):
    if re.search("p\.x\s*=\s*[0-9]+\s*;", sources_buf) or \
            re.search("p\.y\s*=\s*[0-9]+\s*;", sources_buf):
        raise check50.Failure("Should not initialize p's members in main")
    if "Pair p(10, 20);" not in sources_buf and \
            "Pair p(10,20);" not in sources_buf and \
            "Pair(10,20);" not in sources_buf and \
            "Pair(10, 20);" not in sources_buf:
        raise check50.Failure("Couldn't find call to the constructor")

@check50.check(compiles)
def output_correct():
    check50.run("./constructor")\
            .stdout("p.x is 10, p.y is 20")\
            .exit()

