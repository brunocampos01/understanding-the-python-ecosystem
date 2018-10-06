import time
import copy
from re import compile as regex

from tek.tools import decode
from tek.errors import InternalError, InvalidInput, MooException
from golgi.io.terminal import terminal, ColorString


class UserInputTerminated(MooException):
    pass


class InputQueue(list):
    delay = None
    force_output = False

    def push(self, *input):
        self.extend(input)

    @property
    def pop(self):
        if self.delay is not None:
            time.sleep(self.delay)
        return list.pop(self, 0)

    @property
    def suppress_output(self):
        return bool(self) and not self.force_output

input_queue = InputQueue()


def is_digit(arg):
    return isinstance(arg, int) or (isinstance(arg, str) and
                                    arg.isdigit())


class UserInput(object):
    def __init__(self, text, validator=None, validate=True, newline=True,
                 single=False, remove_text=False, initial_input=None, **kw):
        """ @param remove_text: Clear the prompt lines after input has
        been accepted.
        @param newline: Print a newline after input has been accepted.
        @param initial_input: Text that is inserted into the input
        initially. Will be returned as input value.
        """
        self._text = text
        self._validator = validator
        self._do_validate = validate
        self._newline = newline
        self._single = single
        self._remove_text = remove_text
        self._initial_input = initial_input
        self.__init_attributes()

    def __init_attributes(self):
        self._input = None
        self._args = None
        self._setup_validator()

    def _setup_validator(self):
        pass

    @property
    def value(self):
        return decode(self._input)

    @property
    def args(self):
        return self._args

    def read(self):
        prompt = self.prompt
        if input_queue:
            self._synth_input()
        else:
            clear_count = max(len(prompt) - len(self.fail_prompt), 0)
            lower = prompt[clear_count:]
            upper = prompt[:clear_count]
            if not terminal.locked:
                terminal.lock()
            if self._remove_text:
                terminal.push_lock()
            terminal.push(upper)
            while not self._read(lower):
                lower = self.fail_prompt
            if self._remove_text:
                terminal.pop_lock()
            if self._newline:
                terminal.push()
        return self.value

    def _read(self, prompt):
        terminal.push(prompt)
        terminal.write(' ')
        input = terminal.input(single=self._single,
                               initial=self._initial_input)
        valid = self._do_input(input)
        if not valid:
            terminal.pop()
        return valid

    def _synth_input(self):
        if not input_queue.suppress_output:
            terminal.push(self.prompt)
        input = input_queue.pop
        if not self._do_input(input):
            raise InvalidInput(input)

    def _do_input(self, input):
        self._input = input
        return self._validate()

    def _validate(self):
        return not (self._do_validate and self._validator and not
                    self._validator.match(str(self._input)))

    @property
    def prompt(self):
        return self._text

    @property
    def fail_prompt(self):
        return ['Invalid input. Try again:']


class SimpleChoice(UserInput):
    def __init__(self, elements, text=[''], additional=[], *a, **kw):
        self.text = text
        self._elements = list(map(str, elements))
        self._additional = list(map(str, additional))
        UserInput.__init__(self, [], *a, **kw)

    def _setup_validator(self):
        self._validator = regex(r'^(%s)$' % '|'.join(self._elements +
                                                     self._additional))

    @property
    def prompt(self):
        text = list(self.text)
        text[-1] += self.input_hint_string
        return text

    @property
    def fail_prompt(self):
        sup = UserInput.fail_prompt.fget(self)
        sup[-1] += self.input_hint_string
        return sup

    @property
    def input_hint_string(self):
        v = [_f for _f in self.input_hint if _f]
        return ' [%s]' % '/'.join(v) if v else ''

    @property
    def input_hint(self):
        return [e for e in self._elements if not e.isdigit()]

    def add_element(self, e):
        self._elements.append(str(e))
        self._setup_validator()


class SingleCharSimpleChoice(SimpleChoice):
    """ Restrict input to single characters, allowing omission of
    newline for input. Fallback to conventional SimpleChoice if choices
    contain multi-char elements.
    """
    def __init__(self, elements, enter=None, additional=[], validate=True,
                 *args, **kwargs):
        if enter:
            additional += ['']
        self._enter = enter
        single = (all(len(str(e)) <= 1 for e in elements + additional) and
                  validate)
        SimpleChoice.__init__(self, elements, additional=additional,
                              single=single, validate=validate, *args,
                              **kwargs)

    def _do_input(self, _input):
        return SimpleChoice._do_input(self, self._enter if self._enter and
                                      _input == '' else _input)


class YesNo(SingleCharSimpleChoice):
    def __init__(self, text=['Confirm'], *args, **kwargs):
        SingleCharSimpleChoice.__init__(self, ['y', 'n'], text=text, enter='y')

    @property
    def value(self):
        return self._input == 'y'

    def __bool__(self):
        return bool(self.value)


