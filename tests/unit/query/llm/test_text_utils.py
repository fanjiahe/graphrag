# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from graphrag.query.llm.text_utils import try_parse_json_object


def test_wrapped_json_keeps_backslash_escapes():
    text = 'Result: {"path": "C:\\\\temp", "note": "a\\nb"}'
    parsed_text, parsed = try_parse_json_object(text, verbose=False)

    assert parsed == {"path": "C:\\temp", "note": "a\nb"}
    assert "\\n" not in parsed["note"]
    assert parsed_text == '{"path": "C:\\\\temp", "note": "a\\nb"}'


def test_fenced_json_keeps_backslash_escapes():
    text = '```json\n{"name": "a\\nb"}\n```'
    _, parsed = try_parse_json_object(text, verbose=False)

    assert parsed == {"name": "a\nb"}


def test_whole_document_json_is_unchanged():
    text = '{"ok": true}'
    parsed_text, parsed = try_parse_json_object(text, verbose=False)

    assert parsed_text == text
    assert parsed == {"ok": True}


def test_doubled_braces_still_go_through_cleanup():
    _, parsed = try_parse_json_object('{{ "a": 1 }}', verbose=False)

    assert parsed == {"a": 1}
