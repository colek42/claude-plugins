import json
import os
import unittest

import organize
from organize import classify, window_key

# Tests run against rules.example.json, never the user's local rules.
_rules = json.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "rules.example.json")))
organize.APPS.clear(); organize.APPS.update(_rules["apps"])
organize.CHROME_DATA_DIRS.clear(); organize.CHROME_DATA_DIRS.update(_rules["chrome_data_dirs"])
organize.CHROME_PROFILES.clear(); organize.CHROME_PROFILES.update(_rules["chrome_profiles"])
organize.LAUNCHER_TITLES.clear(); organize.LAUNCHER_TITLES.update(_rules["launcher_titles"])
organize.ULTRAWIDE = _rules["ultrawide"]
organize.PROMPTER = _rules["prompter"]

CHROME = "com.google.Chrome"
MAIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
AGENT = MAIN + " --user-data-dir=/Users/me/Library/Application Support/Google/ChromeAgent --remote-debugging-port=9222"
WORK = "/usr/bin/arch -arm64 " + MAIN + " --user-data-dir=/Users/me/Library/Application Support/Google/ChromeWork --no-first-run"


class Classify(unittest.TestCase):
    def test_comms_apps_go_to_laptop(self):
        self.assertEqual(classify("us.zoom.xos", "", "Zoom Meeting"), "M")
        self.assertEqual(classify("com.tinyspeck.slackmacgap", "", "x - Slack"), "M")

    def test_meet_tab_goes_to_laptop(self):
        self.assertEqual(classify(CHROME, MAIN, "Meet - abc-defg-hij - Google Chrome - Cole"), "M")

    def test_calendar_pinned_to_laptop(self):
        self.assertEqual(classify(CHROME, MAIN, "Google Calendar - Thursday, October 29, 2026"), "M")
        self.assertEqual(window_key(CHROME, MAIN, "testifysec - Calendar - Thursday, October 29, 2026, today - Cole"), "chrome:calendar")

    def test_teams_call_in_pinned_instance_goes_to_laptop(self):
        # Teams web in a pinned Chrome instance must beat the instance rule.
        self.assertEqual(classify(CHROME, WORK, "Weekly sync | Microsoft Teams - Google Chrome"), "M")
        self.assertEqual(classify(CHROME, WORK, "Chat | Microsoft Teams - Google Chrome"), "M")
        self.assertEqual(classify(CHROME, MAIN, "Cisco Webex Meetings - Google Chrome - Cole"), "M")
        self.assertEqual(classify(CHROME, MAIN, "Zoom Meeting - Google Chrome - Cole"), "M")

    def test_chrome_profiles(self):
        # Work Chrome follows the session you're in; only personal is pinned.
        self.assertIsNone(classify(CHROME, MAIN, "Feed | LinkedIn - Google Chrome - Cole"))
        self.assertEqual(classify(CHROME, MAIN, "Inbox - Google Chrome - Family"), "P")

    def test_chrome_instances_by_user_data_dir(self):
        # Same title shape, different instance: only the command line tells them apart.
        self.assertIsNone(classify(CHROME, AGENT, "Vuln Index Hosting Design - Google Chrome"))
        self.assertEqual(classify(CHROME, WORK, "Portal - Google Chrome"), "N")
        self.assertEqual(window_key(CHROME, AGENT, "x - Google Chrome"), "chrome:ChromeAgent")

    def test_session_apps_stay_where_opened(self):
        self.assertIsNone(classify("com.mitchellh.ghostty", "", "zsh"))
        self.assertIsNone(classify("com.microsoft.VSCode", "", "x"))

    def test_windows_app_launcher_parked_desktop_stays(self):
        self.assertEqual(classify("com.microsoft.rdc.macos", "", "Windows App"), "N")
        self.assertIsNone(classify("com.microsoft.rdc.macos", "", "Remote Desktop-14"))

    def test_unknown_left_alone(self):
        self.assertIsNone(classify("com.apple.finder", "", "Downloads"))


class ActiveWindowIsUntouchable(unittest.TestCase):
    # Cole: "if you don't disturb the active window, you can move around the
    # windows that are not active."
    def test_window_in_use_gets_a_suggestion(self):
        from organize import call_transition
        self.assertEqual(call_transition("319", focused="319"), "suggest")

    def test_background_window_just_moves(self):
        from organize import call_transition
        self.assertEqual(call_transition("319", focused="285"), "move")


class CallScreen(unittest.TestCase):
    def test_calls_go_to_prompter_when_it_is_connected(self):
        from organize import call_workspace
        self.assertEqual(call_workspace(["ULTRA", "Built-in Retina Display", "PROMPTER"]), "T")
        self.assertEqual(call_workspace(["ULTRA", "Built-in Retina Display"]), "M")


class Plan(unittest.TestCase):
    """Ultrawide = 1280 | 2560 | 1280. Ghostty takes the center, empty side columns are margin."""

    def setUp(self):
        from organize import plan
        self.plan = plan

    def test_lone_window_centered(self):
        self.assertEqual(self.plan(1, False), (1280, 1280, []))
        self.assertEqual(self.plan(1, True), (1280, 1280, []))

    def test_two_windows_use_the_whole_screen(self):
        # No empty columns once there is more than one window (Cole: "useless space").
        self.assertEqual(self.plan(2, True), (8, 8, ["left"]))

    def test_three_windows_ghostty_in_middle(self):
        # Push to the left edge from any position, then one step right.
        self.assertEqual(self.plan(3, True), (8, 8, ["left", "left", "right"]))

    def test_no_ghostty_never_full_width(self):
        self.assertEqual(self.plan(2, False), (8, 8, []))
        self.assertEqual(self.plan(3, False), (8, 8, []))

    def test_set_margins_rewrites_only_ultrawide_side_gaps(self):
        from organize import set_margins
        cfg = ("outer.left = [{ monitor.'ULTRA' = 640 }, 8]\n"
               "outer.right = [{ monitor.'ULTRA' = 640 }, 8]\n"
               "outer.top = 8\n")
        out = set_margins(cfg, 8, 1280)
        self.assertIn("outer.left = [{ monitor.'ULTRA' = 8 }, 8]", out)
        self.assertIn("outer.right = [{ monitor.'ULTRA' = 1280 }, 8]", out)
        self.assertIn("outer.top = 8", out)


if __name__ == "__main__":
    unittest.main()
