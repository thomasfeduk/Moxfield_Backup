from __future__ import annotations
import json
import re
from abc import abstractmethod, ABC
from typing import Any, Dict, List, Iterator, TypeVar, Generic


class InvalidFilenameError(Exception):
    pass


T = TypeVar('T')


class Collection(Generic[T]):
    def __init__(self, items: list[T] | None = None):
        if items is None:
            items = []
        self._current_index = 0
        if not isinstance(items, list):
            raise TypeError(f'Type "list" is expected. Received: {type(items)} {repr(items)}')
        self._items: list[T] = items

    def __iter__(self) -> Iterator[T]:
        self._current_index = 0
        return iter(self._items)

    def __next__(self) -> T:
        if self._current_index >= len(self._items):
            raise StopIteration
        self._current_index += 1
        return self._items[self._current_index - 1]

    def __getitem__(self, index) -> T:
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self._items))
            return [self._items[i] for i in range(start, stop, step)]
        else:
            return self._items[int(index)]

    def __setitem__(self, key, value: T) -> None:
        self._items[key] = value

    def __add__(self, value: list[T] | Collection[T]) -> Collection[T]:
        if isinstance(value, Collection):
            combined = self._items + value._items
        elif isinstance(value, list):
            combined = self._items + value
        else:
            raise TypeError(f"Cannot concatenate '{self.__class__.__name__}' and '{value.__class__.__name__}' objects")
        return Collection(combined)

    def __len__(self) -> int:
        return len(self._items)

    def __str__(self) -> str:
        return str(self._items)

    def __repr__(self) -> str:
        output = f"{self.__class__.__name__}["
        output += ','.join(map(repr, self._items))
        output += f']'
        return output

    def __eq__(self, other) -> bool:
        return repr(self) == repr(other)

    def append(self, item: T) -> None:
        self._items.append(item)

    def json(self, *, indent: int | None = None) -> str:
        return json.dumps([json.loads(i.json()) for i in self._items], indent=indent)


class RestrictedCollection(Collection[T], ABC):
    def __init__(self, items: list[T] | None = None):
        super().__init__(items)
        for item in self._items:
            self._validate_item(item)

    def __iter__(self) -> Iterator[T]:
        super().__iter__()
        return self

    def __getitem__(self, index) -> T:
        return super().__getitem__(index)

    def __next__(self) -> T:
        return super().__next__()

    def append(self, item: T) -> None:
        self._validate_item(item)
        self._items.append(item)

    def __setitem__(self, key, value: T) -> None:
        self._validate_item(value)
        self._items[key] = value

    def __add__(self, value: list[T] | RestrictedCollection[T]) -> RestrictedCollection[T]:
        if isinstance(value, list):
            combined = self._items + value
        elif isinstance(value, RestrictedCollection):
            combined = self._items + value._items
        else:
            raise TypeError("Can only add a list of T or RestrictedCollection of T to this collection")
        return self.__class__(combined)

    @property
    @abstractmethod
    def expected_type(self) -> type:
        return object

    def _validate_item(self, value: T) -> T:
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"Each item in the collection must be of type {repr(self.expected_type)}. Received: {type(value)} {repr(value)}")
        return value


def safe_filename(filename: str) -> str:
    safe_name = re.sub(r'[^a-zA-Z0-9-_ ]', '', filename)
    safe_name = safe_name.strip()
    if safe_name == '':
        raise InvalidFilenameError(f'Filename is invalid as it resulted in zero acceptable characters.\n'
                                   f'Original passed value: "{filename}"')
    return safe_name


def display_friendly_error(friendly_error_msg: str) -> None:
    cols = 85
    print('\n')
    print('-' * cols)
    print('!' * cols)
    print('-' * cols)
    print('\n')
    print(friendly_error_msg)
    print('\n')
    print('-' * cols)
    print('!' * cols)
    print('-' * cols)

