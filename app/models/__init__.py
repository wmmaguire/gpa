import inspect
import pkgutil
import importlib
import sys


def import_models():
    thismodule = sys.modules[__name__]
    module_iter = pkgutil.iter_modules(thismodule.__path__,
                                       thismodule.__name__ + '.')
    for loader, module_name, is_pkg in module_iter:
        module = importlib.import_module(module_name, loader.path)
        for name, _object in inspect.getmembers(module, inspect.isclass):
            globals()[name] = _object


import_models()
