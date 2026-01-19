import pytest
from namespacecraft import Namespace, Term


def test_is_str_subclass():
    term = Term('http://example.org/a')
    assert isinstance(term, str)
    assert isinstance(term, Term)


def test_is_not_namespace():
    term = Term('http://example.org/a')
    assert not isinstance(term, Namespace)


def test_repr():
    term = Term('http://example.org/a')
    assert repr(term) == "Term('http://example.org/a')"


def test_is_terminal_no_path_extension():
    term = Term('http://example.org/a')

    with pytest.raises(TypeError):
        term / 'b'


def test_has_no_attribute_namespace_semantics():
    term = Term('http://example.org/a')

    # Attribute access should behave like str, not Namespace
    with pytest.raises(AttributeError):
        _ = term.b

def test_relative_to_basic_slash():
    BASE = Namespace('http://example.org/api/')
    term = (BASE / 'users') + '123'
    assert term.relative_to(BASE) == 'users/123'


def test_relative_to_nested_slash():
    BASE = Namespace('http://example.org/api/')
    term = BASE / 'users/123/' + 'details'
    assert term.relative_to(BASE) == 'users/123/details'


def test_relative_to_hash_namespace():
    BASE = Namespace('http://example.org#')
    term = BASE / 'fragment1'
    assert term.relative_to(BASE) == 'fragment1'


def test_relative_to_hash_namespace():
    BASE = Namespace('http://example.org#')
    term = BASE / 'section'
    assert term.relative_to(BASE) == 'section'

    # Trying to add another path component should fail
    with pytest.raises(TypeError):
        term / 'subsection'


def test_relative_to_returns_error_if_not_relative():
    BASE = Namespace('http://example.org/api/')
    OTHER = Namespace('http://example.org/other/')
    term = BASE / 'users' + '123'
    with pytest.raises(ValueError):
        term.relative_to(OTHER)


def test_relative_to_slash_and_hash_combined():
    BASE_SLASH = Namespace('http://example.org/api/')
    BASE_HASH = Namespace('http://example.org/api#')
    term1 = BASE_SLASH / 'users' + '123'
    term2 = BASE_HASH / 'users123'
    
    assert term1.relative_to(BASE_SLASH) == 'users/123'
    assert term2.relative_to(BASE_HASH) == 'users123'


def test_relative_to_entire_namespace_returns_empty_string():
    BASE = Namespace('http://example.org/api/')
    term = Term(str(BASE))
    assert term.relative_to(BASE) == ''


def test_relative_to_with_non_namespace_raises_type_error():
    BASE = Namespace('http://example.org/api/')
    term = BASE / 'users'
    with pytest.raises(TypeError):
        term.relative_to('http://example.org/api/')
