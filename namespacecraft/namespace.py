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
    __slots__ = ('_base', '_hash', '_term_class', '_trailing_delim', '_last_component_has_delimiter')

    def __init__(self, base: str, *, term_class: Type = Term, trailing_delim: str = '/', last_component_has_delimiter: bool = False) -> None:
        base = str(base)

        if base.count('#') > 1:
            raise ValueError("A namespace may contain at most one fragment delimiter")

        self._hash = base.endswith('#')

        # Remove any embedded fragment; we keep only the base
        if '#' in base:
            base, _ = base.split('#', 1)

        self._base = base
        self._term_class = term_class
        self._trailing_delim = trailing_delim
        self._last_component_has_delimiter = last_component_has_delimiter

    # Path-building operator
    def __truediv__(self, other: str | int | list | tuple) -> "Namespace":
        if isinstance(other, (list, tuple)):
            ns = self
            for part in other:
                ns = ns / part
            return ns

        other_str = str(other)

        if self._hash:
            if '/' in other_str:
                raise ValueError("Cannot append hierarchical path to a hash namespace")
            return self._term_class(f"{self._base}#{other_str}")

        if '#' in other_str:
            raise ValueError("Cannot append fragment-like string to a slash namespace")

        new_base = self._base.rstrip(self._trailing_delim) + self._trailing_delim + other_str.lstrip(self._trailing_delim)
        return Namespace(new_base, term_class=self._term_class, trailing_delim=self._trailing_delim, last_component_has_delimiter=self._trailing_delim in other_str)

    # Addition creates a terminal
    def __add__(self, other: str):
        other_str = str(other)
        base_str = str(self)

        if self._hash:
            return self._term_class(f"{self._base}#{other_str}")
        else:
            # For slash namespace
            # Strip leading delimiter from other if base already ends with it
            if base_str.endswith(self._trailing_delim) and other_str.startswith(self._trailing_delim):
                other_str = other_str.lstrip(self._trailing_delim)
                return self._term_class(base_str + other_str)
            elif base_str.endswith(self._trailing_delim):
                # Base already ends with delimiter, just concatenate
                return self._term_class(base_str + other_str)
            elif self._last_component_has_delimiter:
                # Last component added via / contained delimiter, so just concatenate
                return self._term_class(base_str + other_str)
            else:
                # Last component was simple, add delimiter before new component (unless other starts with it)
                if other_str.startswith(self._trailing_delim):
                    return self._term_class(base_str + other_str)
                else:
                    return self._term_class(base_str + self._trailing_delim + other_str)

    # Dot-access creates a terminal
    def __getattr__(self, name: str):
        if name.startswith('_'):
            raise AttributeError(f"{type(self).__name__} object has no attribute {name!r}")

        if self._hash:
            term_str = f"{self._base}#{name}"
        else:
            term_str = f"{self._base.rstrip('/')}/{name}"

        return self._term_class(term_str)

    # String representation
    def __str__(self) -> str:
        return self._base + ('#' if self._hash else '')

    def __repr__(self) -> str:
        return f"Namespace({str(self)!r})"

    # Membership test
    def __contains__(self, other: str | "Namespace") -> bool:
        return str(other).startswith(self._base)

    @property
    def uri(self):
        """Return this namespace as a terminal URI (_term_class instance)."""
        return self._term_class(str(self))

    def terminates_with(self, character: str) -> Namespace:
        """Return a new Namespace guaranteed to end with the given delimiter."""
        if not character:
            raise ValueError("character must be a non-empty string")

        if self._hash:
            return self  # hash namespaces ignore trailing delimiters

        if self._base.endswith(character):
            return self

        return Namespace(self._base + character, term_class=self._term_class, trailing_delim=character, last_component_has_delimiter=self._last_component_has_delimiter)
