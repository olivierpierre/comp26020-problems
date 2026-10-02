import check50
import check50.c
import re

# string[<index>] = <value>; as a statement (not the declaration)
ASSIGN_RE = r"(?:^|[;{}])\s*string\s*\[\s*([0-9]+)\s*\]\s*=\s*([^;]+);"
NUL_RE = r"'\\0'|0"

def assignments(buf):
    """index -> assigned value (as written in the source) for each string[i] ="""
    return {int(i): v.strip()
            for i, v in re.findall(ASSIGN_RE, buf, re.MULTILINE)}

@check50.check()
def exists():
    check50.exists("string.c")
    with open("string.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("string.c", cc="gcc")

@check50.check(exists)
def has_right_size(sources_buf):
    """the array is large enough for every character written to it"""
    res = re.search(r"\bchar\s+string\s*\[\s*([0-9]+)\s*\]", sources_buf)
    if not res:
        raise check50.Failure("Cannot determine the string size")

    size = int(res.group(1))
    if size < 9:
        raise check50.Failure("String size not large enough")

    written = assignments(sources_buf)
    if written and max(written) >= size:
        raise check50.Failure(f"string[{max(written)}] is written but the "
                f"array only has {size} elements")

@check50.check(exists)
def built_char_by_char(sources_buf):
    """the string is still built character by character"""
    if re.search(r'"hi there', sources_buf):
        raise check50.Failure("The string should be built character by "
                "character, not from a string literal")
    written = assignments(sources_buf)
    for i, c in enumerate("hi there"):
        if written.get(i) != f"'{c}'":
            raise check50.Failure(f"Could not find string[{i}] = '{c}';")

@check50.check(exists)
def has_termination_character(sources_buf):
    """the string is terminated with '\\0'"""
    written = assignments(sources_buf)
    if re.fullmatch(NUL_RE, written.get(8, "")):
        return
    if written.get(8) == r"'\n'" and re.fullmatch(NUL_RE, written.get(9, "")):
        return
    raise check50.Failure("Cannot find string termination character")

@check50.check(compiles)
def output_correct():
    """output is exactly 'hi there'"""
    out = check50.run("./string").stdout()
    # also accept the extra empty line printed when string[8] is kept as '\n'
    if out not in ["hi there\n", "hi there\n\n"]:
        raise check50.Failure(f"Expected 'hi there\\n', got {out!r}")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./string").exit(0)

@check50.check(exists)
def no_memory_errors(sources_buf):
    """no out-of-bounds memory accesses (AddressSanitizer)"""
    check50.c.compile("string.c", exe_name="string_asan", cc="gcc",
                      fsanitize="address")
    run = check50.run("./string_asan")
    out = run.stdout()  # waits for the program to exit and sets exitcode
    if run.exitcode != 0:
        error = re.search(r"AddressSanitizer: [\w-]+", out)
        raise check50.Failure("Memory error detected: " +
                (error.group(0) if error else "unknown error") +
                ", compile with 'gcc -fsanitize=address string.c -o string' "
                "and run ./string to see the full report")

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc and argv are unused in the provided code, don't flag them
    check50.c.compile("string.c", exe_name="string_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
