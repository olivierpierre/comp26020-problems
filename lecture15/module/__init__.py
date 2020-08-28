import check50
import check50.c
import re

srcs = ["main.cpp", "Pair.cpp", "Pair.h", "Trio.cpp", "Trio.h"]

@check50.check()
def exists():
    sources = {}

    for src in srcs:
        check50.exists(src)
        with open(src) as f:
            sources[src] = f.read()

    return sources

@check50.check(exists)
def compiles():
    check50.c.compile("main.cpp", "Pair.cpp", "Trio.cpp", exe_name="module",
            cc="g++")

def has_header(header, source_buffer):
    rex = "#include\s+[<\"]+\s*" + re.escape(header) + "\s*[>\"]+"
    if re.search(rex, source_buffer):
        return True
    return False

@check50.check(exists)
def validate(sources):
    # Check main
    if not has_header("Pair.h", sources["main.cpp"]) or \
            not has_header("Trio.h", sources["main.cpp"]):
                raise check50.Failure("Header(s) missing in main.cpp")

    # Check Pair
    if not has_header("Pair.h", sources["Pair.cpp"]):
            raise check50.Failure("Header(s) missing in Pair.cpp")

    # Check Trio
    if not has_header("Trio.h", sources["Trio.cpp"]):
            raise check50.Failure("Header(s) missing in Trio.cpp")
    if not has_header("Pair.h", sources["Trio.h"]):
            raise check50.Failure("Header(s) missing in Trio.h")

@check50.check(compiles)
def output_correct():
    check50.run("./module")\
            .stdout("multiply 42 and 100: 4200")\
            .stdout("add 42 and 100: 142")\
            .stdout("multiply 10, 20 and 30: 6000")\
            .stdout("add 10, 20 and 30: 60")\
            .exit()

