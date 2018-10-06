
def data_type(value):
    if ':' in value:
        return [ x.strip() for x in value.rsplit(':', 1) ]
    return ('', value.strip())

START = '__start__'
END = '__end__'
SEQUENCE = 'sequence'
MAPPING = 'mapping'
RENAME = 'rename'
IGNORE = 'ignore'
TYPS = (SEQUENCE, MAPPING, RENAME, IGNORE)


def parse(tokens):
    """ Infer a data structure from the ordered set of fields and
    return it."""
    target = typ = None
    out = []    # [(key, value)]
    stack = []  # [(target, typ, out)]

    for token in tokens:
        key, val = token
        if key == START:
            stack.append((target, typ, out))
            target, typ = data_type(val)
            if typ in TYPS:
                out = []
            else:
                raise ValueError("Unknown start marker %s" % repr(token))
        elif key == END:
            if typ == SEQUENCE:
                parsed = [v for (k, v) in out]
            elif typ == MAPPING:
                parsed = dict(out)
            elif typ == RENAME:
                parsed = out[0][1] if out else ''
            elif typ == IGNORE:
                parsed = None
            else:
                raise ValueError("Too many end markers")
            prev_target, prev_typ, out = stack.pop()
            if parsed is not None:
                out.append((target, parsed))
            target = prev_target
            typ = prev_typ
        else:
            out.append(token)

    if stack:
        raise ValueError("Not enough end markers")

    return dict(out)
