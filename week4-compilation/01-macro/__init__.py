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
    if not re.search(r"\#define\s+SAMPLE_SIZE\s+10", sources_buf):
        raise check50.Failure("Can't find a correct definition of SAMPLE_SIZE")
    if not re.search(r"\#define\s+MAX_VAL\s+50", sources_buf):
        raise check50.Failure("Can't find a correct definition of MAX_VAL")

    if sources_buf.count("SAMPLE_SIZE") != 5:
        raise check50.Failure("There should be 5 occurences of SAMPLE_SIZE in"
                " the sources")
    if sources_buf.count("MAX_VAL") != 11:
        raise check50.Failure("There should be 11 occurences of MAX_VAL in"
                " the sources")

@check50.check(compiles)
def output_correct():
    check50.run("./macro")\
            .stdout(r"bin 0: \[000 - 010\[ \**")\
            .stdout(r"bin 1: \[010 - 020\[ \**")\
            .stdout(r"bin 2: \[020 - 030\[ \**")\
            .stdout(r"bin 3: \[030 - 040\[ \**")\
            .stdout(r"bin 4: \[040 - 050\[ \**")\
            .exit()

