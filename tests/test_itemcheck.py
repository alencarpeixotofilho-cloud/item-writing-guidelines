import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from itemcheck import check, parse_file, parse_item  # noqa: E402
from itemcheck.cli import main  # noqa: E402

EX = ROOT / "examples"


def rules_of(item):
    return {f.rule for f in check(item)}


def by_id(path):
    return {i.id: i for i in parse_file(path)}


def test_parser_reads_all_sections():
    items = parse_file(EX / "good_items.md")
    assert len(items) == 2
    it = items[0]
    assert it.id == "GOOD-001" and it.key == "D"
    assert set(it.options) == set("ABCDE")
    assert it.lead_in.endswith("?")


def test_good_items_have_no_warnings():
    for it in parse_file(EX / "good_items.md"):
        sev = {f.severity for f in check(it)}
        assert "error" not in sev and "warning" not in sev, check(it)


def test_flawed_001():
    r = rules_of(by_id(EX / "flawed_items.md")["FLAWED-001"])
    assert {"NEGATIVE_LEAD_IN", "ALL_NONE_OF_THE_ABOVE", "ABSOLUTE_TERM",
            "LONGEST_KEY", "SHORT_STEM"} <= r


def test_flawed_002_grammatical_cue():
    r = rules_of(by_id(EX / "flawed_items.md")["FLAWED-002"])
    assert "GRAMMATICAL_CUE" in r and "OPEN_LEAD_IN" in r


def test_flawed_003_numeric_order():
    r = rules_of(by_id(EX / "flawed_items.md")["FLAWED-003"])
    assert "NUMERIC_ORDER" in r


def test_key_not_in_options_is_error():
    it = parse_item("## Stem\nx\n## Lead-in\nWhich?\n## Options\nA. a\nB. b\nC. c\n## Key\nE\n")
    assert any(f.rule == "KEY" and f.severity == "error" for f in check(it))


def test_cli_exit_codes(capsys):
    assert main([str(EX / "good_items.md")]) == 0
    assert main([str(EX / "flawed_items.md"), "--fail-on", "warning"]) == 1
