import os
import sys

MOBILE_AUTOMATION = "mobile_automation"
ESPRESSO = "espresso"
XCUITEST = "xcuitest"

if(len(sys.argv) < 2):
    print("Specify which test should be run")
    print(f"Example python statsCollector.py {MOBILE_AUTOMATION} / {ESPRESSO} / {XCUITEST}")

command = sys.argv[1]

if command == MOBILE_AUTOMATION:
    print("Running mobile automation tests")
elif comment == ESPRESSO:
    print("Running android espresso tests")
elif comment == XCUITEST:
    print("Running iOs xcuitest tests")


class MobileAutomation:

    def __init__(self, android=True):
        self.base_path = "../mobile_automation"
        self.platform = "android" if android else "ios"
        self.start_command = f'pytest --config="andrija-{self.platform}" --app="thesis_app" {self.base_path}/tests/'

    def runTest(self):
        print(f"Running command: {self.start_command}")
        result = os.system(self.start_command)
        print(result)

mb = MobileAutomation()
mb.runTest()
