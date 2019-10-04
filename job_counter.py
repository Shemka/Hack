def hours(days):
    return days * 8


# weekends - [start, end] or None
def count_for_driver(week_part, days, budni, weekends=None):
    
    allow_jobs = None
    jobs = {
        8: [5, 13, 14, 15, 18, 19, 20, 21, 25],
        9: [1, 2, 3, 6, 7, 8, 9, 11, 16],
        10: [4, 12, 22, 24, 26, 28, 29, 55, 56, 57]
    }

    if week_part == 0:
        allow_jobs = [1, 2, 3, 4, 5, 6, 9, 22, 24, 25, 26, 28, 7, 8, 11, 25, 12, 56, 57]
        idx = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 3, 3, 3]
    elif week_part == 1:
        allow_jobs = [14, 22, 24, 26, 28, 13, 15, 16, 56, 57]
        idx = [0, 0, 0, 0, 0, 1, 1, 1, 2, 2]
    elif week_part == 2:
        allow_jobs = [18, 24, 26, 28, 29, 55, 19, 20, 21, 56, 57]
        idx = [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2]
    else:
        print('Poshel v zad')
        return None
    
    optimum = hours(budni)
    print(optimum)
    if weekends is None:
        weekends = 0
    else:
        weekends = len([x for x in range(weekends[0], weekends[1]+1)])
    days -= weekends

    now_max = optimum // 10
    optimum = optimum % 10

    now_max += optimum // 9
    optimum = optimum % 9

    now_max += optimum // 8
    optimum = optimum % 8
    
    if optimum != 0:
        now_max += 1
        optimum -= 8
    

    print(days - now_max)
    





    

def count_for_worker(week_part, weekends, days):
    jobs = {
        8: [5, 13, 14, 15, 18, 19, 20, 21],
        9: [1, 2, 3, 6, 7, 8, 9, 11, 16],
        10: [4, 12, 22, 24, 26, 28, 29, 55, 56, 57]
    }
    if week_part == 0:
        allow_jobs = [1, 2, 3, 4, 5, 6, 9, 22, 24, 26, 28, 7, 8, 11, 12, 56, 57]
        idx = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 3, 3, 3]
    elif week_part == 1:
        allow_jobs = [14, 22, 24, 26, 28, 13, 15, 16, 56, 57]
        idx = [0, 0, 0, 0, 0, 1, 1, 1, 2, 2]
    elif week_part == 2:
        allow_jobs = [18, 24, 26, 28, 29, 55, 19, 20, 21, 56, 57]
        idx = [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2]
    else:
        print('Poshel v zad')
        return None
    
