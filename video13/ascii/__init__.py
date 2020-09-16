import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("ascii.c")
    with open("ascii.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("ascii.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./ascii 5")\
            .stdout("capital a: A")\
            .stdout("capital b: B")\
            .stdout("capital c: C")\
            .stdout("capital d: D")\
            .stdout("capital e: E")\
            .stdout("capital f: F")\
            .stdout("capital g: G")\
            .stdout("capital h: H")\
            .stdout("capital i: I")\
            .stdout("capital j: J")\
            .stdout("capital k: K")\
            .stdout("capital l: L")\
            .stdout("capital m: M")\
            .stdout("capital n: N")\
            .stdout("capital o: O")\
            .stdout("capital p: P")\
            .stdout("capital q: Q")\
            .stdout("capital r: R")\
            .stdout("capital s: S")\
            .stdout("capital t: T")\
            .stdout("capital u: U")\
            .stdout("capital v: V")\
            .stdout("capital w: W")\
            .stdout("capital x: X")\
            .stdout("capital y: Y")\
            .stdout("capital z: Z")\
            .exit()
