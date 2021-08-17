import re
from stats.base_stat import BaseStat


class XCUITest(BaseStat):

    def __init__(self):
        super().__init__()
        self.start_command = 'fastlane scan --scheme ../thesis-ios/thesis-iosUITests --project ../thesis-ios/thesis-ios.xcodeproj'
        self.encoding = 'utf-8'

    def extract_data_from_result(self, result):
        pattern = re.compile(r"Executed\s(\d)\stests,\swith\s(\d)\sfailures")
        match = re.search(pattern, result)
        all_test_cases = int(match.group(1))
        failed_test_cases = int(match.group(2))
        self.all_cases += all_test_cases
        self.failed_cases += failed_test_cases
