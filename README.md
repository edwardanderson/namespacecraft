# Namespacecraft

Namespacecraft is a tiny toolkit for composing URI namespaces.

```pycon
>>> from namespacecraft import Namespace
>>> EX = Namespace('http://example.org/') / 'a' / 'b' / 'c'
>>> str(EX)
'http://example.org/a/b/c
>>> EX = Namespace('http://example.org') / [1, 2, 3]
>>> str(EX)
'http://example.org/1/2/3/'
>>> EX = Namespace('http://example.org/') / 'x' + 'y'
>>> str(EX)
'http://example.org/x#y'
>>> EX = Namespace('http://example.org/)
>>> EX.a
'http://example.org/a'
```

`Namespace` can be configured to create terms in any class that initialises from `str`.

For example, use with [RDFLib](https://rdflib.readthedocs.io/en/stable/):

```python
from namespacecraft import Namespace
from rdflib import Graph, URIRef


EX = Namespace('http://example.org', term_class=URIRef) / 'a/b/c/'
graph = Graph()
graph.add((EX.s, EX.p, EX.o))
print(graph.serialize(format='turtle'))
```

```turtle
@prefix ns1: <http://example.org/a/b/c/> .

ns1:s ns1:p ns1:o .
```

## Install

> [!NOTE]
> Until this package has a 1.x.x release, install it in editable state in a virtual environment.

```bash
git clone https://github.com/edwardanderson/namespacecraft.git
cd namespacecraft
uv venv
uv pip install --editable namespacecraft
```
