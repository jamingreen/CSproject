def apply(ls: list, func, **args) -> list:
    """
    Apply a function to items in a list with optional arguments

    Args:
        ls (list): list to be applying to
        func (Function): function to apply
        **args: list of arguments to be passed to

    Returns:
        list: The list with function applied to each element
    """
    result = []
    argument = ""
    for key, value in args.items():
        argument = argument + ", " + str(key) +"="+str(value)
    argument = argument + ")"
    for i in ls:
        com = f"x = {func.__name__}({ i }" + argument
        loc = {}
        exec(f"{com}",globals(),loc)
        x = loc["x"]
        result.append(x)
    return result

a = [1.325235, 3242.723432, 100_100_100.2151365, 10.2156234]

answer = apply(a, round, ndigits = 4)
answer1 = list(round(x, ndigits = 4) for x in a)

print(answer)
print(answer1)