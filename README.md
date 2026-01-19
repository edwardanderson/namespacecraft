# Namespacecraft

Namespacecraft is a tiny toolkit for composing URI namespaces.

## Use

```pycon
>>> from namespacecraft import Namespace, Term
>>> EX = Namespace('http://example.org/')
>>> EX.a
Term('http://example.org/a)
>>> Namespace('http://example.org').terminates_with('#') / 'a' / 'b' / 'c' + 'x'
Term('http://example.org/a/b/c#x)
```

### Paths

Build paths using the `/` operator.

```pycon
>>> Namespace('http://example.org/') / 'a' / 'b' / 'c'
Namespace('http://example.org/a/b/c)
```

Lists are coerced to string paths.

```pycon
>>> Namespace('http://example.org') / [1, 2, 3]
Namespace('http://example.org/1/2/3)
```

Use `terminates_with()` to set the final delimiter.

```pycon
>>> Namespace('http://example.org').terminates_with('#') / 'a' / 'b'
Namespace('http://example.org/a/b#')
```

### Terms

Create terms by accessing a `Namespace` attribute.

```pycon
>>> EX = Namespace('http://example.org/')
>>> EX.a
Term('http://example.org/a')
```

Or by getting an attribute by name.

```pycon
>>> EX['b']
Term('http://example.org/b)
```

Or with the `+` operator.

```pycon
>>> EX + 1
Term('http://example.org/1)
```

`Namespace` will create terms in any class that initialises from `str`. For example create terms as instances of [`rdflib.URIRef`](https://rdflib.readthedocs.io/en/stable/rdf_terms/?h=uriref#uriref).

```python
from namespacecraft import Namespace
from rdflib import Graph, URIRef


EX = Namespace('http://example.org/', term_cls=URIRef).terminates_with('/') / 'a/b/c'
graph = Graph()
graph.add((EX.s, EX.p, EX.o))
print(graph.serialize(format='turtle'))
```

```turtle
@prefix ns1: <http://example.org/a/b/c/> .

ns1:s ns1:p ns1:o .
```

## Install

```bash
uv add namespacecraft
```

## Gotchas

The `+` operator returns a terminal URI object. Any further `+` operations on that object are string concatenations, not additional fragments.

```pycon
>>> from namespacecraft import Namespace
>>> Namespace('http://example.org/') + 'a'
Namespace('http://example.org/a')
>>> Namespace('http://example.org/') + 'a' + 'b'
'http://example.org/ab'
```

## Test

```bash
uv run pytest
```
