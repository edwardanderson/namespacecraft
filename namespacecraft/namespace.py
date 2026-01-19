from __future__ import annotations
from typing import Type


class Term(str):
    """A terminal URI value"""
    __slots__ = ()

    def __new__(cls, value: str):
        return super().__new__(cls, value)

    def __repr__(self) -> str:
        return f'Term({super().__repr__()})'


class Namespace:
    __slots__ = ('_base', '_hash', '_term_class', '_trailing_delim', '_last_has_delim')

    def __init__(self, base: str, *, term_cls: Type = Term, _trailing_delim: str = '/', _last_has_delim: bool = False) -> None:
        base = str(base)

        if base.count('#') > 1:
            raise ValueError('A namespace may contain at most one fragment delimiter')

        self._hash = base.endswith('#')

        # Remove embedded fragment; only keep base
        if '#' in base:
            base, _ = base.split('#', 1)

        self._base = base
        self._term_class = term_cls
        self._trailing_delim = _trailing_delim
        self._last_has_delim = _last_has_delim

    def __truediv__(self, other: str | int | list | tuple) -> Namespace:
        """Build a Namespace() like a path"""
        if isinstance(other, (list, tuple)):
            ns = self
            for part in other:
                ns = ns / part
            return ns

        other_str = str(other)

        if self._hash:
            if '/' in other_str:
                raise ValueError('Cannot append hierarchical path to a hash namespace')
            return self._term_class(f'{self._base}#{other_str}')

        if '#' in other_str:
            raise ValueError('Cannot append fragment-like string to a slash namespace')

        # Compose new base respecting _trailing_delim
        new_base = self._base.rstrip(self._trailing_delim) + self._trailing_delim + other_str.lstrip(self._trailing_delim)
        return Namespace(new_base, term_cls=self._term_class, _trailing_delim=self._trailing_delim, _last_has_delim=self._trailing_delim in other_str)

    def __add__(self, other: str):
        """Create a Term() by adding a value"""
        other_str = str(other)
        if self._hash:
            return self._term_class(f'{self._base}#{other_str}')
        # Slash namespace
        base_str = str(self)
        # If last component had delimiter, just concatenate
        if self._last_has_delim:
            return self._term_class(base_str + other_str)
        # If base doesn't end with delimiter and other doesn't start with it, add delimiter
        if not base_str.endswith(self._trailing_delim) and not other_str.startswith(self._trailing_delim):
            return self._term_class(base_str + self._trailing_delim + other_str)
        # If both have delimiter, strip from other
        elif base_str.endswith(self._trailing_delim) and other_str.startswith(self._trailing_delim):
            return self._term_class(base_str + other_str.lstrip(self._trailing_delim))
        # Otherwise just concatenate
        else:
            return self._term_class(base_str + other_str)

    def __getattr__(self, name: str):
        """Create a Term() by accessing an attribute"""
        if name.startswith('_'):
            raise AttributeError(f'{type(self).__name__} object has no attribute {name!r}')

        if self._hash:
            term_str = f'{self._base}#{name}'
        else:
            term_str = f'{self._base.rstrip('/')}/{name}'

        return self._term_class(term_str)

    def __getitem__(self, key: str):
        """Create a Term() by accessing an attribute by name"""
        return self.__getattr__(str(key))

    def __str__(self) -> str:
        return self._base + ('#' if self._hash else '')

    def __repr__(self) -> str:
        return f'Namespace({str(self)!r})'

    def __contains__(self, other: str | Namespace) -> bool:
        return str(other).startswith(self._base)

    @property
    def uri(self):
        """Return this namespace as a terminal URI (_term_class instance)."""
        return self._term_class(str(self))

    def terminates_with(self, character: str) -> Namespace:
        """Return a new Namespace guaranteed to end with the given delimiter."""
        if not character:
            raise ValueError('character must be a non-empty string')

        if self._hash:
            return self  # hash namespaces ignore trailing delimiters

        if self._base.endswith(character):
            return self

        return Namespace(self._base + character, term_cls=self._term_class, _trailing_delim=character, _last_has_delim=self._last_has_delim)
