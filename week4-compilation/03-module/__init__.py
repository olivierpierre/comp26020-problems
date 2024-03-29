import check50
import check50.c
import re

srcs = ["main.c", "module1.c", "module1.h", "module2.c", "module2.h",
        "module3.c", "module3.h"]

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
    check50.c.compile("main.c", "module1.c", "module2.c", "module3.c",
            exe_name="module", cc="gcc")

def has_header(header, source_buffer):
    rex = "#include\s+[<\"]+\s*" + re.escape(header) + "\s*[>\"]+"
    if re.search(rex, source_buffer):
        return True
    return False

@check50.check(exists)
def validate(sources):
    # Check main
    if not has_header("module1.h", sources["main.c"]) or \
            not has_header("module2.h", sources["main.c"]) or \
            not has_header("module3.h", sources["main.c"]):
                raise check50.Failure("Header(s) missing in main.c")
    if has_header("math.h", sources["main.c"]) or \
            has_header("sys/time.h", sources["main.c"]):
            raise check50.Failure("Unneeded header(s) in main.c")

    # Check module1
    if not has_header("module1.h", sources["module1.c"]) or \
            not has_header("math.h", sources["module1.c"]):
            raise check50.Failure("Header(s) missing in module1.c")
    if has_header("stdio.h", sources["module1.c"]) or \
            has_header("sys/time.h", sources["module1.c"]) or \
            has_header("module2.h", sources["module1.c"]) or \
            has_header("module3.h", sources["module1.c"]):
        raise check50.Failure("Unneeded header(s) in module1.c")

    # Check module2
    if not has_header("module2.h", sources["module2.c"]) or \
            not has_header("sys/time.h", sources["module2.c"]):
            raise check50.Failure("Header(s) missing in module2.c")
    if  has_header("module1.h", sources["module2.c"]) or \
            has_header("module3.h", sources["module2.c"]):
        raise check50.Failure("Unneeded header(s) in module2.c")

    # Check module3
    if not has_header("module3.h", sources["module3.c"]) or \
            not has_header("stdio.h", sources["module3.c"]):
            raise check50.Failure("Header(s) missing in module3.c")
    if has_header("sys/time.h", sources["module3.c"]) or \
            has_header("math.h", sources["module3.c"]) or \
            has_header("module1.h", sources["module3.c"]) or \
            has_header("module2.h", sources["module3.c"]):
        raise check50.Failure("Unneeded header(s) in module2.c")

@check50.check(compiles)
def output_correct():
    check50.run("./module")\
            .stdout("module3_function1 called with parameter CASE2")\
            .stdout("res1: 84")\
            .stdout("res2: 1.0+")\
            .stdout("res3: [1-9]+")\
            .exit()

