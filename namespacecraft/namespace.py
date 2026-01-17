from __future__ import annotations
from typing import Type


class Namespace:
    __slots__ = ('_base', '_fragment', '_hash', '_term_class')

    def __init__(self, base: str, fragment: str | None = None, *, term_class: Type = str) -> None:
        base = str(base)

        # Count hash delimiters
        if base.count('#') > 1:
            raise ValueError('A namespace may contain at most one fragment delimiter')

        # Determine hash vs slash namespace
        self._hash = base.endswith('#')

        # Split existing fragment if present
        if '#' in base:
            base, existing_fragment = base.split('#', 1)
            if fragment is not None:
                raise ValueError('Fragment specified twice')
            fragment = existing_fragment or None

        self._base = base
        self._fragment = fragment
        self._term_class = term_class

    # Path-building operator
    def __truediv__(self, other: str | int | list | tuple) -> Namespace:
        # Coerce lists/tuples recursively
        if isinstance(other, (list, tuple)):
            ns = self
            for part in other:
                ns = ns / part
            return ns

        other = str(other)

        if self._fragment is not None:
            raise ValueError("Cannot extend a namespace that already has a fragment")

        # Mismatched delimiter check
        if self._hash and "/" in other:
            raise ValueError("Cannot append hierarchical path to a hash namespace")
        if not self._hash and "#" in other:
            raise ValueError("Cannot append fragment-like string to a slash namespace")

        # Slash namespace logic
        if self._hash:
            return Namespace(self._base, other, term_class=self._term_class)

        new_base = self._base.rstrip("/") + "/" + other.lstrip("/")
        return Namespace(new_base, term_class=self._term_class)


    # Fragment assignment
    def __add__(self, other: str) -> Namespace:
        if self._fragment is not None:
            raise ValueError('A namespace may only contain one fragment')
        return Namespace(self._base, str(other), term_class=self._term_class)

    # Dot-access for terminal term
    def __getattr__(self, name: str):
        if name.startswith('_'):
            raise AttributeError(f'{type(self).__name__} object has no attribute {name!r}')
        
        if self._hash:
            term = f'{self._base}#{name}'
        else:
            # Remove trailing slash from base, leading slash from name
            term = f'{self._base.rstrip('/')}/{name.lstrip('/')}'
        
        return self._term_class(term)

    # String representation
    def __str__(self) -> str:
        if self._fragment is not None:
            return f'{self._base}#{self._fragment}'
        if self._hash:
            return f'{self._base}#'
        return self._base

    def __repr__(self) -> str:
        return f'Namespace({str(self)!r})'

    # Membership test
    def __contains__(self, other: str | Namespace) -> bool:
        other_str = str(other)
        base_no_fragment = self._base
        return other_str.startswith(base_no_fragment)

    def to_rdflib(self):
        """
        Convert this Namespacecraft.Namespace to an rdflib.Namespace.

        Returns:
            rdflib.Namespace: an RDFLib-compatible namespace object.

        Raises:
            ImportError: if rdflib is not installed.
        """
        try:
            from rdflib import Namespace as RDFLibNamespace
        except ImportError as e:
            raise ImportError(
                "rdflib is required to use .to_rdflib(). Install it with "
                "`pip install rdflib`."
            ) from e

        # Construct the base string for RDFLib
        base_uri = str(self)

        # If this Namespace has a fragment, remove it for RDFLib.Namespace
        # RDFLib Namespace objects expect the base URI only
        if self._fragment is not None:
            base_uri = self._base

        return RDFLibNamespace(base_uri)