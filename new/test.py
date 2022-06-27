def apply(list, func, **args):
    result = []
    argument = ""
    for key, value in args.items():
        argument = argument + ", " + str(key) +"="+str(value)
    argument = argument + ")"
    for i in list:
        com = f"x = {func}({ i }" + argument
        loc = {}
        print(com)
        exec(f"{com}",globals(),loc)
        x = loc["x"]
        result.append(x)
    return result

def func(num, num1):
    return num * num1 +33

a = [1.11231231, 2.6121535, 3.342735, 4.7125135, 5.9]

b = apply(a, "round", ndigits = 3)

newB = []
for num in b:
    x = round(num, ndigits = 3)
    newB.append(x)
print(newB)

print(b)