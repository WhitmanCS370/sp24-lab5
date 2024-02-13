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

def do_print(env,args):
    assert len(args)>=0
    for item in args:
        print(do(env,item),end=" ")
    print()

def do_repeat(env,args):
    assert len(args)==2
    assert isinstance(args[0],int)
    assert args[0]>0
    for i in range(args[0]):
        result=do(env,args[1])
    return result

def do_equal(env,args):
    assert len(args)==2
    assert isinstance(args[0],type(args[1]))
    return args[0]==args[1]

def do_leq(env,args):
    assert len(args)==2
    assert isinstance(args[0],type(args[1]))
    return args[0]<=args[1]

def do_geq(env,args):
    assert len(args)==2
    assert isinstance(args[0],type(args[1]))
    return args[0]>=args[1]

def do_if(env,args):
    assert len(args)==3
    if args[0]:
        value=do(env,args[1])
    else:
        value=do(env,args[2])
    return value

def do_array(env,args):
    assert isinstance(args[0],str)
    assert args[0] > 0
    return [0]*args[0]


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
    if isinstance(expr, int) or isinstance(expr,str):
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
