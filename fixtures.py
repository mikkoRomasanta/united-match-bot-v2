from datetime import datetime


class Fixture(object):
    def __init__(self, time, weekday, day, month, year, competition, home, away):
        self.time = time
        self.weekday = weekday
        self.day = day
        self.month = month
        self.year = year
        self.competition = competition
        self.home = home
        self.away = away
        self.converted_matchday = self.format_datetime()

    def convert_datetime(self):
        date = f'{self.day}/{self.month}/{self.year} {self.time} {self.weekday} +0100' #UTC+1
        matchday = datetime.strptime(date, '%d/%B/%Y %H:%M %A %z')
        matchday = matchday.astimezone() #convert to localtime
        
        return matchday
    
    def format_datetime(self):
        md = self.convert_datetime()
        readable_date = (
            f'{self.home} [ VS ] {self.away}  [ {self.competition} ]\n'
            f'\t{md.strftime("%d")} {md.strftime("%b")} '
            f'{md.strftime("%Y")} [ {md.strftime("%H:%M")} ], '
            f'{md.strftime("%A")}'
        )
        
        return readable_date