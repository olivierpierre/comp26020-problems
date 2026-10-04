import check50
import check50.c
import re

EXPECTED = "".join(f"{i}\n" for i in range(10))

def strip_comments(buf):
    return re.sub(r"//[^\n]*|/\*.*?\*/", " ", buf, flags=re.DOTALL)

def string_literals(buf):
    return re.findall(r'"((?:[^"\\\n]|\\.)*)"', strip_comments(buf))

@check50.check()
def exists():
    check50.exists("malloc4.c")
    with open("malloc4.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("malloc4.c", cc="gcc")

@check50.check(exists)
def validate(sources_buf):
    """the array is allocated with malloc and sizeof, and freed"""
    buf = strip_comments(sources_buf)
    if not re.search(r"\bmalloc\s*\(", buf):
        raise check50.Failure("Cant find call to malloc")
    if not re.search(r"\bmalloc\s*\([^;]*\bsizeof\b", buf):
        raise check50.Failure("Cant find call to malloc using sizeof to "
                "compute the size of the array")
    if not re.search(r"\bfree\s*\(", buf):
        raise check50.Failure("Cant find call to free")

@check50.check(exists)
def not_hardcoded(sources_buf):
    """the numbers are not hardcoded in the printed strings"""
    for lit in string_literals(sources_buf):
        if re.search(r"[0-9]", lit):
            raise check50.Failure(f"Found the string \"{lit}\" containing a "
                    "number: the values should be stored in the array and "
                    "printed from it with printf(\"%d\\n\", ...)")

@check50.check(compiles)
def output_correct():
    """output is exactly 0 to 9, one number per line"""
    out = check50.run("./malloc4").stdout()
    # tolerate trailing spaces and a missing final newline
    got = "\n".join(l.rstrip(" ") for l in out.rstrip("\n").split("\n")) + "\n"
    if got != EXPECTED:
        raise check50.Failure(f"Expected {EXPECTED!r}, got {out!r}")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./malloc4").exit(0)

@check50.check(compiles)
def valgrind_memcheck():
    """no memory errors or leaks (valgrind)"""
    check50.c.valgrind("./malloc4").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc and argv are typically unused, don't flag them
    check50.c.compile("malloc4.c", exe_name="malloc4_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
