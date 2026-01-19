import pytest

from namespacecraft.namespace import Namespace, Term


def test_namespace_as_str():
    EX = Namespace('http://example.org/')
    assert str(EX) == 'http://example.org/'


def test_namespace_coerce_int_to_str():
    EX = Namespace('http://example.org/')
    PART = EX / 'part'
    assert str(PART / 1) == 'http://example.org/part/1'


def test_namespace_create_term_by_addition():
    EX = Namespace('http://example.org/')
    assert EX / 'a/b/c/' + 'a' == 'http://example.org/a/b/c/a'
    assert EX / 'x/y' + 'z' == 'http://example.org/x/yz'


def test_namespace_deduplicates_delimiter_in_path():
    EX = Namespace('http://example.org/') / '/a'
    assert str(EX) == 'http://example.org/a'


def test_namespace_paths_from_list():
    EX = Namespace('http://example.org/') / [1, 2, 3]
    assert str(EX) == 'http://example.org/1/2/3'


def test_namespace_paths_from_list_and_create_term():
    EX = Namespace('http://example.org/') / [1, 2, 3] + '/a'
    assert str(EX) == 'http://example.org/1/2/3/a'


def test_namespace_create_term_from_attribute():
    EX = Namespace('http://example.org/')
    a = EX.a
    assert str(a) == 'http://example.org/a'
    assert isinstance(a, Term)

    EX = Namespace('http://example.org#')
    b = EX.b
    assert str(b) == 'http://example.org#b'
    assert isinstance(b, Term)


def test_namespace_create_path_with_hash_delimiter():
    EX = Namespace('http://example.org#') / 'a'
    assert str(EX) == 'http://example.org#a'

# Expected errors

def test_only_one_fragment_allowed():
    EX = Namespace('http://example.org#')
    
    # First fragment is fine
    assert EX + 'a' == 'http://example.org#a'
    
    # The original Namespace can still be used to create another fragment
    assert EX + 'b' == 'http://example.org#b'


def test_mismatched_delimiters_in_path():
    # Slash namespace cannot accept #
    EX_slash = Namespace('http://example.org/')
    with pytest.raises(ValueError):
        EX_slash / '#a'

    # Hash namespace cannot accept /
    EX_hash = Namespace('http://example.org#')
    with pytest.raises(ValueError):
        EX_hash / '/a'


def test_namespace_hash_delimiter_is_terminal():
    EX = Namespace('http://example.org#')

    # First / returns a terminal object
    term = EX / 'a'
    assert term == 'http://example.org#a'

    # Further / calls are invalid (TypeError)
    with pytest.raises(TypeError):
        term / 'b'


def test_namespace_add_returns_term():
    EX = Namespace('http://example.org/')
    term = EX + 'a'

    assert isinstance(term, Term)
    assert term == 'http://example.org/a'


def test_namespace_dot_returns_term():
    EX = Namespace('http://example.org/')
    term = EX.a

    assert isinstance(term, Term)
    assert term == 'http://example.org/a'


def test_namespace_uri_property_returns_term():
    EX = Namespace('http://example.org/')
    term = EX.uri

    assert isinstance(term, Term)
    assert term == 'http://example.org/'


def test_term_is_str_subclass():
    term = Term('http://example.org/a')
    assert isinstance(term, str)
    assert isinstance(term, Term)


def test_term_is_not_namespace():
    term = Term('http://example.org/a')
    assert not isinstance(term, Namespace)


def test_term_repr():
    term = Term('http://example.org/a')
    assert repr(term) == "Term('http://example.org/a')"


def test_term_is_terminal_no_path_extension():
    term = Term('http://example.org/a')

    with pytest.raises(TypeError):
        term / 'b'


def test_term_has_no_attribute_namespace_semantics():
    term = Term('http://example.org/a')

    # Attribute access should behave like str, not Namespace
    with pytest.raises(AttributeError):
        _ = term.b
