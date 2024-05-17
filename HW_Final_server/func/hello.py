def hello():
    return "<h1>Hello!</h1>"

_func = hello

__exports__ = {
    "name" : _func.__code__.co_name,
    "path" : "/",
    "methods": ['GET'],
    "execute": _func
}

if __name__ == "__main__":
    print(_func.__code__.co_name)