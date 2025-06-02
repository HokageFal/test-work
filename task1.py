def strict(func):
    def wrapper(*args, **kwargs):
        type_hints = func.__annotations__

        for arg_name, arg_value in zip(type_hints.keys(), args):
            expected_type = type_hints[arg_name]
            if not isinstance(arg_value, expected_type):
                raise TypeError(
                    f"Аргумент '{arg_name}' должен быть типа {expected_type.__name__}, "
                    f"а получен {type(arg_value).__name__}"
                )

        for arg_name, arg_value in kwargs.items():
            if arg_name in type_hints:
                expected_type = type_hints[arg_name]
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Аргумент '{arg_name}' должен быть типа {expected_type.__name__}, "
                        f"а получен {type(arg_value).__name__}"
                    )

        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


# Тестируем
print(sum_two(1, 2))
print(sum_two(1, 2.4))