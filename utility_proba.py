def uty(y, tetta): #y - количество выходных, tetta = optimum - reality
    return tetta / y

def optimum(days):
    return days * 8

def probability(y, tetta, days):
    optimum_max = optimum(days)
    optimum_min = - optimum(days)
    utility_std = (uty(y, tetta) - optimum_min) / (optimum_max - optimum_min)
    return utility_std