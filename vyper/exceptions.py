import types

from vyper.settings import (
    VYPER_ERROR_CONTEXT_LINES,
    VYPER_ERROR_LINE_NUMBERS,
)


# Attempts to display the line and column of violating code.
class ParserException(Exception):
    def __init__(self, message='Error Message not found.', item=None):
        self.message = message
        self.lineno = None
        self.col_offset = None

        if isinstance(item, tuple):  # is a position.
            self.lineno, self.col_offset = item[:2]
        elif item and hasattr(item, 'lineno'):
            self.set_err_pos(item.lineno, item.col_offset)
            if hasattr(item, 'full_source_code'):
                self.source_code = item.full_source_code

    def set_err_pos(self, lineno, col_offset):
        if not self.lineno:
            self.lineno = lineno

            if not self.col_offset:
                self.col_offset = col_offset

    def __str__(self):
        lineno, col_offset = self.lineno, self.col_offset

        if lineno is not None and hasattr(self, 'source_code'):
            from vyper.utils import annotate_source_code

            source_annotation = annotate_source_code(
                self.source_code,
                lineno,
                col_offset,
                context_lines=VYPER_ERROR_CONTEXT_LINES,
                line_numbers=VYPER_ERROR_LINE_NUMBERS,
            )
            col_offset_str = '' if col_offset is None else str(col_offset)
            return f'line {lineno}:{col_offset_str} {self.message}\n{source_annotation}'

        elif lineno is not None and col_offset is not None:
            return f'line {lineno}:{col_offset} {self.message}'

        return self.message


class PythonSyntaxException(ParserException):
    """
    Invalid syntax.

    This error is converted from errors raised during ast.parse
    """
    def __init__(self, syntax_error: SyntaxError, source_code: str):
        item = types.SimpleNamespace()  # TODO: Create an actual object for this
        item.lineno = syntax_error.lineno
        item.col_offset = syntax_error.offset
        item.full_source_code = source_code
        super().__init__(message=f'SyntaxError: {syntax_error.msg}', item=item)


class SyntaxException(ParserException):
    """Valid Python syntax, but invalid Vyper syntax."""


class StructureException(ParserException):
    """TODO"""


class InvalidLiteralException(ParserException):
    """Invalid literal value."""


class InvalidTypeException(ParserException):
    """Invalid type declaration."""


class VariableDeclarationException(ParserException):
    """Invalid variable declaration."""


class FunctionDeclarationException(ParserException):
    """Invalid function declaration."""


class EventDeclarationException(ParserException):
    """Invalid event declaration."""


class TypeMismatchException(ParserException):
    """TODO"""


class ConstancyViolationException(ParserException):
    """State-changing action inside a constant function."""


class NonPayableViolationException(ParserException):
    """Used msg.value in a nonpayable function."""


class VersionException(ParserException):
    """Version string is malform or incompatible with this version of Vyper."""


class ArrayIndexException(ParserException):
    """Array index out of range."""


class ZeroDivisionException(ParserException):
    """Second argument to a division or modulo operation was zero."""


class EvmVersionException(ParserException):
    """Cannot perform an action based on the active EVM ruleset."""


class CompilerPanic(Exception):

    """Unexpected error during compilation."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message + ' Please create an issue.'


class JSONError(Exception):

    """Invalid compiler input JSON."""

    def __init__(self, msg, lineno=None, col_offset=None):
        super().__init__(msg)
        self.lineno = lineno
        self.col_offset = col_offset
