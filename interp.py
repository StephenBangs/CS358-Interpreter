#Stephen Bangs
#4/24/25
#Dr. Yao Li - CS358
#Milestone 1 - Interpreter Implementation Project

# interp.py (Milestone 1, dataclass version)

from dataclasses import dataclass

# --- Expression Types ---

@dataclass
class Lit:
    value: int | bool

@dataclass
class Add:
    left: 'Expr'
    right: 'Expr'

@dataclass
class Sub:
    left: 'Expr'
    right: 'Expr'

@dataclass
class Mul:
    left: 'Expr'
    right: 'Expr'

@dataclass
class Div:
    left: 'Expr'
    right: 'Expr'

@dataclass
class Neg:
    expr: 'Expr'

@dataclass
class And:
    left: 'Expr'
    right: 'Expr'

@dataclass
class Or:
    left: 'Expr'
    right: 'Expr'

@dataclass
class Not:
    expr: 'Expr'

@dataclass
class Let:
    name: str
    value_expr: 'Expr'
    body_expr: 'Expr'

@dataclass
class Name:
    name: str

@dataclass
class Eq:
    left: 'Expr'
    right: 'Expr'

@dataclass
class Lt:
    left: 'Expr'
    right: 'Expr'

@dataclass
class If:
    cond: 'Expr'
    then_branch: 'Expr'
    else_branch: 'Expr'

# --- Domain-specific String Expressions ---

@dataclass
class StrLit:
    value: str

@dataclass
class Concat:
    left: 'Expr'
    right: 'Expr'

@dataclass
class Replace:
    source: 'Expr'
    old: 'Expr'
    new: 'Expr'

Expr = Lit | Add | Sub | Mul | Div | Neg | And | Or | Not | Let | Name | Eq | Lt | If | StrLit | Concat | Replace

# --- Evaluation Logic ---
def eval(expr: Expr, env={}):
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
            if type(lval) is not bool:
                raise Exception("And: left operand must be boolean")
            if not lval:
                return False
            rval = eval(r, env)
            if type(rval) is not bool:
                raise Exception("And: right operand must be boolean")
            return rval
        case Or(left=l, right=r):
            lval = eval(l, env)
            if type(lval) is not bool:
                raise Exception("Or: left operand must be boolean")
            if lval:
                return True
            rval = eval(r, env)
            if type(rval) is not bool:
                raise Exception("Or: right operand must be boolean")
            return rval
        case Not(expr=e):
            val = eval(e, env)
            if type(val) is bool: return not val
            raise Exception("Not: operand must be boolean")
        case Let(name=n, value_expr=val_expr, body_expr=body):
            val = eval(val_expr, env)
            new_env = env.copy(); new_env[n] = val
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
def run(e: Expr) -> None:
    print(f"running {e}")
    try:
        result = eval(e)
        print(f"result: {result}")
    except Exception as err:
        print(f"error: {err}")

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
