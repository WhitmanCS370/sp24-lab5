"""A tiny expression evaluator with variables."""
import json
import sys

def do_abs(env, args):
    assert len(args) == 1
    val = do(env, args[0])
    return abs(val)

def do_add(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left + right

def do_get(env, args):
    assert len(args) == 1
    assert isinstance(args[0], str)
    assert args[0] in env, f"Unknown variable {args[0]}"
    return env[args[0]]

def do_seq(env, args):
    assert len(args) > 0
    for item in args:
        result = do(env, item)
    return result

def do_set(env, args):
    assert len(args) == 2
    assert isinstance(args[0], str)
    value = do(env, args[1])
    env[args[0]] = value
    return value

def do_print(env, args):
    """["print", arg1, arg2]"""
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    print(str(left) + " " + str(right))

def do_repeat(env, args):
    """["repeat", count, loop_body]"""
    assert len(args) == 2
    count = do(env, args[0])
    for i in range(count):
        x = do(env, args[1])
    return x

def do_equal(env, args):
    """["equal", X, Y]"""
    assert len(args) == 2
    x = do(env, args[0])
    y = do(env, args[1])
    return x == y

def do_leq(env, args):
    assert len(args) == 2
    x = do(env, args[0])
    y = do(env, args[1])
    return x <= y

def do_geq(env, args):
    assert len(args) == 2
    x = do(env, args[0])
    y = do(env, args[1])
    return x >= y

def do_if(env, args):
    """["if", boolean_predicate, then_command, else_command]"""
    """boolean check, then this, or else this"""
    
    assert len(args) > 0
    boolean_predicate = do(env, args[0])        # should give true or false value.
    if boolean_predicate:
        do(env, args[1])
    else:
        do(env, args[2])

# [lookup]
OPS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}
# [/lookup]

# [do]
def do(env, expr):
    # Integers evaluate to themselves.
    if isinstance(expr, int):
        return expr
    
    if isinstance(expr, str):
        return expr

    # Lists trigger function calls.
    assert isinstance(expr, list)
    assert expr[0] in OPS, f"Unknown operation {expr[0]}"
    func = OPS[expr[0]]
    return func(env, expr[1:])
# [/do]

def main():
    assert len(sys.argv) == 2, "Usage: vars_reflect.py filename"
    with open(sys.argv[1], "r") as reader:
        program = json.load(reader)
    result = do({}, program)
    print(f"=> {result}")

if __name__ == "__main__":
    main()
