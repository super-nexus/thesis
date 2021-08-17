import sys
import numpy as np
from stats.mobile_automation import MobileAutomation
from stats.espresso import Espresso
from stats.xcuitest import XCUITest

MOBILE_AUTOMATION = "mobile_automation"
ESPRESSO = "espresso"
XCUITEST = "xcuitest"

TESTING_ITERATIONS = 20


def run_tests(t):
    for i in range(TESTING_ITERATIONS):
        t.run_test()
    print("Test results: ")
    print(f"Average time: {np.average(t.run_results)}")
    print(f"Median time: {np.median(t.run_results)}")
    print(f"Total time: {np.sum(t.run_results)}")
    print(f"All test cases: {t.all_cases}")
    print(f"Failed test cases: {t.failed_cases}")
    print(f"Fail rate: {t.failed_cases / t.all_cases}")


def get_platform():
    if len(sys.argv) < 3:
        print("No platform defined taking android as default")
        return True
    return sys.argv[2] == "android"


if len(sys.argv) < 2:
    print("Specify which test should be run")
    print(f"Example python statsCollector.py {MOBILE_AUTOMATION} / {ESPRESSO} / {XCUITEST}")

command = sys.argv[1]
test_class = None

if command == MOBILE_AUTOMATION:
    print("Running mobile automation tests")
    is_android = get_platform()
    test_class = MobileAutomation(android=is_android)
elif command == ESPRESSO:
    print("Running android espresso tests")
    test_class = Espresso()
elif command == XCUITEST:
    print("Running iOs xcuitest tests")
    test_class = XCUITest()


run_tests(test_class)
