"""

CIS 211: Project 3
Bernardo Izquierdo-Rodriguez

"""

# One global environment (scope) for
# the calculator

ENV = dict()

def env_clear():
    """Clear all variables in calculator memory"""
    global ENV
    ENV = dict()

class Expr(object):
    """Abstract base class of all expressions."""

    def eval(self) -> "IntConst":
        """Implementations of eval should return an integer constant."""
        raise NotImplementedError("Each concrete Expr class must define 'eval'")

    def __str__(self) -> str:
        """Implementations of __str__ should return the expression in algebraic notation"""
        raise NotImplementedError("Each concrete Expr class must define __str__")

    def __repr__(self) -> str:
        """Implementations of __repr__ should return a string that looks like
        the constructor, e.g., Plus(IntConst(5), IntConst(4))
        """
        raise NotImplementedError("Each concrete Expr class must define __repr__")

    def __eq__(self, other: "Expr") -> bool:
        """ Implementationn of __eq__ should return a boolean. """
        raise NotImplementedError("__eq__ method not defined for class")

class IntConst(Expr):

    def __init__(self, value: int):
        self.value = value

    def eval(self) -> 'IntConst':
        return IntConst(self.value)

    def __str__(self) -> str:
        return f"{self.value}"

    def __repr__(self) -> str:
        return f"IntConst({self.value})"

    def __eq__(self, other: Expr) -> bool:
        return isinstance(other, IntConst) and self.value == other.value

class BinOp(Expr):
    """Abstract base class for binary operators +, *, /, -"""
    def __init__(self, left: int, right: int):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        """Implementations of __str__ should return the expression in algebraic notation"""
        return f"({str(self.left)} {self.opsym} {str(self.right)})"

    def __repr__(self) -> str:
        """Implementations of __repr__ should return a string that looks like
        the constructor, e.g., Plus(IntConst(5), IntConst(4))
        """
        return f"{self.opname}({repr(self.left)}, {repr(self.right)})"

    def __eq__(self, other: "Expr") -> bool:
        return type(self) == type(other) and  \
            self.left == other.left and \
            self.right == other.right

    def eval(self) -> "IntConst":
        """Each concrete subclass must define _apply(int, int)->int"""
        left_val = self.left.eval()
        right_val = self.right.eval()
        return IntConst(self._apply(left_val.value, right_val.value))

class Plus(BinOp):
    """left + right"""

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right)
        self.opsym = "+"
        self.opname = "Plus"

    def _apply(self, left: int, right: int) -> int:
        return left + right

class Minus(BinOp):
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right)
        self.opsym = "-"
        self.opname= "Minus"

    def _apply(self, left: int, right: int) -> int:
        return left - right

class Times(BinOp):
    """left * right"""

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right)
        self.opsym = "*"
        self.opname= "Times"

    def _apply(self, left: int, right: int) -> int:
        return left * right

class Div(BinOp):
    """left / right"""

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right)
        self.opsym = "/"
        self.opname= "Div"

    def _apply(self, left: int, right: int) -> int:
        return left // right

class Unop(Expr):
    """Abstract base class for unary operators ~, @"""
    def __init__(self, left: int):
        self.left = left

    def __str__(self) -> str:
        """Implementations of __str__ should return the expression in algebraic notation"""
        return f"({self.opsym}{str(self.left)})"

    def __repr__(self) -> str:
        """Implementations of __repr__ should return a string that looks like
        the constructor, e.g., Plus(IntConst(5), IntConst(4))
        """
        return f"{self.opname}({repr(self.left)})"

    def __eq__(self, other: "Expr") -> bool:
        return type(self) == type(other) and \
               self.left == other.left

    def eval(self) -> "IntConst":
        """Each concrete subclass must define _apply(int, int)->int"""
        left_val = self.left.eval()
        return IntConst(self._apply(left_val.value))

class Abs(Unop):
    """ |left| """
    def __init__(self, left: int):
        self.left = left
        self.opsym = "@"
        self.opname = "Abs"

    def _apply(self, left: int) -> int:
        """ returns the absolute value of integer """
        return abs(left)

class Neg(Unop):
    """ -Left """
    def __init__(self, left: int):
        self.left = left
        self.opsym = "~"
        self.opname = "Neg"

    def _apply(self, left: int) -> int:
        """ Negates an integer"""
        return -(left)

class UndefinedVariable(Exception):
    """Raised when expression tries to use a variable that
    is not in ENV
    """
    pass

class Var(Expr):

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Var({self.name})"

    def eval(self):
        global ENV
        if self.name in ENV:
            return ENV[self.name]
        else:
            raise UndefinedVariable(f"{self.name} has not been assigned a value")

    def assign(self, value: IntConst):
        """ Assigns value to variable"""
        ENV[self.name] = value

class Assign(Expr):
    """Assignment:  x = E represented as Assign(x, E)"""

    def __init__(self, left: Var, right: Expr):
        assert isinstance(left, Var)  # Can only assign to variables!
        self.left = left
        self.right = right

    def eval(self) -> IntConst:
        r_val = self.right.eval()
        self.left.assign(r_val)
        return r_val

    def __str__(self) -> str:
        return f"{self.left} = {self.right}"

    def __repr__(self) -> str:
        return f"Assign({self.left}, {self.right})"
