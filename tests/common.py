import os
import sys

from asgish.testutils import ProcessTestServer, MockTestServer


def get_backend():
    return os.environ.get("ASGISH_SERVER", "mock").lower()


def set_backend_from_argv():
    for arg in sys.argv:
        if arg.upper().startswith("--ASGISH_SERVER="):
            os.environ["ASGISH_SERVER"] = arg.split("=")[1].strip().lower()


def run_tests(scope):
    for func in list(scope.values()):
        if callable(func) and func.__name__.startswith("test_"):
            print(f"Running {func.__name__} ...")
            func()
    print("Done")


def filter_lines(lines):
    # Overloadable line filter
    skip = (
        "Running on http",
        "Task was destroyed but",
        "task: <Task pending coro",
        "[INFO ",
    )
    return [line for line in lines if not line.startswith(skip)]


def make_server(app):
    servername = get_backend()
    if servername.lower() == "mock":
        server = MockTestServer(app)
    else:
        server = ProcessTestServer(app, servername)
    server.filter_lines = filter_lines
    return server