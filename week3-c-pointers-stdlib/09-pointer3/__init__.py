import check50
import check50.c
import random
import re

# test program wrapping the student's printf calls: for each address printed
# (%p, or %lx/%llx/%zx...), it records the int stored at that address at the
# time of the call; the recorded values are printed after a marker at exit
HARNESS = r"""
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>

#define CHK_MAX 64
static int chk_n;
static int chk_vals[CHK_MAX];

static int chk_printf(const char *fmt, ...) {
    va_list ap, ap2;
    const char *f;
    int ret;

    va_start(ap, fmt);
    va_copy(ap2, ap);
    ret = vprintf(fmt, ap);
    va_end(ap);

    for (f = fmt; *f; f++) {
        int len = 0;
        unsigned long addr = 0;
        if (*f != '%')
            continue;
        f++;
        if (*f == '%')
            continue;
        while (*f && strchr("-+ #0'", *f))
            f++;
        if (*f == '*') { (void)va_arg(ap2, int); f++; }
        else while (*f >= '0' && *f <= '9') f++;
        if (*f == '.') {
            f++;
            if (*f == '*') { (void)va_arg(ap2, int); f++; }
            else while (*f >= '0' && *f <= '9') f++;
        }
        while (*f && strchr("hlLqjzt", *f)) {
            len = (*f == 'h') ? 1 : (*f == 'L') ? 3 : 2;
            f++;
        }
        switch (*f) {
            case 'p':
                addr = (unsigned long)va_arg(ap2, void *);
                break;
            case 'x': case 'X':
                if (len == 2) addr = va_arg(ap2, unsigned long);
                else (void)va_arg(ap2, unsigned int);
                break;
            case 'd': case 'i': case 'u': case 'o': case 'c':
                if (len == 2) (void)va_arg(ap2, long);
                else (void)va_arg(ap2, int);
                break;
            case 's': case 'n':
                (void)va_arg(ap2, void *);
                break;
            case 'e': case 'E': case 'f': case 'F':
            case 'g': case 'G': case 'a': case 'A':
                if (len == 3) (void)va_arg(ap2, long double);
                else (void)va_arg(ap2, double);
                break;
            case '\0':
                f--;
                break;
        }
        if (addr > 4096 && addr % sizeof(int) == 0 && chk_n < CHK_MAX)
            chk_vals[chk_n++] = *(int *)addr;
    }
    va_end(ap2);
    return ret;
}

static void chk_report(void) {
    int i;
    fflush(stdout);
    fputs("\n@@CHECK@@", stdout);
    for (i = 0; i < chk_n; i++)
        fprintf(stdout, " %d", chk_vals[i]);
    fputs("\n", stdout);
    fflush(stdout);
}

#define printf chk_printf
#define main student_main
#include "pointer3.c"
#undef main
#undef printf

int main(int argc, char **argv) {
    atexit(chk_report);
    return student_main(argc, argv);
}
"""

ADDR_RE = r"0x[0-9a-fA-F]+"

def check_value(exe, n):
    """run ./exe n and check the output format and the printed value"""
    out = check50.run(f"./{exe} {n}").stdout()
    exp = f"Variable contains {n} and is located @"
    if not re.fullmatch(re.escape(exp) + ADDR_RE + r"\n?", out):
        raise check50.Failure(f"With argument {n}: expected "
                f"'{exp}0x<address in hexadecimal>', got {out!r}")

@check50.check()
def exists():
    check50.exists("pointer3.c")
    with open("pointer3.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("pointer3.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    """output is 'Variable contains N and is located @0x...' for the README examples and others"""
    for n in [5, 93, 156, 42]:
        check_value("pointer3", n)

@check50.check(compiles)
def negative_and_zero():
    """handles zero, negative numbers and large values"""
    for n in [0, -7, -123456, 2147483647, -2147483648]:
        check_value("pointer3", n)

@check50.check(compiles)
def random_inputs():
    """outputs the value for random inputs"""
    for _ in range(5):
        check_value("pointer3", random.randint(-1000000000, 1000000000))

@check50.check(compiles)
def address_of_variable():
    """the printed address is the address of an int containing the value"""
    with open("harness.c", "w") as f:
        f.write(HARNESS)
    try:
        check50.c.compile("harness.c", cc="gcc")
    except check50.Failure:
        raise check50.Failure("Could not build the test program wrapping "
                "printf, main should be declared as "
                "'int main(int argc, char **argv)'")
    for n in [1234567, -98765, random.randint(10000000, 1000000000)]:
        # the output format itself is tested by the other checks
        out = check50.run(f"./harness {n}").stdout()
        m =re.search(r"@@CHECK@@([ \d-]*)", out)
        found = [int(v) for v in m.group(1).split()] if m else []
        if n not in found:
            raise check50.Failure(f"With argument {n}: the address printed "
                    f"does not point to an int containing {n}, print the "
                    "address of the variable with printf and %p (e.g. "
                    "&variable)")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./pointer3 5").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc may legitimately be unused, don't flag it
    check50.c.compile("pointer3.c", exe_name="pointer3_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
