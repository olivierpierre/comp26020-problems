import check50
import check50.c

@check50.check()
def exists():
    check50.exists("variable.c")
    with open("variable.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("variable.c", cc="gcc")

@check50.check(exists)
def has_variables(sources_buf):
    if "int_var" not in sources_buf:
        raise check50.Failure("Could not find mention of int_var in the "
                "source")
    if "double_var" not in sources_buf:
        raise check50.Failure("Could not find mention of dobule_var in the"
                "source")

@check50.check(exists)
def has_format_specifier(sources_buf):
    buf = sources_buf
    if "%d" not in buf and "%i" not in buf:
        raise check50.Failure("Could not find and integer format specifier "
                "(%d or %i)")
    if "%f" not in buf and "%F" not in buf and "%q" not in buf and \
            "%G" not in buf:
        raise check50.Failure("Could not find and integer format specifier "
                "(%f, %F, %q, %G)")

@check50.check(compiles)
def output_correct():
    check50.run("./variable").stdout("int_var: [0-9]+", regex=True)\
            .stdout("double_var: [0-9]+\.[0-9]+", regex=True)\
            .exit()
