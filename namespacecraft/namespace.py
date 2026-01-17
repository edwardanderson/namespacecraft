from __future__ import annotations
from typing import Type


class Namespace:
    __slots__ = ('_base', '_hash', '_term_class')

    def __init__(self, base: str, *, term_class: Type = str) -> None:
        base = str(base)

        if base.count('#') > 1:
            raise ValueError('A namespace may contain at most one fragment delimiter')

        # Determine if this is a hash namespace (ends with '#')
        self._hash = base.endswith('#')

        # Remove fragment if present; base becomes everything before '#'
        if '#' in base:
            base, _ = base.split('#', 1)

        self._base = base
        self._term_class = term_class

    # Path-building operator
    def __truediv__(self, other: str | int | list | tuple) -> Namespace:
        if isinstance(other, (list, tuple)):
            ns = self
            for part in other:
                ns = ns / part
            return ns

        other_str = str(other)

        if self._hash:
            if '/' in other_str:
                raise ValueError('Cannot append hierarchical path to a hash namespace')
            # Terminal: return term_class immediately
            return self._term_class(f'{self._base}#{other_str}')

        if '#' in other_str:
            raise ValueError('Cannot append fragment-like string to a slash namespace')

        # Compose new slash base
        new_base = self._base.rstrip('/') + '/' + other_str.lstrip('/')
        return Namespace(new_base, term_class=self._term_class)


    # Fragment assignment: terminal operation
    def __add__(self, other: str):
        fragment = str(other)
        # Compose URI with fragment
        if self._hash:
            full_uri = f'{self._base}#{fragment}'
        else:
            full_uri = f'{self._base.rstrip('/')}#{fragment}'
        return self._term_class(full_uri)

    # Dot-access for terminal term
    def __getattr__(self, name: str):
        if name.startswith('_'):
            raise AttributeError(f'{type(self).__name__} object has no attribute {name!r}')

        if self._hash:
            term = f'{self._base}#{name}'
        else:
            term = f'{self._base.rstrip('/')}/{name.lstrip('/')}'
        return self._term_class(term)

    # String representation
    def __str__(self) -> str:
        return self._base + ('#' if self._hash else '')

    def __repr__(self) -> str:
        return f'Namespace({str(self)!r})'

    # Membership test
    def __contains__(self, other: str | Namespace) -> bool:
        other_str = str(other)
        return other_str.startswith(self._base)
