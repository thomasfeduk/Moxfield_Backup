from __future__ import annotations
import json
import re
from abc import abstractmethod
from typing import Any, Dict, List


class InvalidFilenameError(Exception):
    pass


class Collection:
    def __init__(self, items: list | None = None):
        if items is None:
            items = []
        self._current_index = 0
        if not isinstance(items, list):
            raise TypeError(f'Type "list" is expected. Received:  {type(items)} {repr(items)}')
        self._items = items

    def __iter__(self) -> Any:
        self._current_index = 0
        return self

    def __next__(self) -> Any:
        if self._current_index >= len(self._items):
            raise StopIteration
        self._current_index += 1
        return self._items[self._current_index - 1]

    def __getitem__(self, index) -> Any:
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self._items))
            return [self._items[i] for i in range(start, stop, step)]
        else:
            return self._items[int(index)]

    def __setitem__(self, key, value) -> None:
        self._items[key] = value

    def __add__(self, value: list | Collection) -> Collection:
        if isinstance(value, Collection):
            combined = self._items + value._items
        elif isinstance(value, list):
            combined = self._items + value
        else:
            raise TypeError(f"Cannot concatenate '{self.__class__.__name__}' and '{value.__class__.__name__}' objects")
        # Return a new instance
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

    def append(self, item) -> None:
        self._items.append(item)

    def toJson(self, *, indent: int | None = None) -> str:
        return json.dumps([json.loads(i.toJson()) for i in self._items], indent=indent)


class RestrictedCollection(Collection):
    @abstractmethod
    def __init__(self, items: list = None):
        super().__init__(items)
        for item in self._items:
            self._validate_item(item)

    @abstractmethod
    def __iter__(self) -> Any:
        super().__iter__()
        return self

    @abstractmethod
    def __getitem__(self, index) -> Any:
        return super().__getitem__(index)

    @abstractmethod
    def __next__(self) -> Any:
        return super().__next__()

    def append(self, item) -> None:
        self._validate_item(item)
        self._items.append(item)

    def __setitem__(self, key, value) -> None:
        self._validate_item(value)
        self._items[key] = value

    def __add__(self, value: RestrictedCollection) -> Any:
        # Need to rework this to handle restricted type checking with list support both here
        # and in the extended class that does proper type checking thats compatible from
        # both the restricted class and extended class perspective
        raise NotImplementedError

        # Return a new instance
        # return RestrictedCollection(list(super().__add__(list(value))))

    @property
    @abstractmethod
    def expected_type(self):
        return object  # Set your allowed object type here

    def _validate_item(self, value):
        if isinstance(value, self.expected_type):
            return value
        raise TypeError(f"Each item in the collection must be of type {repr(self.expected_type)}. Received: "
                        f"{type(value)} {repr(value)}")


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

