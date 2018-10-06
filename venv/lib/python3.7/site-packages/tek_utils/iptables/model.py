switches = {
    'policy': 'P',
    'append': 'A',
    'flush': 'F',
    'jump': 'j',
    'delete': 'X'
}


def join_if(seq):
    string = ''
    for index, item in enumerate(seq):
        if item:
            string += str(item) + ' '
    return string.rstrip()


def switchify(switch):
    if len(switch) == 0:
        raise SwitchError('Zero-length switch!')
    if switch[0] == '-':
        pass
    elif len(switch) == 1:
        switch = '-' + switch
    else:
        switch = '--' + switch
    switch = switch.replace('M', '-')
    return switch


class SwitchError(Exception):
    pass


class Argument(object):
    ''' single parameter for iptables. If noswitch is False, a - or --
    is prepended, depending on the length. As iptables args can contain
    a minus sign, this has to be handled. M is being replaced by a
    minus.
    '''
    def __init__(self, string, noswitch=False):
        if string:
            assert(isinstance(string, str))
        if not string or noswitch:
            self.argument = string
        else:
            self.argument = switchify(string)

    def __str__(self):
        return self.argument

    @property
    def strings(self):
        return [self.argument]

    def __bool__(self):
        return self.argument is not None and bool(self.argument)


class InvalidArgument(Argument):
    def __init__(self):
        super(InvalidArgument, self).__init__(None)


class Option(Argument):
    def __init__(self, switch, parameter):
        Argument.__init__(self, switch)
        if parameter:
            assert(isinstance(parameter, str))
        self.parameter = Argument(parameter, True)

    def __str__(self):
        return super(Option, self).__str__() + ' ' + str(self.parameter)

    def __bool__(self):
        return super(Option, self).__bool__() and bool(self.parameter)

    @property
    def strings(self):
        if self:
            return [self.argument, str(self.parameter)]
        else:
            return []


class Rule(object):
    def __init__(self, *arguments, **params):
        self._params = dict()
        for argument in arguments:
            self.set_argument(argument)
        for param, value in params.items():
            self.set(param, value)

    # TODO def __call__(self, param, value):
    #    self.set(param, value)
    #    return self

    def set(self, param, value):
        self.set_argument(Option(param, value))

    def set_argument(self, argument):
        if isinstance(argument, str):
            argument = Argument(argument)
        assert(isinstance(argument, Argument))
        self._params[argument.argument] = argument

    @property
    def params(self):
        return list(self._params.values())

    @property
    def string(self):
        return join_if(self.params)

    @property
    def strings(self):
        ret = []
        for option in self.params:
            assert(isinstance(option, Argument))
            if option:
                ret.extend(option.strings)
        return ret


class CommandBase(Rule):
    def __init__(self, switch, **params):
        super(CommandBase, self).__init__(**params)
        self.switch = switch

    @property
    def params(self):
        return [self.switch] + (super(CommandBase, self).params)


class Match(Rule):
    def __init__(self, field=None, **params):
        Rule.__init__(self, **params)
        self.field = Option('match', field)

    @property
    def params(self):
        ''' empty match options still have a valid 'field' option. As ist is invalid
            to pass only that parameter, the options have to be checked.
        '''
        options = super(Match, self).params
        if any(options):
            return [self.field] + options
        else:
            return [InvalidArgument()]


class StateMatch(Match):
    def __init__(self, value):
        super(StateMatch, self).__init__('state', state=value)


class MacMatch(Match):
    def __init__(self, value):
        super(MacMatch, self).__init__('mac', macMsource=value)


class Target(CommandBase):
    def __init__(self, target=None, **params):
        CommandBase.__init__(self, Option('j', target), **params)


class Accept(Target):
    def __init__(self, **params):
        super(Accept, self).__init__('ACCEPT', **params)


class Reject(Target):
    def __init__(self, reject_with=None, **params):
        super(Reject, self).__init__('REJECT', rejectMwith=reject_with,
                                     **params)


class NoTarget(Target):
    def __init__(self, **params):
        super(NoTarget, self).__init__()


class DNAT(Target):
    # TODO check for nat table usage
    def __init__(self, to_destination, **params):
        super(DNAT, self).__init__('DNAT', **params)
        self.set('to-destination', to_destination)


class Command(CommandBase):
    ''' one line of iptables love.
    '''

    def __init__(self, switch, chain=None, *rules):
        ''' @param rules: rules to be used in order. if one of them is a
        Target, it is used as target.
        '''
        self.rules = []
        self.target = Accept()
        for rule in rules:
            if isinstance(rule, Target):
                self.target = rule
            else:
                self.rules.append(rule)
        if chain:
            argument = Option(switch, chain)
        else:
            argument = Argument(switch)
        CommandBase.__init__(self, argument)

    @property
    def params(self):
        ret = super(Command, self).params
        for rule in self.rules:
            ret += rule.params
        if self.target:
            ret.extend(self.target.params)
        return ret


class Append(Command):
    def __init__(self, chain=None, *rules):
        super(Append, self).__init__(switches['append'], chain, *rules)


class Flush(Command):
    def __init__(self, table=None):
        ''' need to pass chain=None and an invalid Target '''
        super(Flush, self).__init__(switches['flush'], None, Target(),
                                    Rule(table=table))


class DeleteChains(Command):
    def __init__(self, chain=None):
        ''' need to pass chain=None and an invalid Target '''
        super(DeleteChains, self).__init__(switches['delete'], chain, Target())


class Policy(Command):
    def __init__(self, chain, action):
        super(Policy, self).__init__('P', chain,
                                     Rule(Argument(action, noswitch=True)),
                                     NoTarget())

    @property
    def params(self):
        return super(Policy, self).params


class Chain(object):
    pass
