from __future__ import annotations


class Namespace:
    __slots__ = ('_base', '_fragment')

    def __init__(self, base, fragment=None) -> None:
        self._base = str(base)
        self._fragment = fragment

    def __truediv__(self, other) -> Namespace:
        # coerence list into path parts
        if isinstance(other, (list, tuple)):
            ns = self
            for part in other:
                ns = ns / part
            return ns

        other = str(other)

        # strip one side to ensure a single slash
        if self._base.endswith('/') and other.startswith('/'):
            new_base = self._base + other[1:]
        elif not self._base.endswith('/') and not other.startswith('/'):
            new_base = self._base + '/' + other
        else:
            new_base = self._base + other

        # path extension clears any fragment
        return Namespace(new_base)

    def __add__(self, other) -> Namespace:
        if self._fragment is not None:
            raise ValueError('A namespace may only contain one fragment')

        fragment = str(other)
        return Namespace(self._base, fragment)

    def __str__(self) -> str:
        if self._fragment is None:
            return self._base
        return f'{self._base}#{self._fragment}'

    def __repr__(self) -> str:
        return f'Namespace({str(self)!r})'

    def __contains__(self, other):
        other_str = str(other)
        # Ignore fragment in the namespace base
        base_no_fragment = self._base
        if self._fragment:
            base_no_fragment = self._base.split('#', 1)[0]
        return other_str.startswith(base_no_fragment)
