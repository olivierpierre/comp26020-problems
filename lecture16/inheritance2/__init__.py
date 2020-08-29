import check50
import check50.c
import re

srcs = ["inheritance2.cpp", "Employee.h", "Employee.cpp"]

@check50.check()
def exists():
    sources = {}

    for src in srcs:
        check50.exists(src)
        with open(src) as f:
            sources[src] = f.read()

    return sources

@check50.check(exists)
def compiles():
    check50.c.compile("inheritance2.cpp", "Employee.cpp",  exe_name="inheritance2", cc="g++")

@check50.check(exists)
def validate(sources):
    sources_buf = sources["Employee.h"]
    if not re.search("class\s+Employee", sources_buf):
        raise check50.Failure("Could not find class Employee")
    if not re.search("class\s+TemporaryEmployee\s+:\s+public\s+Employee", sources_buf):
        raise check50.Failure("Could not find class TemporaryEmployee or class "\
                "TemporaryEmployee does not inheritates correctly")
    if not re.search("class\s+PermanentEmployee\s+:\s+public\s+Employee", sources_buf):
        raise check50.Failure("Could not find class PermanentEmployee or class "\
                "PermanentEmployee does not inheritates correctly")
    if not re.search("class\s+Consultant\s+:\s+public\s+TemporaryEmployee", sources_buf):
        raise check50.Failure("Could not find class Consultant or class "\
                "Consultant does not inheritates correctly")
    if not re.search("class\s+Manager\s+:\s+public\s+PermanentEmployee", sources_buf):
        raise check50.Failure("Could not find class Manager or class "\
                "Manager does not inheritates correctly")
    if not re.search("class\s+Director\s+:\s+public\s+Manager", sources_buf):
        raise check50.Failure("Could not find class Director or class "\
                "Director does not inheritates correctly")

@check50.check(compiles)
def output_correct():
    check50.run("./inheritance2")\
            .stdout("[1234 - James] I'm consulting on Aerodynamics until 15/01/2022")\
            .stdout("[1212 - Stella] I'm taking an important decision in office 10")\
            .stdout("[1678 - Elon] I'm taking an very important decision in office 42")\
            .exit()

