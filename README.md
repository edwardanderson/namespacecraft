# Namespacecraft

Namespacecraft is a tiny toolkit for composing URI namespaces.

```python
>>> from namespacecraft import Namespace

>>> Namespace('http://example.org/')
http://example.org/

>>> Namespace('http://example.org/') / 'a' / 'b' / 'c'
http://example.org/a/b/c/

>>> Namespace('http://example.org') / [1, 2, 3]
http://example.org/1/2/3/

>>> Namespace('http://example.org/') / 'x' + 'y'
http://example.org/x#y
```
