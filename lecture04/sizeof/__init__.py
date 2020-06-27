import check50
import check50.c

@check50.check()
def exists():
    check50.exists("sizes.c")
    with open("sizes.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("sizes.c", cc="gcc")

@check50.check(exists)
def has_sizeof(sources_buf):
    soi_re = "sizeof\(\s*int\s*\)"
    sod_re = "sizeof\(\s*double\s*\)"
    soull_re = "sizeof\(\s*unsigned\s*long\s*long\s*[int\s]+\)"

    if not re.search(soi_re, sources_buf):
        raise check50.Failure("Could not find a call to sizeof(int)")
    if not re.search(sod_re, sources_buf):
        raise check50.Failure("Could not find a call to sizeof(double)")
    if not re.search(soull_re, sources_buf):
        raise check50.Failure("Could not find a call to sizeof(unsigned long "
                "long int)")

@check50.check(compiles)
def output_correct():
    check50.run("./sizes").stdout("4")\
            .stdout("8")\
            .stdout("8")\
            .stdout("256")\
            .exit()
