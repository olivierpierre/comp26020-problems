import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("strtol.c")
    with open("strtol.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("strtol.c", cc="gcc")

@check50.check(compiles)
def output_correct_standard_integer():
    check50.run("./strtol")\
            .stdout("please enter an integer number \(base 10\):")\
            .stdin("42\n")\
            .stdout("you have entered: 42")\
            .exit()

@check50.check(compiles)
def output_correct_negative_integer():
    check50.run("./strtol")\
            .stdout("please enter an integer number \(base 10\):")\
            .stdin("-42\n")\
            .stdout("you have entered: -42")\
            .exit()

@check50.check(compiles)
def output_correct_letters():
    check50.run("./strtol")\
            .stdout("please enter an integer number \(base 10\):")\
            .stdin("bar\n")\
            .stdout("invalid string")\
            .exit()

@check50.check(compiles)
def output_correct_overflow():
    check50.run("./strtol")\
            .stdout("please enter an integer number \(base 10\):")\
            .stdin("100000000000000000000\n")\
            .stdout("under/overflow")\
            .exit()

@check50.check(compiles)
def output_correct_underflow():
    check50.run("./strtol")\
            .stdout("please enter an integer number \(base 10\):")\
            .stdin("-100000000000000000000\n")\
            .stdout("under/overflow")\
            .exit()

