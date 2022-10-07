from typing import Any
from typing import Iterable

NOT_SET = object()

def get_arg(
    index: int,
    name: str,
    args: tuple,
    kwargs: dict[str, Any],
    default: Any = NOT_SET,
    position_offset: int = 1,
) -> Any:
    by_position = index < len(args)
    by_name = name in kwargs

    position = index + position_offset

    if by_name and by_position:
        raise TypeError(f"function argument given by name ({name!r}) and position ({position!r})")

    if not by_name and not by_position:
        if default is not NOT_SET:
            return default
        raise TypeError(f"function missing required argument {name!r} (pos {position})")

    if by_position:
        return args[index]
    else:
        return kwargs[name]


def validate_args(
    max_args: int,
    allowed_keys: Iterable[str],
    args: tuple,
    kwargs: dict[str, Any],
) -> None:
    total_args = len(args) + len(kwargs)
    if total_args > max_args:
        if max_args == 0:
            subj = "no arguments"
        elif max_args == 1:
            subj = "at most 1 argument"
        else:
            subj = f"at most {max_args} arguments"
        raise TypeError(f"function accepts {subj} ({total_args} given)")

    allowed_keys = set(allowed_keys)
    invalid_keyword = next((key for key in kwargs.keys() if key not in allowed_keys), None)
    if invalid_keyword is not None:
        raise TypeError(f"{invalid_keyword!r} is an invalid keyword argument for this function")
