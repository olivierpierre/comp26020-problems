import check50
import check50.c
import re

EXPECTED = ("f1:\nFLAG1 enabled\nFLAG2 enabled\n"
            "f2:\nFLAG1 enabled\nFLAG2 enabled\nFLAG3 enabled\n")

# test program calling the student's print_flags with every combination of the
# 4 flags, the student's main is renamed so that it does not clash with ours
HARNESS = r"""
#include <stdio.h>
#define main student_main
#include "enum2.c"
#undef main

int main(void) {
    for (int m = 0; m < 16; m++) {
        flags f = 0;
        if (m & 1) f |= FLAG1;
        if (m & 2) f |= FLAG2;
        if (m & 4) f |= FLAG3;
        if (m & 8) f |= FLAG4;
        printf("combination %d:\n", m);
        print_flags(f);
    }
    return 0;
}
"""

@check50.check()
def exists():
    check50.exists("enum2.c")
    with open("enum2.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("enum2.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    """output is exactly the expected one"""
    out = check50.run("./enum2").stdout()
    if out != EXPECTED:
        exp_lines, out_lines = EXPECTED.split("\n"), out.split("\n")
        for i in range(max(len(exp_lines), len(out_lines))):
            exp = exp_lines[i] if i < len(exp_lines) else None
            act = out_lines[i] if i < len(out_lines) else None
            if exp != act:
                raise check50.Failure(f"Line {i+1}: expected {exp!r}, got "
                        f"{act!r}")

@check50.check(compiles)
def all_combinations():
    """print_flags is correct for every combination of the 4 flags"""
    with open("harness.c", "w") as f:
        f.write(HARNESS)
    check50.c.compile("harness.c", cc="gcc")
    out = check50.run("./harness").stdout()
    blocks = re.split(r"combination \d+:\n", out)[1:]
    for m in range(16):
        enabled = [f"FLAG{i+1}" for i in range(4) if m & (1 << i)]
        exp = "".join(f"{flag} enabled\n" for flag in enabled)
        if m >= len(blocks) or blocks[m] != exp:
            got = blocks[m] if m < len(blocks) else ""
            desc = " | ".join(enabled) if enabled else "no flag"
            raise check50.Failure(f"With {desc} set: expected {exp!r}, got "
                    f"{got!r}")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./enum2").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc and argv are unused in the provided code, don't flag them
    check50.c.compile("enum2.c", exe_name="enum2_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
