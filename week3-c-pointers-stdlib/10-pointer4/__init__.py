import check50
import check50.c
import re

LITERAL = r'"hello, world!\n"'

# strings replacing LITERAL in the mutation test: (C literal, expected output)
OTHER_STRINGS = [
    (r'"pointers are fun\n"', "pointers are fun\n"),
    (r'"x"', "x"),
    (r'"A longer string, with digits 0123456789 and symbols: ?!*&.\n"',
     "A longer string, with digits 0123456789 and symbols: ?!*&.\n"),
]

# name of a declared char * variable (possibly const)
CHAR_PTR_RE = r"\bchar\s*(?:\bconst\b\s*)?\*\s*(?:\bconst\b\s*)?([A-Za-z_]\w*)"
# NAME is incremented
INCR_RE = (r"\+\+\s*{0}\b|\b{0}\s*\+\+|\b{0}\s*\+=|"
           r"\b{0}\s*=\s*{0}\s*\+")
# NAME is dereferenced
DEREF_RE = r"\*\s*\(?\s*{0}\b"
# functions printing a whole string at once
STRING_FUNCS_RE = r"\b(puts|fputs|fwrite|write)\s*\("

# leaks are not checked, ASan errors are reported with a distinctive exit code
ASAN_EXITCODE = 99
ASAN_OPTIONS = f"detect_leaks=0:exitcode={ASAN_EXITCODE}"

def strip_comments(buf):
    return re.sub(r"//[^\n]*|/\*.*?\*/", " ", buf, flags=re.DOTALL)

def check_output(exe, exp, what):
    out = check50.run(f"./{exe}").stdout()
    if out != exp:
        raise check50.Failure(f"{what}: expected {exp!r}, got {out!r}")

def check_asan(exe, what):
    run = check50.run(f"./{exe}", env={"ASAN_OPTIONS": ASAN_OPTIONS})
    out = run.stdout()  # waits for the program to exit and sets exitcode
    if run.exitcode == ASAN_EXITCODE or "AddressSanitizer" in out:
        error = re.search(r"AddressSanitizer: [\w-]+", out)
        raise check50.Failure(f"{what}: memory error detected: " +
                (error.group(0) if error else "unknown error") +
                ", compile with 'gcc -fsanitize=address pointer4.c -o "
                "pointer4' and run ./pointer4 to see the full report")

@check50.check()
def exists():
    check50.exists("pointer4.c")
    with open("pointer4.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("pointer4.c", cc="gcc")

@check50.check(exists)
def validate(sources_buf):
    """no square brackets in the source and no %s"""
    for i, line in enumerate(sources_buf.split("\n")):
        if "[" in line or "]" in line:
            raise check50.Failure(f"There should be no '[' or ']' in the "
                    f"sources, found on line {i+1}: {line.strip()!r}")
    if "%s" in strip_comments(sources_buf):
        raise check50.Failure("There should be no '%s' in the sources")

@check50.check(exists)
def prints_char_by_char(sources_buf):
    """the string is printed character by character"""
    buf = strip_comments(sources_buf)
    m = re.search(STRING_FUNCS_RE, buf)
    if m:
        raise check50.Failure(f"Found a call to {m.group(1)}, the string "
                "should be printed character by character")
    if re.search(r"\bprintf\s*\(\s*[^\s\"]", buf):
        raise check50.Failure("Found a call to printf whose first parameter "
                "is not a format string literal, the string should be printed "
                "character by character")

@check50.check(exists)
def pointer_iterator(sources_buf):
    """a char * pointer is incremented and dereferenced to access characters"""
    buf = strip_comments(sources_buf)
    # turn declarations such as "char *p" into "char p" so that they are not
    # mistaken for dereferences
    decl_free = re.sub(r"\bchar\s*(?:\bconst\b\s*)?\*", "char ", buf)
    names = re.findall(CHAR_PTR_RE, buf)
    if not names:
        raise check50.Failure("Could not find the declaration of a char * "
                "pointer")
    for name in names:
        if re.search(INCR_RE.format(name), buf) and \
                re.search(DEREF_RE.format(name), decl_free):
            return
    raise check50.Failure("Could not find a char * pointer that is both "
            "incremented (e.g. p++) and dereferenced (e.g. *p) to access the "
            "characters of the string")

@check50.check(compiles)
def output_correct():
    """output is exactly 'hello, world!'"""
    check_output("pointer4", "hello, world!\n", "Running ./pointer4")

@check50.check(compiles)
def other_strings():
    """prints other strings when the string literal is changed"""
    with open("pointer4.c") as f:
        sources_buf = f.read()
    if LITERAL not in sources_buf:
        raise check50.Failure("Could not find the string literal "
                f"{LITERAL} in the sources, keep the declaration of the "
                "string from the provided program")
    # only the first occurrence (the declaration of string) is replaced
    for i, (literal, exp) in enumerate(OTHER_STRINGS):
        with open(f"pointer4_mut{i}.c", "w") as f:
            f.write(sources_buf.replace(LITERAL, literal, 1))
        check50.c.compile(f"pointer4_mut{i}.c", cc="gcc")
        check_output(f"pointer4_mut{i}", exp, "With the string replaced by "
                f"{literal}")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./pointer4").exit(0)

@check50.check(exists)
def no_memory_errors(sources_buf):
    """no out-of-bounds memory accesses (AddressSanitizer)"""
    check50.c.compile("pointer4.c", exe_name="pointer4_asan", cc="gcc",
                      fsanitize="address")
    check_asan("pointer4_asan", "Running ./pointer4")
    # also with a string of another length, if the literal is found
    if LITERAL in sources_buf:
        literal = OTHER_STRINGS[1][0]
        with open("pointer4_asan_mut.c", "w") as f:
            f.write(sources_buf.replace(LITERAL, literal, 1))
        check50.c.compile("pointer4_asan_mut.c", cc="gcc",
                          fsanitize="address")
        check_asan("pointer4_asan_mut", f"With the string replaced by "
                f"{literal}")

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc and argv are unused in the provided code, don't flag them
    check50.c.compile("pointer4.c", exe_name="pointer4_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
