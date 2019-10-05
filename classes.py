# -----------------------------------------------------------
# Action class where define operations under <actions_object>
# -----------------------------------------------------------
class Actions:
    def __init__(self, actions_set):
        self.actions_set = actions_set
        
    def remove_action(self, action):
        self.actions_set.remove(action)
        
    def actions(self):
        return self.actions_set

    
    
# -------------------------------    
# Environment where algorithm attract
# n = count of personal
# c = number of days in month
# days_idx = [0, 1, 2 ... ] (usuall day, saturday, sunday)
# days_before = 5 days before this month
# -------------------------------
class Environment:
    def __init__(self, n, c, days_idx, days_before):
        self.size = (c, n)
        self.table = np.zeros(self.size)
        self.now_pos = [0, 0]
        self.days_idx = list(map(int, days_idx))
        self.days_before = days_before
    
    # position = (start_day, end_date)
    def add_holiday(self, y, position):
        self.table[self.now_pos[0]][position[0]-1:position[1]-1] = 'О'
    
    def how_to_move(self):
        if self.now_pos[1] == self.size[1]-1 and self.now_pos[0] != self.size[0]-1:
            self.now_pos[0] += 1
            self.now_pos[1] = 0
            return True
        else:
            return 'Kavabanga'
        
    # Add element to now sequence
    # Return True or False depends on is table is full
    def add_element(self, element):
        if self.table[self.now_pos[0]][self.now_pos[1]] == 'О':
            moves = self.how_to_move()
            if moves == 'Kavabanga':
                return True
            else:
                self.add_element(element)
        else:
            self.table[self.now_pos[0]][self.now_pos[1]] = element
            moves = self.how_to_move()
            if moves == 'Kavabanga':
                return True
            else:
                return False

            
            
# ----------------------------------------           
# Tester class test had already made table
# surface = table
# size = size of surface looks like (n, c) where n = count of employers,  c = number of days in month
# w_d = True or False (True if it is drivers and False if it's not)
# days_idx = [0, 1, 2 ... ] (usuall day, saturday, sunday)
# days_before = 5 days before this month
# special_cases = {id: array_of_cases_where_he_must_work, ...} or None if its not exist
# ----------------------------------------
class Tester:
    def __init__(self, surface, days_before, days_idx, size, w_d):
        self.surface = np.asarray(surface)
        self.size = size
        self.w_d = w_d
        self.days_before = days_before
        self.days_idx = list(map(int, days_idx))
        #self.special_cases = special_cases
        
    # psurface = piece of days_idx (5 els)
    def previous_day(self, psurface):
        if 1 in psurface and 2 in psurface:
            return 0
        elif 1 in psurface and not 2 in psurface:
            return 0
        elif 2 in psurface and not 1 in psurface:
            return 1
        else:
            return 2
    
    # If can't check line then return False
    # If 'Bad' was returned => bad action
    # If everything is ok => return True
    
    def check_line(self, idx):
        # Catch error
        if idx >= self.size[0]:
            return False
        else:
            
            # CASE 0 (is action was before)
            for i in self.surface.shape[0]:
                if self.surface[idx][i] in self.surface[:,i]:
                    return 'Bad'
            
            # CASE 1 (max days)
            steps = 0
            for el in np.concatenate((self.days_before, self.surface[idx])):
                # Check was holidays in range of 5 days or not
                if el in ('В', 'О'):
                    steps = 0
                else:
                    steps += 1
                    
                if steps > 5:
                    return 'bad'
            
            # CASE 2 (time of the day)
            with open('works.json', 'r') as f:
                workers = json.loads(f.read())
            
            if self.w_d:
                # Night -> not Evening, Morning
                # Night, Evening -> not Morning
                conc = np.concatenate((np.array([  self.days_before[-1]]), self.surface[idx]))
                
                for i in range(1, len(conc)):
                    
                    # Previous day and now
                    el1, el0 = (self.surface[idx][i], self.surface[idx][i-1])
                    
                    if i == 1:
                        left = self.previous_day(self.days_idx[i-1:i+4])
                    else:
                        left = self.days_idx[i-1]
                        
                    right = self.days_idx[i]
                    
                    jobsl = workers['worker_dayt'][str(left)]
                    idx_daytl = workers['worker_dayt'][str(left)+'_idx']
                    
                    jobsr = workers['worker_dayt'][str(right)]
                    idx_daytr = workers['worker_dayt'][str(right)+'_idx']
                    
                    if (not el0 in jobsl or not el1 in jobsr) and (el0 != 0 and el1 != 0):
                        return 'bad'
                    else:
                        if el0 != 0 and el1 != 0:
                            if idx_daytl[jobsl.index(el0)] != idx_daytr[jobsr.index(el1)]:
                                return 'bad'
            else:
                # Night -> not Evening, Morning
                # Night, Evening -> not Morning
                conc = np.concatenate((np.array([ self.days_before[-1]]), self.surface[idx]))
                
                for i in range(1, len(conc)):
                    
                    # Previous day and now
                    el1, el0 = (self.surface[idx][i], self.surface[idx][i-1])
                    
                    if i == 1:
                        left = self.previous_day(self.days_idx[i-1:i+4])
                    else:
                        left = self.days_idx[i-1]
                        
                    right = self.days_idx[i]
                    
                    jobsl = workers['driver_dayt'][str(left)]
                    idx_daytl = workers['driver_dayt'][str(left)+'_idx']
                    
                    jobsr = workers['driver_dayt'][str(right)]
                    idx_daytr = workers['driver_dayt'][str(right)+'_idx']
                    
                    if (not el0 in jobsl or not el1 in jobsr) and (el0 != 0 and el1 != 0):
                        return 'bad'
                    else:
                        if el0 != 0 and el1 != 0:
                            if idx_daytl[jobsl.index(el0)] != idx_daytr[jobsr.index(el1)]:
                                return 'bad'
                            
            # CASE 3 ("3и" paradox)
            conc = np.concatenate((np.array([self.days_before[-1]]), self.surface[idx]))
            flag = False
            if w_d:
                for el in conc:
                    if el == 3:
                        if not flag:
                            flag = True
                        elif el != 3 and not el in ('О', 'В') and flag:
                            return 'bad'
                        elif el in ('О', 'В') and flag:
                            flag = False
            
