from smartdiff import core
from pathlib import Path

if __name__ == '__main__':
    core.is_func_changed(Path().cwd() / "tests" / "example.py", "foo2")

