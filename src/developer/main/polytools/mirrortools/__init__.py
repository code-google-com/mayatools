import pkgutil

__all__ = []

print 'executing ....'
print __path__

for loader, pkg_name, is_pkg in pkgutil.walk_packages(__path__):
    if is_pkg and 'widget' in pkg_name:
        __all__.append(module_name)
        module = loader.find_module(pkg_name).load_module(pkg_name)
        exec('%s = module' % pkg_name)