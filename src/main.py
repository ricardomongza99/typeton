from semantic import run_tests, Cube
from virtual import run_tests as run_memory


def run_semantic_tests():
    semantic = Cube()
    run_tests(semantic)


if __name__ == '__main__':
    run_semantic_tests()
    run_memory()
