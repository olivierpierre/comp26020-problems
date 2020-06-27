import check50
import check50.c

@check50.check()
def exists():
    check50.exists("variable.c")

@check50.check(exists)
def compiles():
    check50.c.compile("variable.c", cc="gcc")

@check50.check(exists)
def has_int_var():
    with open("variable.c") as f:
        buf = f.read()
    if "int_var" not in buf:
        raise check50.Failure("Could not find mention to int_var")

@check50.check(compiles)
def output_correct():
    check50.run("./variable").stdout("int_var: [0-9]+", regex=True)\
            .stdout("double_var: [0-9]+\.[0-9]+", regex=True)\
            .exit()
