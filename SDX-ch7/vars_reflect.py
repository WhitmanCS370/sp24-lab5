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
    result = ""
    for item in args:
        if isinstance(item, str):
            result += item + " "
        else:
            value = do(env, item)
            result += str(value) + " "
    print(result)

def do_repeat(env, args):
    assert isinstance(args[0], int)
    for i in range(0, args[0]):
        do(env, args[1])

def do_leq(env, args):
    val1 = do(env, args[0])
    val2 = do(env, args[1])
    return val1 <= val2

def do_equal(env, args):
    val1 = do(env, args[0])
    val2 = do(env, args[1])
    return val1 == val2   

def do_geq(env, args):
    val1 = do(env, args[0])
    val2 = do(env, args[1])
    return val1 >= val2

def do_if(env, args):
    if do(env, args[0]):
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

    # Lists trigger function calls.
    assert isinstance(expr, list)
    assert expr[0] in OPS, f"Unknown operation {expr[0]}"
    func = OPS[expr[0]]
    val = func(env, expr[1:])
    if sys.argv[1] == "--trace":
        print(val)
    return val
# [/do]

def main():
    i = 1
    assert len(sys.argv) >= 2, "Usage: vars_reflect.py filename"
    if len(sys.argv) >= 2:
        i = 2
    with open(sys.argv[i], "r") as reader:
        program = json.load(reader)
    result = do({}, program)
    print(f"=> {result}")

if __name__ == "__main__":
    main()
