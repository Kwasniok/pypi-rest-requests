from json import dumps as _dumps
from typing import Any, Type, TypeAlias, Iterable, cast

_JSONNode: TypeAlias = (
    None | bool | int | float | str | dict[str, "_JSONNode"] | list["_JSONNode"]
)
JSON: TypeAlias = dict[str, "_JSONNode"] | list["_JSONNode"]


def diff(jsons: Iterable[JSON]) -> dict[tuple[str | int, ...], list[JSON]]:
    """
    Recursively diffs an iterable of JSON objects.
    Returns a mapping: recursive key --> list of values from each dict (in order).
    Only includes keys where not all values are equal.

    Example:
    ```python
    jsons = [
        {
            "a": 1,
            "b": {"c": 2, "d": 3},
        },
        {
            "a": 1,
            "b": {"c": 2, "d": 4},
        },
    ]
    expected = {
        ("b", "d"): [3, 4],
    }
    assert diff(jsons) == expected
    ```
    """
    return _diff(list(jsons), ())  # type: ignore


def _diff(
    jsons: list[_JSONNode], path: tuple[str | int, ...] = ()
) -> dict[tuple[str | int, ...], list[_JSONNode]]:

    differences: dict[tuple[str | int, ...], list[_JSONNode]] = {}

    # all None
    if _all_areinstances(jsons, type(None)):
        pass

    # all same primitive types
    elif (
        _all_areinstances(jsons, bool)
        or _all_areinstances(jsons, int)
        or _all_areinstances(jsons, float)
        or _all_areinstances(jsons, str)
    ):
        if not _all_equal(jsons):
            differences[path] = jsons

    # all dicts
    elif all(isinstance(d, dict) for d in jsons):
        ds = cast(list[dict[str, _JSONNode]], jsons)
        if not _all_equal(list(map(lambda d: d.keys(), ds))):
            differences[path] = list(jsons)
        else:
            for key in ds[0].keys():
                differences |= _diff(
                    [d[key] for d in ds],
                    (*path, key),
                )

    # all lists
    elif all(isinstance(d, list) for d in jsons):
        ls = cast(list[list[_JSONNode]], jsons)
        if not _all_equal(list(map(len, ls))):
            differences[path] = list(jsons)
        else:
            for i in range(len(ls[0])):
                differences |= _diff(
                    [d[i] for d in ls],
                    (*path, i),
                )

    # mixed types
    else:
        differences[path] = list(jsons)

    return differences


def _all_areinstances(
    xs: list[Any],
    typ: Type,
) -> bool:
    return all(isinstance(item, typ) for item in xs)


def _all_equal(
    xs: list[Any],
) -> bool:
    return len(xs) == 0 or all(item == xs[0] for item in xs[1:])
