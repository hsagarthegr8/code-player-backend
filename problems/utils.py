import time
import subprocess


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        return result, te-ts
    return timed


@timeit
def run_code(filepath):
    runner = subprocess.run(
        args=['python', filepath], capture_output=True)
    return runner
