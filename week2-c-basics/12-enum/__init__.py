import check50
import check50.c
import re

DAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY",
        "SUNDAY"]

re1 = r"\benum\s+day\s*\{([^}]*)\}"
re2 = r"\benum\s+day\s+\w+"
re3 = r"\n\s*case\s+__DAY__\s*:"
# an assignment (or initialisation) of WEDNESDAY, not a comparison
INIT_RE = r"((?<![=!<>])=\s*)WEDNESDAY\b"

def strip_comments(buf):
    return re.sub(r"//[^\n]*|/\*.*?\*/", " ", buf, flags=re.DOTALL)

@check50.check()
def exists():
    check50.exists("enum.c")
    with open("enum.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("enum.c", cc="gcc")

@check50.check(exists)
def has_enum(sources_buf):
    """enum day is defined with constants MONDAY to SUNDAY"""
    res = re.search(re1, strip_comments(sources_buf))
    if not res:
        raise check50.Failure("Can't find the definition of enum day")
    constants = re.findall(r"\b[A-Za-z_]\w*\b", re.sub(r"=[^,]*", "",
            res.group(1)))
    missing = [d for d in DAYS if d not in constants]
    if missing:
        raise check50.Failure("enum day does not define " + ", ".join(missing))

@check50.check(exists)
def declare_enum_var(sources_buf):
    if not re.search(re2, sources_buf):
        raise check50.Failure("Can't find a variable declared with the enum type")

@check50.check(exists)
def initialised_with_enum(sources_buf):
    """the day variable is set to WEDNESDAY"""
    if not re.search(INIT_RE, strip_comments(sources_buf)):
        raise check50.Failure("Can't find a variable set to WEDNESDAY")

@check50.check(exists)
def cases_enum(sources_buf):
    for day in DAYS:
        if not re.search(re3.replace("__DAY__", day), sources_buf):
            raise check50.Failure("Can't find usage of the enum value in case statements")

@check50.check(compiles)
def output_correct():
    """output is exactly 'Today is: Wednesday'"""
    out = check50.run("./enum").stdout()
    if out != "Today is: Wednesday\n":
        raise check50.Failure(f"Expected 'Today is: Wednesday\\n', got {out!r}")

@check50.check(initialised_with_enum)
def all_days():
    """prints the right name when the variable is set to each day"""
    with open("enum.c") as f:
        sources_buf = f.read()
    for day in DAYS:
        with open("enum_day.c", "w") as f:
            f.write(re.sub(INIT_RE, r"\g<1>" + day, sources_buf, count=1))
        check50.c.compile("enum_day.c", cc="gcc")
        exp = f"Today is: {day.capitalize()}\n"
        out = check50.run("./enum_day").stdout()
        if out != exp:
            raise check50.Failure(f"With the variable set to {day}: expected "
                    f"{exp!r}, got {out!r}")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./enum").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc and argv are unused in the provided code, don't flag them
    check50.c.compile("enum.c", exe_name="enum_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
