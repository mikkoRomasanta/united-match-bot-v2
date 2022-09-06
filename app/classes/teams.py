class TeamInfo(object):
    def __init__(self, position, name, played, gd, points):
        self.position = self.add_spaces(1,str(position).strip())
        self.name = self.add_spaces(2,str(name).strip())
        self.points = self.add_spaces(3,str(points).strip())
        self.gd = self.add_spaces(4,str(gd).strip())
        self.played = self.add_spaces(5,str(played).strip())

    def add_to_table(self):
        return f'{self.position}| {self.name}| {self.played}| {self.gd}| {self.points}'

    def add_spaces(self, num, string): #fix formatting for the table
        space = ' '

        if num == 1:  #1 for position 
            max_len = 3 #max length for string
            add_space = space*(max_len - len(string))
            new_string = f'{string}{add_space}'

        elif num == 2:  #2 for name
            max_len = 25
            add_space = space*(max_len - len(string))
            new_string = f'{string}{add_space}'
        
        elif num == 3:  #3 for points
            max_len = 4 
            add_space = space*(max_len - len(string))
            new_string = f'{string}{add_space}'

        elif num == 5: #4 for played
            max_len = 3
            add_space = space*(max_len - len(string))
            new_string = f'{string}{add_space}'
            
        elif num == 4: #5 for GD
            max_len = 3
            add_space = space*(max_len - len(string))
            new_string = f'{string}{add_space}'
            
        return new_string