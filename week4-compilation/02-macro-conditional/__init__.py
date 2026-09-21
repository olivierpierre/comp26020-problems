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
    check50.c.compile("macro-conditional.c", exe_name="debug", cc="gcc", DDEBUGMODE="1")
    check50.c.compile("macro-conditional.c", exe_name = "release", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./debug")\
            .stdout(r"\[DEBUG\] Allocating memory")\
            .stdout(r"\[DEBUG\] Allocation successfull")\
            .stdout(r"\[DEBUG\] Filling array")\
            .stdout(r"\[DEBUG\] Generated 1000 random numbers")\
            .stdout(r"\[DEBUG\] Dividing numbers into bins")\
            .stdout(r"\[DEBUG\] Printing results")\
            .stdout(r"bin 0: \[000 - 020\[ \**")\
            .stdout(r"bin 1: \[020 - 040\[ \**")\
            .stdout(r"bin 2: \[040 - 060\[ \**")\
            .stdout(r"bin 3: \[060 - 080\[ \**")\
            .stdout(r"bin 4: \[080 - 100\[ \**")\
            .stdout(r"\[DEBUG\] Printing done")\
            .stdout(r"\[DEBUG\] Memory freed")\
            .exit()
    check50.run("./release")\
            .stdout(r"bin 0: \[000 - 020\[ \**")\
            .stdout(r"bin 1: \[020 - 040\[ \**")\
            .stdout(r"bin 2: \[040 - 060\[ \**")\
            .stdout(r"bin 3: \[060 - 080\[ \**")\
            .stdout(r"bin 4: \[080 - 100\[ \**")\
            .exit()

