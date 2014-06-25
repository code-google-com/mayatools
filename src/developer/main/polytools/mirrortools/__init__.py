import pkgutil

__all__ = []

print 'executing ....'

for loader, modul e_name, is_pkg in pkgutil.walk_packages(__path__):
    if not is_pkg and 'Widget' in module_name:
        print module_name
        #__all__.append(module_name)
        #module = loader.find_module(module_name).load_module(module_name)
        #exec('%s = module' % module_name)