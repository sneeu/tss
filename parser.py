from eflexer import Lexer
from sorted_dict import SortedDict


def _strip_whitespace(s):
    return s.strip(' \t\n')


def _property_list(scanner, token):
    properties = [
        t.split(':')
        for t in token.strip('{} \t\n').split(';')]
    r = []
    for prop in properties:
        if len(prop) == 2:
            r.append([_strip_whitespace(p) for p in prop])
    return r


def _extends(scanner, token):
    return [_strip_whitespace(t) for t in token.strip('()').split(',')]


def _selector_list(scanner, token):
    return _strip_whitespace(token)


class _Selector(object):
    def __init__(self, selector, abstract=False, new_properties=None):
        self.selector = selector
        self.abstract = abstract
        self.new_properties = new_properties
        self.extended_properties = None

    def _get_properties(self):
        props = {}
        if self.extended_properties:
            props = self.extended_properties
        if self.new_properties:
            for key, val in self.new_properties:
                props[key] = val
        return props

    def _set_properties(self, val):
        self.new_properties = val

    properties = property(_get_properties, _set_properties)

    def __str__(self):
        if self.abstract:
            return ''
        return '%s {\n%s\n}' % (self.selector, '\n'.join(['\t%s: %s;' % p for p in self.properties.items()]))


def parse(pcss):
    SELECTOR = '([a-z0-9#\.\-_ \t\n]+)'
    SELECTOR_LIST = SELECTOR + '(, ' + SELECTOR + ')*'

    K_ABSTRACT = 'KEYWORD_ABSTRACT'
    T_SELECTOR = 'SELECTOR'
    T_PROPERTY_LIST = 'PROPERTY_LIST'
    T_EXTENDS = 'EXTENDS'

    rules = (
        (K_ABSTRACT,
            r'abstract'),
        (T_SELECTOR,
            (SELECTOR_LIST, _selector_list)),
        (T_PROPERTY_LIST,
            (r'\{([^\}]*)\}', _property_list)),
        (T_EXTENDS,
            (r'\(%s\)' % SELECTOR_LIST, _extends))
    )

    lex = Lexer(rules, case_sensitive=False)

    next_is_abstract = False
    previous_selector = None
    selectors = SortedDict()

    for token, value in lex.scan(_strip_whitespace(pcss)):
        if token == K_ABSTRACT:
            next_is_abstract = True
        if token == T_SELECTOR:
            selectors[value] = _Selector(value, next_is_abstract)
            previous_selector = value
            next_is_abstract = False
        if token == T_PROPERTY_LIST:
            selectors[previous_selector].properties = value
        if token == T_EXTENDS:
            props = {}
            for selector in value:
                for prop, val in selectors[selector].properties.items():
                    props[prop] = val
            selectors[previous_selector].extended_properties = props

    for __, selector in selectors.items():
        if not selector.abstract:
            print selector


if __name__ == '__main__':
    import sys
    pcss = ''.join(sys.stdin.readlines())
    parse(pcss)
