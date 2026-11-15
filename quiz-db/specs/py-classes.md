# Classes (just enough): coverage spec

**Ladder:** Python core › Classes (just enough)   ·   **Prerequisites:** py-basics, py-functions, py-errors (reading AttributeError / TypeError)
**Why it matters for AI/ML:** Every PyTorch model is a class (`class Net(nn.Module)` with `__init__` and `forward`), every Dataset is a class with `__len__` and `__getitem__`, and scikit-learn estimators are objects with `fit`/`predict`. Configs are dataclasses. You don't need to be an OOP architect, but you must read and write these patterns without guessing.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `class-instance` | Class vs instance, `__init__`, `self` | class = blueprint, `Point(2, 3)`, self = this | instances are independent, forgetting `self` | `__new__` vs `__init__`, bound methods | `__new__` returning another type |
| 2 | `attributes` | Instance vs class attributes | class attribute read via instance | shared mutable class attribute trap, shadowing | `__dict__`, `+=` on class attr via instance, mutable default arg | lookup order instance -> class at runtime |
| 3 | `methods` | Methods, `@classmethod`, `@staticmethod` | calling a method, method uses self | classmethod as alternative constructor, staticmethod | classmethod + inheritance returns subclass, bound methods | `__init_subclass__` registries |
| 4 | `property-encapsulation` | `@property` and encapsulation (`_x`, `__x`) | `_x` is a convention | `@property` getter, read-only property, setter with validation, `__x` mangling | mangled name `_Class__x` | mangling in subclasses |
| 5 | `inheritance` | Inheritance, `super()` and MRO | `class Dog(Animal)`, overriding, isinstance | `super().__init__`, forgetting it | MRO of a diamond, cooperative super, isinstance vs type | super() follows the MRO not the parent, inconsistent MRO |
| 6 | `dunder` | Dunder (special) methods | what dunders are, `__len__`, `__str__` | `__repr__` vs `__str__`, default `__eq__`, `__getitem__`, `__call__` | `__eq__` without `__hash__`, `__add__`, NotImplemented, `__bool__`, old iteration protocol | hash/eq consistency, `__getattr__`, `__radd__` and sum() |
| 7 | `dataclasses` | Dataclasses | `@dataclass` auto `__init__`/`__repr__` | equality, defaults, keyword args | mutable default error, `default_factory`, `frozen`, `__post_init__`, unhashable by default | default-before-non-default across inheritance |
| 8 | `duck-typing` | Duck typing, protocols and ABCs | "if it quacks" | unrelated classes with the same method, TypeError when a dunder is missing | `typing.Protocol` + runtime_checkable, ABC cannot be instantiated | structural vs nominal typing |
| 9 | `composition` | Composition vs inheritance | has-a vs is-a | choosing composition | why prefer composition (fragile base class) | Liskov violations, delegation |
| 10 | `internals` | `__slots__` and descriptors | — | — | what `__slots__` is for | slots block new attributes / no `__dict__`, descriptors, data descriptor precedence, cached_property |
| 11 | `nn-module` | The `nn.Module` pattern | forward holds the computation | build a Net, call `model(x)` not `model.forward(x)` | forgetting `super().__init__()`, parameter count, plain list vs ModuleList | `__setattr__` registration, eval() propagation, hooks run via `__call__` |
| 12 | `iteration` | Making classes iterable: `__iter__` and `__next__` | — | `__iter__` written with yield, `__iter__`/`__next__` names | iterable vs iterator (one-shot iterators), generator `__iter__` is reusable | — |
| 13 | `copying` | Identity, aliasing and copying objects | `b = a` is the same object | `==` vs `is`, shallow `copy.copy` shares inner lists | `list.copy()` keeps the same objects, `deepcopy` | `state_dict()` returns live references (the 'best weights' bug) |

