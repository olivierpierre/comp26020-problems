import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("macro-conditional.c")
    with open("macro-conditional.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("macro-conditional.c", exe_name="debug", cc="gcc", DDEBUG\\_MODE="1")
    check50.c.compile("macro-conditional.c", exe_name = "release", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./debug")\
            .stdout("[DEBUG] Allocating memory")\
            .stdout("[DEBUG] Allocation successfull")\
            .stdout("[DEBUG] Filling array")\
            .stdout("[DEBUG] Generated 1000 random numbers")\
            .stdout("[DEBUG] Dividing numbers into bins")\
            .stdout("[DEBUG] Printing results")\
            .stdout("bin 0: [000 - 020[ \**")\
            .stdout("bin 1: [020 - 040[ \**")\
            .stdout("bin 2: [040 - 060[ \**")\
            .stdout("bin 3: [060 - 080[ \**")\
            .stdout("bin 4: [080 - 100[ \**")\
            .stdout("[DEBUG] Printing done")\
            .stdout("[DEBUG] Memory freed")\
            .exit()
    check50.run("./release")\
            .stdout("bin 0: [000 - 020[ \**")\
            .stdout("bin 1: [020 - 040[ \**")\
            .stdout("bin 2: [040 - 060[ \**")\
            .stdout("bin 3: [060 - 080[ \**")\
            .stdout("bin 4: [080 - 100[ \**")\
            .exit()

