import inspect
import textwrap


class glsl(object):
    def __init__(self, ret=None, params=None):
        super(glsl, self).__init__()
        self.ret = ret or 'void'
        self.params = params or []
        self.fn = None

    def __call__(self, fn):
        fn._glsl_decorator = self
        self.fn = fn
        return fn

    def signature(self):
        # inspect the function's parameters and get their names
        return '{ret} {name}({params})'.format(
            ret=self.ret,
            name=self.fn.__name__,
            params=', '.join(self.parameters()),
        )

    def _arguments(self):
        # get the arguments but ignore self
        return inspect.getargspec(self.fn).args[1:]

    def parameters(self):
        params = [
            '{type} {arg}'.format(type=type, arg=arg)
            for type, arg in zip(self.params, self._arguments())
        ]
        return params

    def source(self, object):
        def fix_indent(text):
            """Re-indents source
            """
            # correct indentation
            #text = textwrap.dedent(text)
            # strip newlines and whitespace from start and end
            text = text.strip()
            # re-indent 4 spaces
            text = '\n'.join([
                '    ' + line.strip()
                for line in text.split('\n')
            ])
            return text

        # call the function with empty parameters
        # we have to handle functions returning None
        args = [object] + [None] * len(self._arguments())
        source = self.fn(*args) or ''
        source = str(source)
        source = fix_indent(source)

        return '{signature}\n{{\n{source}\n}}'.format(
            signature=self.signature(),
            source=source,
        )