class SpecifiedChoice(SingleCharSimpleChoice):
    """ Automatically supply enumeration for the strings available for
    choice and query for a number.
    @param info: list of lines to print after the corresponding
    element, without enumeration.
    """

    def __init__(self, elements, text_pre=None, text_post=None, simple=None,
                 info=None, values=None, *args, **kwargs):
        """ @param values: optional list of objects to return from if
        selected by number
        """
        self._choices = elements
        self._values = values
        self._simple = simple or []
        self._text_pre = text_pre or []
        self._text_post = text_post or []
        self._info = info or [[]] * len(elements)
        self._numbers = list(range(1, len(elements) + 1))
        SingleCharSimpleChoice.__init__(self, elements=self._numbers,
                                        text=[], additional=self._simple,
                                        *args, **kwargs)

    def _format_choice(self, n, choice, info):
        pad = ' ' * (len(str(self._numbers[-1])) - len(str(n)))
        return [' {}[{}] {}'.format(pad, n, choice)] + [' ' * 5 + i for i in
                                                        info]

    @property
    def prompt(self):
        text = copy.copy(self._text_pre)
        for c in zip(self._numbers, self._choices, self._info):
            text.append(self._format_choice(*c))
        return text + self._text_post

    @property
    def input_hint(self):
        return self._simple

    def _is_choice_index(self, index):
        return is_digit(index) and 0 < int(index) <= len(self._choices)

    @property
    def value(self):
        i = SingleCharSimpleChoice.value.fget(self)
        if i in self._simple:
            return i
        elif self._is_choice_index(i):
            return self._effective_values[int(i) - 1]
        elif not self._do_validate:
            return i
        else:
            raise InternalError('SpecifiedChoice: strange input: ' +
                                self._input)

    @property
    def raw_value(self):
        i = SingleCharSimpleChoice.value.fget(self)
        if (i in self._simple or self._is_choice_index(i) or not
                self._do_validate):
            return i
        else:
            raise InternalError('SpecifiedChoice: strange input: ' +
                                self._input)

    @property
    def index(self):
        i = self._input
        return int(i) - 1 if self._is_choice_index(i) else -1

    def add_choice(self, new):
        self._choices.append(new)
        num = len(self._choices)
        self._numbers.append(num)
        self.add_element(num)

    @property
    def _effective_values(self):
        return self._values or self._choices


class LoopingInput(object):
    def __init__(self, terminate='q', overwrite=True, dispatch=[],
                 raise_quit=False, **kw):
        self._terminate = terminate
        self._overwrite = overwrite
        self._dispatch = dict(dispatch)
        self._raise_quit = raise_quit
        self._force_terminate = False

    def read(self):
        self._remove_text |= self._overwrite
        while True:
            value = super(LoopingInput, self).read()
            if value == self._terminate:
                    break
            elif isinstance(value, str) and value in self._dispatch:
                self._dispatch[value]()
            self.process()
            if self._force_terminate:
                break
        if self._overwrite and not input_queue.suppress_output:
            terminal.push(self.prompt)
            terminal.push()
        if self._raise_quit:
            raise UserInputTerminated()
        else:
            return self.loop_value

    def process(self):
        pass

    @property
    def loop_value(self):
        return None


class CheckboxList(LoopingInput, SpecifiedChoice):
    def __init__(self, elements, initial=None, colors=None, simple=[], **kw):
        self._lines = list(map(str, elements))
        LoopingInput.__init__(self, **kw)
        simple = list(set(['q', 'a'] + simple))
        kw.setdefault('enter', 'q')
        kw.setdefault('newline', False)
        SpecifiedChoice.__init__(self, self._lines, simple=simple,
                                 **kw)
        self._states = initial or [0] * len(elements)
        t = terminal
        self._colors = colors or [t.white + t.bg_red, t.black + t.bg_green]

    @property
    def prompt(self):
        text_post = copy.copy(self._text_post)
        text_post[-1] += self.input_hint_string
        col = lambda c: ColorString(' {} '.format(str(c+1)),
                                    self._colors[self._states[c]])
        return (self._text_pre + [[' ', col(i), ' ', el] for i, el in
                                  enumerate(self._lines)] + text_post)

    def process(self):
        if self._input.isdigit():
            self._toggle(int(self._input) - 1)
        elif self._input == 'a':
            self._toggle_all()

    @property
    def loop_value(self):
        return self._states

    def _toggle(self, index):
        self._states[index] += 1
        self._states[index] %= len(self._colors)

    def _toggle_all(self):
        for index in range(len(self._states)):
            self._toggle(index)


def confirm(message, remove_text=False):
    message = [str(message)] + ['Press return to continue.']
    SingleCharSimpleChoice([''], text=message, remove_text=remove_text).read()
