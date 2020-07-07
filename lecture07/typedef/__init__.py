import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("typedef.c")
    with open("typedef.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("typedef.c", cc="gcc")

@check50.check(exists)
def has_typedef_ull(sources_buf):
    if "typedef unsigned long long int ull;" not in sources_buf:
        raise check50.Failure("Found no typedef for ull")
    if "ull width;" not in sources_buf or "ull length;" not in sources_buf:
        raise check50.Failure("Found no use of ull")

@check50.check(exists)
def has_typedef_struct(sources_buf):
    if not re.search("typedef struct s_rectangle {$.*} rectangle;",
            sources_buf, re.DOTALL | re.MULTILINE) and \
            "typedef struct s_rectangle rectangle;" not in sources_buf:
        raise check50.Failure("Found no typedef for rectangle"
    if "rectangle r" not in sources_buf:
        raise check50.Failure("Found no use of rectangle"

@check50.check(compiles)
def output_correct():
    check50.run("./typedef 50 484").stdout("Rectangle is 50 x 484").exit()
    check50.run("./typedef 484 50").stdout("Rectangle is 484 x 50").exit()
    check50.run("./typedef").stdout("").exit()
