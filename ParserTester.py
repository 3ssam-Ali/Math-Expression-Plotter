from MathParser import Expression
for expr in (
    '2**4',                      
    '1 + 2*3**(4//5) // (6 + -7)',
    '7 + 9 * (2 + 2)',           
    '6 // 2 + 0.0',              
    '2+3',                       
    '6+4/2*2',                   
    '3+2.45/8',                  
    '3**3*3/3+3',                
    '2',                         
    'x+50',                      
    'x**2',                      
):
    x=5
    try:
        realResult=eval(expr)
        ParsedResult=Expression(expr).solve({'x':x})
        ok = (realResult == ParsedResult and type(realResult) == type(ParsedResult))
        print("{} {} = {}".format("OK!" if ok else "FAIL!", expr, ParsedResult))
    except Exception as e:
        print(f'Error with expression: {expr} |', e)
    