#             # CASE 4 (special case)
#             if not self.special_cases is None:
#                 for el in self.surface[idx]:
#                     if not el in self.special_cases[idx]:
#                         return 'bad'
            
            return True

# w_d = 1 or 0 (is it worker or not)
# dayt = 0, 1, 2 (usuall day, saturday, sunday)
def all_possible_actions(w_d, dayt):
    
    with open('works.json', 'r') as f:
        workers = json.loads(f.read())
    if w_d:
        worker = workers['worker_dayt'][str(dayt)]
    else:
        worker = workers['driver_dayt'][str(dayt)]
    return worker+['В']
        

# table - pandas.DataFrame without workers + 5 days before this month
# point - (n, c)
def available_actions_in_point(table, point, w_d):
    actions = all_possible_actions(w_d, list(map(int, list(table.columns[5:])))[point[0]])
    for i in actions:
        table.iloc[point[0]].iloc[point[1]] = i
        tester = Tester(table.iloc[:, 5:], table.iloc[:, :5], list(map(int, list(table.columns[5:]))), (table.iloc[:, 5:].shape[1], table.iloc[:, 5:].shape[0]), w_d)
        response = tester.check_line(point[1])
        if response == 'bad':
            actions.remove(i)
    return actions

# ---------------------------------------------------------
# Agent class is a class where bot attract with environment
# w_d = 1 or 0 (1 if it is a worker and 0 if it's not)
# size = (y, x)
# before_days = array of days before this month
# days_idx = array with len of count of days in month with values 0, 1, 2 (usuall day, saturday, sunday)
# holidays = [(id, (start, end))] or None
# ---------------------------------------------------------
class Agent:
    def __init__(self, w_d, size, before_days, days_idx, holidays=None):
        self.w_d = w_d
        self.size = size
        self.before_days = before_days
        self.days_idx = list(map(int, days_idx))
        self.holidays = holidays
        self.env = Environment(size[0], size[1], days_idx, before_days)
            
        self.actions = []
        for day_idx in days_idx:
            self.actions.append(Actions(all_possible_actions(w_d, day_idx)))
    
    def insert_holidays(self):
        if not self.holidays is None:
            for el in self.holidays:
                self.env.add_holiday(el[0], el[1]) 
    
    def count_scores(self):
        
        with open('works.json', 'r') as f:
            workers = json.loads(f.read())
            
        if self.w_d:
            length = self.env.table.shape[1]
            scores = [-self.days_idx.count(0)*8]*length
            worker = workers['worker_hours']
            for en, el in enumerate(self.env.table):
                for i in el:
                    for j in (8, 9, 10):
                        if i in worker[str(j)]:
                            scores[en] += j
                        elif i == 'О':
                            scores[en] += 8
                            
                    
        else:
            length = self.env.table.shape[1]
            scores = [-self.days_idx.count(0)*8]*length
            worker = workers['driver_hours']
            for en, el in enumerate(self.env.table):
                for i in el:
                    for j in (8, 9, 10):
                        if i in worker[str(j)]:
                            scores[en] += j
                        elif i == 'О':
                            scores[en] += 8
        
        return scores
    
    def complete_table(self):
        self.insert_holidays()
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                if j == 0:
                    if not 'В' in before_days[i] or not 'О' in before_days[i]:
                        self.env.add_element('В')
                    elif self.days_before[-1] == 'В' or self.days_before[-1] == 'О':
                        el = random.choice(self.actions.actions())
                        if el != 'В':
                            self.actions.remove_action(el)
                        self.env.add_element(el)
                    else:
                        conc = np.concatenate((self.before_days, self.env.table))
                        actions = available_actions_in_point(conc, (i, j), self.w_d)
                        if len(actions) == 1:
                            self.env.add_element('В')
                        else:
                            el = random.choice(actions)
                            if el != 'В':
                                self.actions.remove_action(el)
                            self.env.add_element(el)
                else:
                    conc = np.concatenate((self.before_days, self.env.table))
                    actions = available_actions_in_point(conc, (i, j), self.w_d)
                    if len(actions) == 1:
                        self.env.add_element('В')
                    else:
                        el = random.choice(actions)
                        if el != 'В':
                            self.actions.remove_action(el)
                        self.env.add_element(el)
        scores = self.count_scores()
        return self.env.table, scores