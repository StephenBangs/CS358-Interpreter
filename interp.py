#Stephen Bangs
#4/24/25
#Dr. Yao Li - CS358
#Milestone 1 - Interpreter Implementation Project

#literals

class Lit:
    def __init__(self, value):
        self.value = value

class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Sub:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Mul:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Div:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Neg:
    def __init__(self, expr):
        self.expr = expr

class And:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Or:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Not:
    def __init__(self, expr):
        self.expr = expr

class Let:
    def __init__(self, name, value_expr, body_expr):
        self.name = name
        self.value_expr = value_expr
        self.body_expr = body_expr

class Name:
    def __init__(self, name):
        self.name = name

class Eq:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Lt:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class If:
    def __init__(self, cond, then_branch, else_branch):
        self.cond = cond
        self.then_branch = then_branch
        self.else_branch = else_branch

# Domain-specific AST nodes for strings
class StrLit:
    def __init__(self, value):
        self.value = value

class Concat:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Replace:
    def __init__(self, source, old, new):
        self.source = source
        self.old = old
        self.new = new


# --- Evaluation Logic ---
def eval(expr, env={}):
    match expr:
        case Lit(value=value):
            return value
        case StrLit(value=value):
            return value
        case Add(left=l, right=r):
            lval, rval = eval(l, env), eval(r, env)
            if type(lval) is int and type(rval) is int: return lval + rval
            raise Exception("Add: operands must be integers")
        case Sub(left=l, right=r):
            lval, rval = eval(l, env), eval(r, env)
            if type(lval) is int and type(rval) is int: return lval - rval
            raise Exception("Sub: operands must be integers")
        case Mul(left=l, right=r):
            lval, rval = eval(l, env), eval(r, env)
            if type(lval) is int and type(rval) is int: return lval * rval
            raise Exception("Mul: operands must be integers")
        case Div(left=l, right=r):
            lval, rval = eval(l, env), eval(r, env)
            if type(lval) is int and type(rval) is int:
                if rval == 0: raise Exception("Division by zero")
                return lval // rval
            raise Exception("Div: operands must be integers")
        case Neg(expr=e):
            val = eval(e, env)
            if type(val) is int: return -val
            raise Exception("Neg: operand must be integer")
        case And(left=l, right=r):
            lval = eval(l, env)
            if type(lval) is bool:
                return lval and eval(r, env) if lval else False
            raise Exception("And: operands must be booleans")
        case Or(left=l, right=r):
            lval = eval(l, env)
            if type(lval) is bool:
                return True if lval else eval(r, env)
            raise Exception("Or: operands must be booleans")
        case Not(expr=e):
            val = eval(e, env)
            if type(val) is bool: return not val
            raise Exception("Not: operand must be boolean")
        case Let(name=name, value_expr=val_expr, body_expr=body):
            val = eval(val_expr, env)
            new_env = env.copy(); new_env[name] = val
            return eval(body, new_env)
        case Name(name=n):
            if n in env: return env[n]
            raise Exception(f"Unbound name: {n}")
        case Eq(left=l, right=r):
            lval, rval = eval(l, env), eval(r, env)
            return type(lval) == type(rval) and lval == rval
        case Lt(left=l, right=r):
            lval, rval = eval(l, env), eval(r, env)
            if type(lval) is int and type(rval) is int: return lval < rval
            raise Exception("Lt: operands must be integers")
        case If(cond=b, then_branch=t, else_branch=e):
            cond = eval(b, env)
            if type(cond) is not bool: raise Exception("If: condition must be boolean")
            return eval(t, env) if cond else eval(e, env)
        case Concat(left=l, right=r):
            lval, rval = eval(l, env), eval(r, env)
            if isinstance(lval, str) and isinstance(rval, str): return lval + rval
            raise Exception("Concat: operands must be strings")
        case Replace(source=s, old=o, new=n):
            s_val, o_val, n_val = eval(s, env), eval(o, env), eval(n, env)
            if all(isinstance(x, str) for x in (s_val, o_val, n_val)):
                return s_val.replace(o_val, n_val, 1)
            raise Exception("Replace: operands must be strings")
        case _:
            raise Exception(f"Unknown expression: {expr}")


# --- Runner ---
def run(expr):
    result = eval(expr)
    print(result)

# --- Domain Description and Test Cases ---
"""
Domain: Strings
This DSL enables basic string manipulation. It supports:
- Quoted string literals (StrLit)
- Concatenation (Concat)
- First substring replacement (Replace)
"""

# --- Tests ---
run(Concat(StrLit("hello"), StrLit(" world")))
run(Replace(StrLit("fizzbuzz"), StrLit("buzz"), StrLit("bang")))
run(If(Eq(Lit(3), Lit(3)), StrLit("equal"), StrLit("not equal")))
run(Let("x", StrLit("abc"), Concat(Name("x"), StrLit("def"))))
run(Mul(Lit(3), Lit(4)))
