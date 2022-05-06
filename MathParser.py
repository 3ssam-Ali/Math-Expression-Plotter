import ast
import operator as op


class Expression:
    """ 
    Basic Expression Class with local Parser and variables

    Args:
    ----
       _vars (mapping): mapping Variables or Objects where obj[name] -> numerical value 
       astcode : the syntax tree representation for the expression

    Functions:
    ---------
       solve(vars:dict) -> float|int :
            solve the expression given the values of the variables in it and return the result

    Example:
    -------
        data = {'x': 3.4}\n
        expr=expression('x**2+2*x+1')\n 
        result = expr.solve(data)
    """

    _operators2method = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div:  op.truediv,
        ast.Pow:  op.pow,
        ast.FloorDiv: op.floordiv,
        ast.USub: op.neg,
        ast.UAdd: lambda a: a
    }

    def __init__(self, expr: str):
        if not self.checkValid(expr):
            raise ValueError(f"Not a valid algebraic expression: {expr}.")
        else:
            try:
                self.astCode = ast.parse(expr, mode='eval')
            except SyntaxError as se:
                raise se  # need to be modified to be clearer

    def checkValid(self, expr: str) -> bool:
        '''
        checks if the string contains only valid characters

        Parameters:
            expr (str): A string mathimatical expression

        Returns:
            bool: True if the expression is valid
        '''
        validChars = '1234567890+-/*x() '
        if any([c not in validChars for c in expr]):
            return False
        else:
            return True

    def _Name(self, name):
        '''
        Return the numerical value of a variable

        parameters:
            name(str): the ID of the variable

        '''
        if self._vars is None:
            raise NameError(f"Variable {name!r} is not provided.")
        else:
            try:
                return self._vars[name]
            except KeyError:
                raise NameError(f"Variable {name!r} is not provided.")

    def _eval(self, node):
        if isinstance(node, ast.Expression):
            return self._eval(node.body)
        if isinstance(node, ast.Num):  # <number>
            return node.n
        if isinstance(node, ast.Name):  # <variable>
            return self._Name(node.id)
        if isinstance(node, ast.BinOp):
            method = self._operators2method[type(node.op)]
            return method(self._eval(node.left), self._eval(node.right))
        if isinstance(node, ast.UnaryOp):
            method = self._operators2method[type(node.op)]
            return method(self._eval(node.operand))
        else:
            raise TypeError(node)

    def solve(self, vars: dict):
        '''
        Return the result of solving the expression provided the values of the variables

        Parameters:
        ----------
            vars(dict) : a dictionary mapping the variable to it's numerical data
                for example {'x':12}

        Example:
            data = {'x': 3.4}\n
            expr=expression('x**2+2*x+1')\n 
            result = expr.solve(data)

            result2 = expr.solve({x:31})
        '''
        self._vars = vars
        return self._eval(self.astCode)