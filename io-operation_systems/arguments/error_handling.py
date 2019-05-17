
def validate(args):
    try:
        args = schema.validate(args)
        return args
    except SchemaError as e:
        exit(e)

    if arguments['<command>'] == 'hello':
        greet(validate(docopt(HELLO)))
    elif arguments['<command>'] == 'goodbye':
        greet(validate(docopt(GOODBYE)))
