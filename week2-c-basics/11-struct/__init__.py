import check50
import check50.c
import random
import re

FIELDS_RE = (r"\{\s*unsigned\s+(?:int\s+)?hour\s*;\s*"
             r"unsigned\s+(?:int\s+)?minute\s*;\s*"
             r"unsigned\s+(?:int\s+)?second\s*;\s*\}")
re1 = r"struct\s+timestamp\s*" + FIELDS_RE + r"\s*;"
re2 = r"typedef\s+struct\s+\w+\s*" + FIELDS_RE + r"\s*\w+\s*;"

# test program calling the student's add_timestamps function directly, the
# student's main is renamed so that it does not clash with ours
HARNESS = r"""
#include <stdio.h>
#include <stdlib.h>
#define main student_main
#include "struct.c"
#undef main

int main(int argc, char **argv) {
    struct timestamp a, b, r;
    if (argc != 7)
        return 1;
    a.hour = atoi(argv[1]); a.minute = atoi(argv[2]); a.second = atoi(argv[3]);
    b.hour = atoi(argv[4]); b.minute = atoi(argv[5]); b.second = atoi(argv[6]);
    r = add_timestamps(a, b);
    printf("%u %u %u\n", r.hour, r.minute, r.second);
    return 0;
}
"""

def expected(h1, m1, s1, h2, m2, s2):
    total = (h1 + h2) * 3600 + (m1 + m2) * 60 + s1 + s2
    return f"{total // 3600} {total % 3600 // 60} {total % 60}"

def check_sum(exe, *args):
    exp = expected(*args)
    args_str = " ".join(str(a) for a in args)
    out = check50.run(f"./{exe} {args_str}").stdout()
    if not re.fullmatch(re.escape(exp) + r"\n?", out):
        raise check50.Failure(f"With arguments {args_str}: expected {exp!r}, "
                f"got {out!r}")

@check50.check()
def exists():
    check50.exists("struct.c")
    with open("struct.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("struct.c", cc="gcc")

@check50.check(exists)
def has_struct(sources_buf):
    if not re.search(re1, sources_buf) and not re.search(re2, sources_buf):
        raise check50.Failure("Can't find usage of the timestamp struct")

@check50.check(exists)
def has_function(sources_buf):
    if not re.search(r"\badd_timestamps\s*\(", sources_buf):
        raise check50.Failure("Can't find the add_timestamps function")

@check50.check(compiles)
def output_correct():
    """adds the README examples and a few other timestamps"""
    check_sum("struct", 14, 12, 5, 22, 5, 0)
    check_sum("struct", 10, 30, 50, 1, 5, 15)
    check_sum("struct", 5, 11, 44, 12, 30, 3)
    check_sum("struct", 51, 8, 4, 15, 2, 31)
    check_sum("struct", 0, 0, 0, 0, 0, 0)

@check50.check(compiles)
def carries():
    """carries seconds into minutes and minutes into hours"""
    check_sum("struct", 0, 0, 30, 0, 0, 45)
    check_sum("struct", 0, 30, 0, 0, 45, 0)
    check_sum("struct", 0, 59, 59, 0, 0, 1)
    check_sum("struct", 23, 59, 59, 23, 59, 59)

@check50.check(compiles)
def random_inputs():
    """adds random timestamps"""
    for _ in range(10):
        check_sum("struct", *[random.randint(0, 99), random.randint(0, 59),
                random.randint(0, 59), random.randint(0, 99),
                random.randint(0, 59), random.randint(0, 59)])

@check50.check(has_function)
def add_timestamps_correct():
    """add_timestamps(struct timestamp, struct timestamp) returns the sum"""
    with open("harness.c", "w") as f:
        f.write(HARNESS)
    try:
        check50.c.compile("harness.c", cc="gcc")
    except check50.Failure:
        raise check50.Failure("Could not call add_timestamps with two struct "
                "timestamp parameters and get a struct timestamp back")
    check_sum("harness", 10, 30, 50, 1, 5, 15)
    check_sum("harness", 0, 59, 59, 0, 0, 1)
    check_sum("harness", 23, 59, 59, 23, 59, 59)

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./struct 5 11 44 12 30 3").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    check50.c.compile("struct.c", exe_name="struct_warn", cc="gcc",
                      Wall=True, Wextra=True, Werror=True)
