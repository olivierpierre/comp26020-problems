import check50
import check50.c
import re

ULL_TYPEDEF_RE = r"\btypedef\s+unsigned\s+long\s+long(?:\s+int)?\s+ull\s*;"
# "typedef struct s_rectangle rectangle;" or
# "typedef struct [s_rectangle] { ... } rectangle;"
STRUCT_TYPEDEF_RE = (r"\btypedef\s+struct\s+s_rectangle\s+rectangle\s*;|"
                     r"\btypedef\s+struct(?:\s+s_rectangle)?\s*\{[^}]*\}\s*"
                     r"rectangle\s*;")

def strip_comments(buf):
    return re.sub(r"//[^\n]*|/\*.*?\*/", " ", buf, flags=re.DOTALL)

def check_output(args, exp):
    out = check50.run("./typedef " + args).stdout()
    if out != exp:
        raise check50.Failure(f"With arguments '{args}': expected {exp!r}, "
                f"got {out!r}")

@check50.check()
def exists():
    check50.exists("typedef.c")
    with open("typedef.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("typedef.c", cc="gcc")

@check50.check(exists)
def has_typedef_ull(sources_buf):
    """ull is defined with typedef and used everywhere"""
    buf = strip_comments(sources_buf)
    if not re.search(ULL_TYPEDEF_RE, buf):
        raise check50.Failure("Found no typedef for ull")
    if re.search(r"\bunsigned\s+long\s+long\b", re.sub(ULL_TYPEDEF_RE, "", buf)):
        raise check50.Failure("unsigned long long int is still used outside "
                "of the typedef, use ull instead")
    if not re.search(r"\bull\s+width\b", buf) or \
            not re.search(r"\bull\s+length\b", buf):
        raise check50.Failure("Found no use of ull")

@check50.check(exists)
def has_typedef_struct(sources_buf):
    """rectangle is defined with typedef and used everywhere"""
    buf = strip_comments(sources_buf)
    if not re.search(STRUCT_TYPEDEF_RE, buf):
        raise check50.Failure("Found no typedef for rectangle")
    # remove the typedef and the struct definition, any struct s_rectangle left
    # is a use that should have been replaced by rectangle
    rest = re.sub(STRUCT_TYPEDEF_RE, "", buf)
    rest = re.sub(r"\bstruct\s+s_rectangle\s*\{", "", rest)
    if re.search(r"\bstruct\s+s_rectangle\b", rest):
        raise check50.Failure("struct s_rectangle is still used outside of the "
                "typedef, use rectangle instead")
    if not re.search(r"\brectangle\s+r\b", buf):
        raise check50.Failure("Found no use of rectangle")

@check50.check(compiles)
def output_correct():
    """prints the rectangle dimensions"""
    check_output("50 484", "Rectangle is 50 x 484\n")
    check_output("484 50", "Rectangle is 484 x 50\n")
    check_output("0 7", "Rectangle is 0 x 7\n")

@check50.check(compiles)
def large_values():
    """handles values that do not fit in 32 bits"""
    check_output("5000000000 9223372036854775807",
            "Rectangle is 5000000000 x 9223372036854775807\n")

@check50.check(compiles)
def wrong_argument_count():
    """prints nothing without exactly 2 arguments"""
    check_output("", "")
    check_output("50", "")
    check_output("50 484 12", "")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./typedef 50 484").exit(0)
    check50.run("./typedef").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    check50.c.compile("typedef.c", exe_name="typedef_warn", cc="gcc",
                      Wall=True, Wextra=True, Werror=True)
