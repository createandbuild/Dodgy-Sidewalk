def maximum(a,b):
    if a>b:
        return a
    else:
        return b

def minimum(a,b):
    if a>b:
        return b
    else:
        return a

def clamp(number,lower_bound,upper_bound):
    new_num = number
    new_num = maximum(lower_bound,new_num)
    new_num = minimum(upper_bound,new_num)
    return new_num
