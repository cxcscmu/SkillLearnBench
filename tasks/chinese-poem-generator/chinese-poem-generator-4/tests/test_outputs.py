from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from pypinyin import Style, pinyin


POEM_FILE = Path("/root/poem.txt")


QILV_PATTERNS: Dict[str, Dict[str, object]] = {
    "Ping-start Ze-end no-rhyme-on-line-1": {
        "rhyme_lines": [2, 4, 6, 8],
        "patterns": [
            "平平仄仄平平仄",
            "仄仄平平仄仄平",
            "仄仄平平平仄仄",
            "平平仄仄仄平平",
            "平平仄仄平平仄",
            "仄仄平平仄仄平",
            "仄仄平平平仄仄",
            "平平仄仄仄平平",
        ],
    },
    "Ze-start Ze-end no-rhyme-on-line-1": {
        "rhyme_lines": [2, 4, 6, 8],
        "patterns": [
            "仄仄平平平仄仄",
            "平平仄仄仄平平",
            "平平仄仄平平仄",
            "仄仄平平仄仄平",
            "仄仄平平平仄仄",
            "平平仄仄仄平平",
            "平平仄仄平平仄",
            "仄仄平平仄仄平",
        ],
    },
    "Ze-start Ping-end rhyme-on-line-1": {
        "rhyme_lines": [1, 2, 4, 6, 8],
        "patterns": [
            "仄仄平平仄仄平",
            "平平仄仄仄平平",
            "平平仄仄平平仄",
            "仄仄平平仄仄平",
            "仄仄平平平仄仄",
            "平平仄仄仄平平",
            "平平仄仄平平仄",
            "仄仄平平仄仄平",
        ],
    },
    "Ping-start Ping-end rhyme-on-line-1": {
        "rhyme_lines": [1, 2, 4, 6, 8],
        "patterns": [
            "平平仄仄仄平平",
            "仄仄平平仄仄平",
            "仄仄平平平仄仄",
            "平平仄仄仄平平",
            "平平仄仄平平仄",
            "仄仄平平仄仄平",
            "仄仄平平平仄仄",
            "平平仄仄仄平平",
        ],
    },
}


def load_poem_text(path: Path) -> str:
    """Load the poem document from a UTF-8 text file."""
    return path.read_text(encoding="utf-8").strip()


