import textwrap
from omgl.gl import glsl_version

"""
def glsl(fn):
    fn._glsl_function = True
    if not hasattr(fn, '_glsl_return'):
        fn._glsl_return = 'void'
    if not hasattr(fn, '_glsl_args'):
        fn._glsl_args = []
    return fn

def glsl_ret(ret):
    def wrapper(fn):
        fn._glsl_function = True
        fn._glsl_ret = ret
        return fn
    return wrapper

def glsl_args(*args):
    def wrapper(fn):
        fn._glsl_function = True
        fn._glsl_args = args
        return fn
    return wrapper


"""
class glsl(object):
    def __init__(self, ret=None, args=None, name=None, glsl_gt=None, glsl_lt=None, glsl_gteq=None, glsl_lteq=None, glsl_eq=None):
        super(glsl, self).__init__()
        self.ret = ret or 'void'
        self.args = args or []
        self.fn = None
        self.name = name

        self.glsl_gt = glsl_gt
        self.glsl_lt = glsl_lt
        self.glsl_gteq = glsl_gteq
        self.glsl_lteq = glsl_lteq
        self.glsl_eq = glsl_eq

    def meets_glsl_version(self):
        v = glsl_version()
        if self.glsl_gt and self.glsl_gt <= v:
            return False
        if self.glsl_lt and self.glsl_lt >= v:
            return False
        if self.glsl_gteq and self.glsls_gteq < v:
            return False
        if self.glsl_lteq and self.glsl_lteq > v:
            return False
        if self.glsl_eq and self.glsl_eq != v:
            return False
        return True

    def __call__(self, fn):
        fn._glsl_decorator = self
        self.fn = fn
        return fn

    def signature(self):
        # inspect the function's parameters and get their names
        return '{ret} {name}({args})'.format(
            ret=self.ret,
            #name=self.fn.__name__,
            name=self.name or self.fn.__name__,
            args=', '.join(self.arguments()),
        )

    def arguments(self):
        args = [
            arg
            for arg in self.args
        ]
        return args

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
        #args = [object] + [None] * len(self._arguments())
        source = self.fn(object) or ''
        source = fix_indent(str(source))

        return '{signature}\n{{\n{source}\n}}'.format(
            signature=self.signature(),
            source=source,
        )
