import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("macro.c")
    with open("macro.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("macro.c", cc="gcc")

@check50.check(exists)
def validate(sources_buf):
    if not re.search("\#define\s+SAMPLE_SIZE\s+10", sources_buf):
        raise check50.Failure("Can't find a correct definition of SAMPLE_SIZE")
    if not re.search("\#define\s+MAX_VAL\s+50", sources_buf):
        raise check50.Failure("Can't find a correct definition of MAX_VAL")

@check50.check(compiles)
def output_correct():
    check50.run("./macro")\
            .stdout("bin 0: \[000 - 010\[ \**")\
            .stdout("bin 1: \[010 - 020\[ \**")\
            .stdout("bin 2: \[020 - 030\[ \**")\
            .stdout("bin 3: \[030 - 040\[ \**")\
            .stdout("bin 4: \[040 - 050\[ \**")\
            .exit()