## Must-know facts
- A class is a blueprint; calling it (`Point(2, 3)`) creates an instance and runs `__init__`.
- `self` is the instance (Java/JS `this`) and must be the first parameter of instance methods; Python passes it for you.
- Attributes set on `self` belong to one instance; attributes in the class body are shared by all instances.
- Assigning through an instance (`a.n = 5`) creates an instance attribute that shadows the class one; mutating (`a.items.append`) changes the shared object.
- `@classmethod` gets the class (`cls`), ideal for alternative constructors; `@staticmethod` gets nothing, it's a plain function in the class namespace.
- `@property` makes a method look like an attribute; without a setter it is read-only.
- `_x` = "internal" by convention only; `__x` is name-mangled to `_ClassName__x`.
- `super().__init__(...)` must be called in a subclass `__init__` if the parent sets attributes.
- Method lookup follows the MRO (`Class.__mro__`); `super()` means "next in the MRO", not "my parent".
- `print(obj)` uses `__str__` (falls back to `__repr__`); containers show `__repr__` of their items.
- Default `__eq__` is identity; defining `__eq__` sets `__hash__` to None (unhashable) unless you define it too.
- `__len__` + `__getitem__` is exactly the PyTorch map-style Dataset protocol; `__call__` makes an object callable.
- `@dataclass` writes `__init__`, `__repr__`, `__eq__`; mutable defaults need `field(default_factory=list)`.
- Duck typing: Python cares whether an object has the method, not what class it is.
- Prefer composition ("has-a") unless the subclass truly "is-a" substitutable parent.
- `nn.Module`: layers in `__init__` (after `super().__init__()`), maths in `forward`, call `model(x)` so `__call__` can run hooks.
- `for` calls `__iter__`; an iterator implements `__next__` and raises StopIteration at the end.
- Assignment never copies an object; `copy.copy` is shallow, `copy.deepcopy` copies all the way down.

## Common traps (each one must have at least one question)
- Forgetting `self` in a method definition -> TypeError: takes 0 positional arguments but 1 was given.
- Mutable class attribute (`layers = []`) -> shared by every instance.
- Mutable default argument in `__init__` (`items=[]`) -> shared between instances.
- `a.n += 1` on an int class attribute -> creates an instance attribute, class value unchanged.
- Forgetting `super().__init__()` -> AttributeError for parent attributes (and in nn.Module, an error on the first layer assignment).
- Calling a property with parentheses (`c.area()`) or assigning to a read-only property -> TypeError / AttributeError.
- `__x` "private" attribute -> AttributeError from outside, it's renamed `_Class__x`.
- Two equal-looking objects compare `==` False -> default `__eq__` is identity.
- Defining `__eq__` only -> objects can no longer go in a set or be dict keys.
- `@dataclass` with `tags: list = []` -> ValueError at class definition.
- Thinking `super()` always calls the direct parent -> it calls the next class in the MRO.
- Storing layers in a plain Python list -> PyTorch doesn't register their parameters; use nn.ModuleList.
- Calling `model.forward(x)` directly -> skips hooks.
- Mutating a field used in `__hash__` after inserting into a set -> the object becomes unfindable.
- `__slots__` class -> cannot add new attributes.
- `best = model.state_dict()` -> keeps live references, so 'best' silently follows the latest weights; deepcopy or clone.
- `copy.copy(obj)` -> inner lists and dicts are still shared.
- An object whose `__iter__` returns self -> empty on the second loop.
- Reading `name` instead of `self.name` in a method -> NameError.
- Annotation-less class attribute in a @dataclass -> not a field, not in `__init__`.
- `self.value` inside the `value` property -> RecursionError; store it as `self._value`.
- `model.eval()` does not turn off gradients -> also use `torch.no_grad()`.
- Plain tensor attribute on nn.Module -> not a parameter and not moved by `.to()`; use nn.Parameter or register_buffer.
- Subclassing dict and overriding `__setitem__` -> `update()` and the constructor bypass it.
- `__getattr__` that reads `self.inner` -> RecursionError when copied or pickled.
- Mixin listed after the base class -> its method never runs.

## Interview angle
1. **"Explain self."** It's the instance the method was called on, passed automatically as the first argument: `d.bark()` is `Dog.bark(d)`. Same as `this` in Java, but explicit.
2. **"Class vs instance attribute, and the classic bug?"** Class attributes are shared; a mutable one (`items = []`) is shared state across all instances, like a static field in Java. Initialise per-instance state in `__init__`.
3. **"classmethod vs staticmethod?"** classmethod receives the class, so it's used for alternative constructors (`from_json`) and works correctly for subclasses; staticmethod is a namespaced utility with no access to class or instance.
4. **"What is the MRO / how does super() work?"** Python linearises the class hierarchy (C3), and `super()` delegates to the next class in that order, which makes cooperative multiple inheritance work in diamonds.
5. **"Walk me through a PyTorch model class."** Subclass nn.Module, call `super().__init__()`, assign layers as attributes (nn.Module's `__setattr__` registers them so `.parameters()` and `.to(device)` find them), write `forward`, and call `model(x)` so `__call__` runs hooks before `forward`. SDE analogy: a framework base class with a template method.

## Source material
To be added
