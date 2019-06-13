import inspect


def modified_func(func, *args, fixated_args, fixated_kwargs, **kwargs):

    def updated_func():
        new_args = fixated_args + args

        new_kwargs = fixated_kwargs.copy()
        new_kwargs.update(kwargs)

        func.__name__ = f'func_{func.__name__}'

        func.__doc__ = f'''A func implementation of {func.__name__} with pre-applied arguments being:
        ... {inspect.getfullargspec(modified_func).kwonlydefaults}
        ... source_code: \n {inspect.getsource(func)}'''

        return func(*new_args, **new_kwargs)

    return updated_func()
