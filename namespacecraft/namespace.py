from __future__ import annotations
from typing import Type


class Term(str):
    """
    A terminal URI value.

    Subclasses `str` for seamless interoperability with libraries that
    expect string-like URI objects.
    """
    __slots__ = ()

    def __new__(cls, value: str):
        return super().__new__(cls, value)

    def __repr__(self) -> str:
        return f"Term({super().__repr__()})"


class Namespace:
    __slots__ = ('_base', '_hash', '_term_class')

    def __init__(self, base: str, *, term_class: Type = Term) -> None:
        base = str(base)

        if base.count('#') > 1:
            raise ValueError('A namespace may contain at most one fragment delimiter')

        # Determine if this is a hash namespace (ends with '#')
        self._hash = base.endswith('#')

        # Strip fragment delimiter from stored base
        if '#' in base:
            base, _ = base.split('#', 1)

        self._base = base
        self._term_class = term_class

    # Path-building operator (namespace-aware)
    def __truediv__(self, other: str | int | list | tuple) -> Namespace | Term:
        if isinstance(other, (list, tuple)):
            ns = self
            for part in other:
                ns = ns / part
            return ns

        other_str = str(other)

        if self._hash:
            # Hash namespaces cannot have hierarchical paths
            if '/' in other_str:
                raise ValueError('Cannot append hierarchical path to a hash namespace')
            # Hash namespace + path is terminal
            return self._term_class(f'{self._base}#{other_str}')

        if '#' in other_str:
            raise ValueError('Cannot append fragment-like string to a slash namespace')

        new_base = self._base.rstrip('/') + '/' + other_str.lstrip('/')
        return Namespace(new_base, term_class=self._term_class)

    # Terminal creation by concatenation
    def __add__(self, other: str) -> Term:
        """
        Create a terminal term by concatenating onto the namespace prefix.

        No delimiter semantics are inferred or enforced.
        """
        return self._term_class(str(self) + str(other))

    # Attribute access: terminal term
    def __getattr__(self, name: str) -> Term:
        if name.startswith('_'):
            raise AttributeError(f'{type(self).__name__} object has no attribute {name!r}')

        return self._term_class(str(self) + name)

    def __str__(self) -> str:
        return self._base + ('#' if self._hash else '')

    def __repr__(self) -> str:
        return f'Namespace({str(self)!r})'

    def __contains__(self, other: str | Namespace | Term) -> bool:
        return str(other).startswith(self._base)

    @property
    def uri(self) -> Term:
        """Return this namespace rendered as a terminal URI."""
        return self._term_class(str(self))
