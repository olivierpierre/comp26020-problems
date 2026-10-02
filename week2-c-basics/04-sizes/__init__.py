import check50
import check50.c
import re

# type name as printed in messages -> regex matching that type
TYPES = {
    "int": r"int",
    "double": r"double",
    "unsigned long long int": r"unsigned\s+long\s+long(?:\s+int)?",
}

def strip_comments(buf):
    return re.sub(r"//[^\n]*|/\*.*?\*/", " ", buf, flags=re.DOTALL)

def declared_vars(buf, type_re):
    """names of the (non-pointer) variables declared with type type_re"""
    decl_re = (r"(?:^|[;{}])\s*(?:(?:const|static|volatile)\s+)*" + type_re +
               r"\s+([^;{}()]*);")
    names = []
    for decl_list in re.findall(decl_re, buf, re.MULTILINE):
        for decl in decl_list.split(","):
            m = re.match(r"\s*([A-Za-z_]\w*)", decl)
            if m:
                names.append(m.group(1))
    return names

@check50.check()
def exists():
    check50.exists("sizes.c")
    with open("sizes.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("sizes.c", cc="gcc")

@check50.check(exists)
def has_sizeof(sources_buf):
    """sizeof is used on int, double and unsigned long long int"""
    buf = strip_comments(sources_buf)
    for type_name, type_re in TYPES.items():
        # either sizeof(type) or sizeof applied to a variable of that type
        operands = [r"\(\s*" + type_re + r"\s*\)"]
        operands += [r"\(?\s*" + v + r"\b" for v in declared_vars(buf, type_re)]
        if not any(re.search(r"\bsizeof\s*" + o, buf) for o in operands):
            raise check50.Failure(f"Could not find sizeof applied to "
                    f"{type_name} or to a variable of type {type_name}")

@check50.check(exists)
def no_hardcoded_sizes(sources_buf):
    """sizes are not hardcoded"""
    m = re.search(r"(?<![\w.%])(4|8|256)(?![\w.])",
            strip_comments(sources_buf))
    if m:
        raise check50.Failure(f"Found the hardcoded value {m.group(1)} in the "
                "source, sizes should be obtained with sizeof")

@check50.check(compiles)
def output_correct():
    """output is exactly 4, 8, 8 and 256 on separate lines"""
    out = check50.run("./sizes").stdout()
    if out != "4\n8\n8\n256\n":
        raise check50.Failure(f"Expected '4\\n8\\n8\\n256\\n', got {out!r}")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./sizes").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    check50.c.compile("sizes.c", exe_name="sizes_warn", cc="gcc",
                      Wall=True, Wextra=True, Werror=True)
