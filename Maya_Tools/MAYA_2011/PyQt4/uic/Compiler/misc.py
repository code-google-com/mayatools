def moduleMember(module, name):
    if module:
        return "%s.%s" % (module, name)

    return name


class Literal(object):
    """Literal(string) -> new literal

    string will not be quoted when put into an argument list"""
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string

    def __or__(self, r_op):
        return Literal("%s|%s" % (self, r_op))
