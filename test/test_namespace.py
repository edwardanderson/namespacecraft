import pytest

from namespacecraft.namespace import Namespace


def test_base_namespace_printing():
    EX = Namespace('http://example.org/')
    assert str(EX) == 'http://example.org/'

def test_single_path_extension_with_int():
    EX = Namespace('http://example.org/')
    PART = EX / 'part'
    assert str(PART / 1) == 'http://example.org/part/1'

def test_fragment_addition():
    EX = Namespace('http://example.org/')
    PART = EX / 'part'
    assert str(PART / '1' + 'a') == 'http://example.org/part/1#a'

def test_multiple_path_extensions_then_fragment():
    EX = Namespace('http://example.org/')
    PART = EX / 'part'
    assert str(PART / 1 / 2 / 3 + 'a') == 'http://example.org/part/1/2/3#a'

def test_leading_delimiter_in_path():
    EX = Namespace('http://example.org/') / '/a'
    assert str(EX) == 'http://example.org/a'

def test_multiple_path_with_duplicate_path_delimiter():
    EX = Namespace('http://example.org/')
    assert str(EX / '/part') == 'http://example.org/part'

def test_multiple_path_from_list():
    EX = Namespace('http://example.org/') / [1, 2, 3]
    assert str(EX) == 'http://example.org/1/2/3'

def test_multiple_path_from_list_and_fragment():
    EX = Namespace('http://example.org/') / [1, 2, 3] + 'a'
    assert str(EX) == 'http://example.org/1/2/3#a'

def test_attribute():
    EX = Namespace('http://example.org/')
    assert EX.a == 'http://example.org/a'

    EX = Namespace('http://example.org#')
    assert EX.a == 'http://example.org#a'

def test_single_fragment_from_path():
    EX = Namespace('http://example.org#') / 'a'
    assert str(EX) == 'http://example.org#a'

# Expected errors

def test_only_one_fragment_allowed():
    EX = Namespace("http://example.org/")
    PART = EX / "part"

    # First fragment is fine
    first = PART + "a"
    assert first == "http://example.org/part#a"
    
    # The original Namespace can still be used to create another fragment
    second = PART + "b"
    assert second == "http://example.org/part#b"


def test_mismatched_delimiters_in_path():
    # Slash namespace cannot accept #
    EX_slash = Namespace("http://example.org/")
    with pytest.raises(ValueError):
        EX_slash / "#a"

    # Hash namespace cannot accept /
    EX_hash = Namespace("http://example.org#")
    with pytest.raises(ValueError):
        EX_hash / "/a"
