# import math
import ast
import operator as op

class MathParser:
    """ 
    Basic parser with local variable
    
    Args:
       vars (mapping): mapping object where obj[name] -> numerical value 
       
    Example:
       
        data = {'x': 3.4}
        parser=MathParser(data)
        expr='x**2+2*x+1'
        result = parser.parse(expr)
    """
        
    _operators2method = {
        ast.Add: op.add, 
        ast.Sub: op.sub, 
        ast.Mult: op.mul,
        ast.Div:  op.truediv,
        ast.Pow:  op.pow,
        ast.FloorDiv: op.floordiv,              
        ast.USub: op.neg, 
        ast.UAdd: lambda a:a  
    }
    
    def __init__(self, vars=None):
        self._vars = vars
        
    def _Name(self, name): 
        if self._vars is None :
            raise NameError(f"Variable {name!r} is not provided.")
        else:
            try: 
                return  self._vars[name]
            except KeyError:
                raise NameError(f"Variable {name!r} is not provided.")
                
    def eval_(self, node):
        if isinstance(node, ast.Expression):
            return self.eval_(node.body)
        if isinstance(node, ast.Num): # <number>
            return node.n
        if isinstance(node, ast.Name): # <variable>
            return self._Name(node.id) 
        if isinstance(node, ast.BinOp):            
            method = self._operators2method[type(node.op)]                      
            return method( self.eval_(node.left), self.eval_(node.right) )            
        if isinstance(node, ast.UnaryOp):             
            method = self._operators2method[type(node.op)]  
            return method( self.eval_(node.operand) )        
        else:
            raise TypeError(node)
    
    def parse(self, expr,vars=None):
        if vars != None:
            self._vars=vars

        return  self.eval_(ast.parse(expr, mode='eval')) 