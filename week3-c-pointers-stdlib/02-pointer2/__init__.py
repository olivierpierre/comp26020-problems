import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("pointer2.c")
    with open("pointer2.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("pointer2.c", cc="gcc")

@check50.check(exists)
def validate(sources_buf):
    if re.search("printf\(.*,\s*.*lm3.*\)", sources_buf):
        raise check50.Failure("Do not use lm3 in printf parameters")
    if re.search("printf\(.*,\s*.*lm2.*\)", sources_buf):
        raise check50.Failure("Do not use lm2 in printf parameters")

@check50.check(exists)
def validate2(sources_buf):
    if not re.search("printf\(.*,\s*lm1\s*.\s*next\s*->\s*next\s*->value\s*\)",
            sources_buf) and \
    not re.search("printf\(.*\(\s*\*\s*\(\s*\*\s*lm1\s*\.\s*next\s*\)\s*\.\s*next\s*\)\s*\.\s*value\s*\)", sources_buf) and \
    not re.search("printf\(.*\*\(\(\*\(lm1\.next\)\)\.next\)\)\.value", source_buf):
        raise check50.Failure("Could not find the proper pointer chain walk")

@check50.check(compiles)
def output_correct():
    check50.run("./pointer2").stdout("third member value is: 3").exit()
