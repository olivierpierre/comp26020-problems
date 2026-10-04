import check50
import check50.c
import random
import re
import time

OUTPUT_RE = r"sleep duration: (\d+\.\d{6}) seconds\n?"

# prepended to the student's source: sleep(n) is replaced by a sleep of
# n + 1.5 seconds, the displayed duration must follow if it is really measured
EXTRA_SLEEP = 1.5
MUTATION_HEADER = r"""
#include <unistd.h>
#include <time.h>
static unsigned int check50_sleep(unsigned int s) {
    struct timespec ts = { s + 1, 500000000 };
    while (nanosleep(&ts, &ts));
    return 0;
}
#define sleep(x) check50_sleep(x)
#line 1 "time.c"
"""

def strip_comments_and_strings(buf):
    return re.sub(r"//[^\n]*|/\*.*?\*/|\"(?:\\.|[^\"\\\n])*\"", " ", buf,
            flags=re.DOTALL)

def check_sleep(exe, n, slept=None):
    """run exe with n as argument, the program is expected to sleep for slept
    seconds (n by default) and to display the measured duration"""
    if slept is None:
        slept = n
    start = time.monotonic()
    out = check50.run(f"./{exe} {n}").stdout(timeout=slept + 5)
    elapsed = time.monotonic() - start
    m = re.fullmatch(OUTPUT_RE, out)
    if not m:
        raise check50.Failure(f"With argument {n}: expected output of the form "
                f"'sleep duration: {int(slept)}.xxxxxx seconds' (with 6 decimals), "
                f"got {out!r}")
    measured = float(m.group(1))
    if elapsed < slept - 0.05:
        raise check50.Failure(f"With argument {n}: the program ran for "
                f"{elapsed:.3f} seconds only, it should sleep for {slept} "
                "seconds")
    if measured <= slept:
        raise check50.Failure(f"With argument {n}: displayed duration is "
                f"{m.group(1)}, it should be slightly more than {slept} "
                "seconds (a call to sleep never takes exactly the requested "
                "time): measure the time with a sub-second precision clock "
                "(e.g. gettimeofday or clock_gettime) and do not use integer "
                "divisions in the computation")
    if measured > elapsed + 0.05:
        raise check50.Failure(f"With argument {n}: displayed duration is "
                f"{m.group(1)}, but the program only ran for {elapsed:.3f} "
                "seconds")

@check50.check()
def exists():
    check50.exists("time.c")
    with open("time.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("time.c", cc="gcc", std="gnu99")

@check50.check(exists)
def has_sleep(sources_buf):
    """calls the sleep function"""
    if not re.search(r"\bsleep\s*\(", strip_comments_and_strings(sources_buf)):
        raise check50.Failure("Could not find a call to the sleep function")

@check50.check(compiles)
def output_correct():
    """sleeps and displays the measured duration for the README examples"""
    check_sleep("time", 3)
    check_sleep("time", 5)

@check50.check(compiles)
def other_durations():
    """sleeps and displays the measured duration for other values of n"""
    check_sleep("time", 1)
    check_sleep("time", random.randint(2, 4))

@check50.check(has_sleep)
def duration_measured():
    """the displayed duration is measured, not computed from n"""
    with open("time.c") as f:
        src = f.read()
    with open("time_mut.c", "w") as f:
        f.write(MUTATION_HEADER + src)
    check50.c.compile("time_mut.c", exe_name="time_mut", cc="gcc",
                      std="gnu99")
    try:
        check_sleep("time_mut", 1, 1 + EXTRA_SLEEP)
    except check50.Failure as e:
        raise check50.Failure("When the call to sleep(1) is replaced by a "
                f"sleep of {1 + EXTRA_SLEEP} seconds, the displayed duration "
                f"should change accordingly. {e}")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./time 1").exit(0, timeout=6)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    check50.c.compile("time.c", exe_name="time_warn", cc="gcc", std="gnu99",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