def parse_poem_document(text: str) -> Tuple[str, List[str]]:
    """
    Parse the poem document.

    Rules:
    - the first non-empty line is treated as the title
    - the remaining non-empty lines are treated as poem body lines
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return "", []
    title = lines[0]
    body_lines = lines[1:]
    return title, body_lines


def chinese_chars(text: str) -> List[str]:
    """Extract Chinese characters only."""
    return re.findall(r"[\u4e00-\u9fff]", text)


def _heteronym_tone3(ch: str) -> List[str]:
    """Return all possible tone3 syllables for a character."""
    result = pinyin(
        ch,
        style=Style.TONE3,
        heteronym=True,
        strict=False,
        errors="ignore",
    )
    if not result:
        return []
    return list(dict.fromkeys(result[0]))


def _heteronym_finals_tone3(ch: str) -> List[str]:
    """Return all possible finals+tone for a character."""
    result = pinyin(
        ch,
        style=Style.FINALS_TONE3,
        heteronym=True,
        strict=False,
        errors="ignore",
    )
    if not result:
        return []
    return list(dict.fromkeys(result[0]))


def tone_options(ch: str) -> Set[str]:
    """
    Return all usable 平/仄 options under modern Mandarin rules.

    Rules:
    - 1/2 -> 平
    - 3/4 -> 仄
    - neutral tone is ignored
    - if there is any non-neutral reading, only non-neutral readings are used
    - if there is no usable non-neutral reading, return an empty set
    """
    options: Set[str] = set()

    for syllable in _heteronym_tone3(ch):
        match = re.search(r"([1-4])$", syllable)
        if not match:
            continue
        tone = int(match.group(1))
        if tone in (1, 2):
            options.add("平")
        elif tone in (3, 4):
            options.add("仄")

    return options


def normalize_final(final_with_tone: str) -> Optional[str]:
    """Normalize a final+tone string to a plain final without tone."""
    match = re.match(r"([a-züv]+)([1-4])$", final_with_tone)
    if not match:
        return None
    final = match.group(1)
    final = final.replace("ü", "v")
    return final


def final_options(ch: str) -> Set[str]:
    """
    Return all usable non-neutral finals for a character.

    Neutral readings are ignored.
    If no usable non-neutral reading exists, return an empty set.
    """
    options: Set[str] = set()

    for item in _heteronym_finals_tone3(ch):
        final = normalize_final(item)
        if final:
            options.add(final)

    return options


def rhyme_family(final: str) -> str:
    """
    Map a modern Mandarin final to a broader rhyme family.

    This is intentionally broader than exact-final matching.
    It merges common medial variants into one family, such as:
    - ang / iang / uang -> ang
    - an / ian / uan / van -> an
    - ao / iao -> ao
    - ai / uai -> ai
    - ei / ui -> ei
    - ou / iu -> ou
    - ong / iong -> ong

    Finals not listed below fall back to themselves.
    """
    family_map = {
        "a": "a",
        "ia": "a",
        "ua": "a",

        "o": "o",
        "uo": "o",
        "e": "e",
        "ie": "e",
        "ve": "e",

        "ai": "ai",
        "uai": "ai",

        "ei": "ei",
        "ui": "ei",

        "ao": "ao",
        "iao": "ao",

        "ou": "ou",
        "iu": "ou",

        "an": "an",
        "ian": "an",
        "uan": "an",
        "van": "an",

        "en": "en",
        "in": "en",
        "un": "en",
        "vn": "en",

        "ang": "ang",
        "iang": "ang",
        "uang": "ang",

        "eng": "eng",
        "ueng": "eng",

        "ong": "ong",
        "iong": "ong",

        "er": "er",
    }
    return family_map.get(final, final)


def rhyme_family_options(ch: str) -> Set[str]:
    """
    Return all usable rhyme families for a character.
    Neutral readings are ignored through final_options().
    """
    return {rhyme_family(f) for f in final_options(ch)}


def match_line_to_pattern(line: str, pattern: str) -> Tuple[bool, List[int]]:
    """
    Check whether one 7-character line matches one strict 平仄 pattern.

    Returns:
    - ok: whether the line matches
    - skipped_positions: 1-based positions skipped because no usable non-neutral reading exists
    """
    chars = chinese_chars(line)
    if len(chars) != 7:
        return False, []

    skipped_positions: List[int] = []

    for idx, (ch, expected) in enumerate(zip(chars, pattern), start=1):
        options = tone_options(ch)

        if not options:
            skipped_positions.append(idx)
            continue

        if expected not in options:
            return False, skipped_positions

    return True, skipped_positions


def rhyme_group_ok(lines: List[str], rhyme_lines: List[int]) -> bool:
    """
    Check whether all required rhyme lines share at least one common rhyme family.

    Required rhyme positions must have usable non-neutral finals.
    Exact-final matching is intentionally relaxed to rhyme-family matching.
    """
    ending_sets: List[Set[str]] = []

    for line_no in rhyme_lines:
        chars = chinese_chars(lines[line_no - 1])
        if len(chars) != 7:
            return False

        options = rhyme_family_options(chars[-1])
        if not options:
            return False

        ending_sets.append(options)

    if not ending_sets:
        return False

    common = set.intersection(*ending_sets)
    return bool(common)


def analyze_qilv_lines(lines: List[str]) -> Dict[str, object]:
    """
    Analyze whether the poem body matches one of the four strict Qilv forms.

    The title must already be removed before calling this function.
    """
    result: Dict[str, object] = {
        "ok": False,
        "matched_form": None,
        "details": {},
    }

    if len(lines) != 8:
        result["details"] = {
            "error": f"Expected 8 body lines, got {len(lines)}."
        }
        return result

    for idx, line in enumerate(lines, start=1):
        count = len(chinese_chars(line))
        if count != 7:
            result["details"] = {
                "error": f"Body line {idx} must have 7 Chinese characters, got {count}.",
                "line": line,
            }
            return result

    candidates = []

    for form_name, spec in QILV_PATTERNS.items():
        patterns = spec["patterns"]
        rhyme_lines = spec["rhyme_lines"]

        assert isinstance(patterns, list)
        assert isinstance(rhyme_lines, list)

        line_reports = []
        pattern_ok = True
        total_skips = 0

        for idx, (line, pattern) in enumerate(zip(lines, patterns), start=1):
            ok, skipped = match_line_to_pattern(line, pattern)
            total_skips += len(skipped)

            line_reports.append(
                {
                    "line_no": idx,
                    "line": line,
                    "pattern": pattern,
                    "ok": ok,
                    "skipped_positions": skipped,
                }
            )

            if not ok:
                pattern_ok = False

        rhyme_ok = rhyme_group_ok(lines, rhyme_lines)

        candidates.append(
            {
                "form": form_name,
                "pattern_ok": pattern_ok,
                "rhyme_ok": rhyme_ok,
                "total_skips": total_skips,
                "rhyme_lines": rhyme_lines,
                "line_reports": line_reports,
            }
        )

    matched = [c for c in candidates if c["pattern_ok"] and c["rhyme_ok"]]

    if matched:
        matched.sort(key=lambda item: item["total_skips"])
        best = matched[0]
        result["ok"] = True
        result["matched_form"] = best["form"]
        result["details"] = best
        return result

    result["details"] = {"candidates": candidates}
    return result


def format_failure_report(result: Dict[str, object]) -> str:
    """Format a readable failure report for pytest output."""
    details = result.get("details", {})

    if isinstance(details, dict) and "error" in details:
        return str(details["error"])

    if not isinstance(details, dict):
        return repr(result)

    candidates = details.get("candidates", [])
    if not candidates:
        return repr(result)

    lines = ["No strict Qilv form matched."]

    for cand in candidates:
        lines.append(f"\nForm: {cand['form']}")
        lines.append(f"  pattern_ok = {cand['pattern_ok']}")
        lines.append(f"  rhyme_ok   = {cand['rhyme_ok']}")
        lines.append(f"  total_skips = {cand['total_skips']}")

        for report in cand["line_reports"]:
            if not report["ok"]:
                lines.append(
                    f"  Line {report['line_no']} failed: {report['line']} | expected {report['pattern']}"
                )
            elif report["skipped_positions"]:
                lines.append(
                    f"  Line {report['line_no']} skipped positions: {report['skipped_positions']}"
                )

    return "\n".join(lines)


def test_poem_file_exists():
    assert POEM_FILE.exists(), f"Poem file not found: {POEM_FILE}"


def test_poem_has_title():
    text = load_poem_text(POEM_FILE)
    title, _ = parse_poem_document(text)
    assert title, "The poem document must include a non-empty title on the first non-empty line."


def test_qilv_has_8_body_lines():
    text = load_poem_text(POEM_FILE)
    _, body_lines = parse_poem_document(text)
    assert len(body_lines) == 8, f"Expected 8 body lines after the title, got {len(body_lines)}."


def test_each_body_line_has_7_chinese_characters():
    text = load_poem_text(POEM_FILE)
    _, body_lines = parse_poem_document(text)

    bad_lines = []
    for idx, line in enumerate(body_lines, start=1):
        count = len(chinese_chars(line))
        if count != 7:
            bad_lines.append(f"Body line {idx}: {count} chars | {line}")

    assert not bad_lines, "Some body lines do not have 7 Chinese characters:\n" + "\n".join(bad_lines)


def test_poem_body_matches_one_strict_qilv_form():
    text = load_poem_text(POEM_FILE)
    _, body_lines = parse_poem_document(text)
    result = analyze_qilv_lines(body_lines)
    assert result["ok"], format_failure_report(result)


def test_report_matched_form_when_successful():
    text = load_poem_text(POEM_FILE)
    _, body_lines = parse_poem_document(text)
    result = analyze_qilv_lines(body_lines)

    if result["ok"]:
        assert result["matched_form"] in QILV_PATTERNS