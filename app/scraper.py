import requests
from bs4 import BeautifulSoup
import sqlalchemy
import classes.teams as t
import classes.fixtures as f
import db
from datetime import datetime
    
def set_table():
    """ Set up beautiful soup for reading the league table.
    """
    #which url to scrape for the table
    url = 'https://www.skysports.com/premier-league-table'

    r = requests.get(url)
    # print(r.status_code)

    bs = BeautifulSoup(r.text, 'html.parser')
    # print(bs).encode("utf-8") # use for printing bs

    league_table = bs.find('table', class_ = 'standing-table__table callfn')
    # print(league_table)
    
    return league_table

def set_fixtures():
    """ Same as setTable, but reads the 3 month fixture list instead.
    """
    #which url to scrape for the table
    url = 'https://www.skysports.com/manchester-united-fixtures'

    r = requests.get(url)
    # print(r.status_code)

    bs = BeautifulSoup(r.text, 'html.parser')
    # print(bs).encode("utf-8") # use for printing bs

    fixtures = bs.find('div', class_ = 'fixres__body callfn')
    # print(league_table)
    return fixtures

#find all teams and stats needed
def get_table():
    """ Scrapes site for table and team info. Create an object for each team then append into a table.
    """
    league_table = set_table()
    for team in league_table.find_all('tbody'):
        table = []
        #setup header
        header = t.TeamInfo('#','Teams','GP','Pts')
        header = header.add_to_table()
        table.append(header)

        #find teams & stats in tr
        rows = team.find_all('tr')
        for row in rows:
            team = row.find('td', class_ = 'standing-table__cell standing-table__cell--name').text.strip()
            position = row.find_all('td', class_ = 'standing-table__cell')[0].text
            played = row.find_all('td', class_ = 'standing-table__cell')[2].text
            points = row.find_all('td', class_ = 'standing-table__cell')[9].text
            
            if team == 'Manchester United':
                position = f'-{position}'

            team_info = t.TeamInfo(position, team, played, points)
            new_team = team_info.add_to_table()
            table.append(new_team)

    return table

def get_fixtures(arg=''):
    """ Scrapes site for fixture list and info. Create object for each fixture then append into table.
    """
    fixtures = set_fixtures()
    fixture_list = []
    #get year
    year = fixtures.find('h3').text.split(' ')
    year = year[1]

    #set limit. 1 = used to notify next match date
    if arg != '-notify': 
        limit = 5 
    else: 
        limit = 1 
    
    for index, fixture in enumerate(fixtures.find_all('h4',limit=limit)):
        date = fixture.get_text()
        date = date.split(' ')
        date[1] = date[1][:len(date[1])-2] #ex. 27th
        competition = fixture.find_next_sibling('h5').text
        matchdiv = fixture.find_next_sibling('div')
        time = matchdiv.find('span',{'class':'matches__date'}).text.strip()
        home = matchdiv.find('span',{'class':'matches__participant--side1'}).text.strip()
        away = matchdiv.find('span',{'class':'matches__participant--side2'}).text.strip()
        matchinfo = f.Fixture(
            time,
            date[0],
            date[1],
            date[2],
            year,
            competition,
            home,
            away,
            )
        
        if limit == 1:
            match_datetime = matchinfo.convert_datetime()
            match_info = matchinfo.format_datetime()
            data = {
                "match_datetime" : match_datetime,
                "match_info" : match_info
            }
                        
            return data
        
        match = matchinfo.format_datetime()
        fixture_list.append(match)
        
    return fixture_list     
    

def send_table(arg):
    """ Get league table, and format it to be readable in discord.
    """  
    session = db.load_session()
    today = datetime.now().date()
    
    if arg != '-force':
        #if data for today is stored then skip scraping and send saved data
        for s in session.query(db.Application).filter(
            db.Application.type=='table',
            db.Application.date==today
            ).order_by(
                sqlalchemy.desc(db.Application.id)
            ):

            text = s.data
            session.close()
            
            #send to discord
            return text

        #run if no data for today is stored
        table = get_table()
        text = '```diff\n'
        
        for x in table:
            text += x + '\n'
            
        text += '```'

        #add to db
        text_to_db = db.Application(data=text,type='table')
        session = db.load_session()
        session.add(text_to_db)
        session.commit()
        session.close()
        
        #send to discord
        return text
    else:
        table = get_table()
        
        text = '```diff\n'
        
        for x in table:
            text += x + '\n'
            
        text += '```'
        
        for s in session.query(db.Application).filter(
            db.Application.type=='table',
            db.Application.date==today
            ).order_by(
                sqlalchemy.desc(db.Application.id)
            ):
                #update data
                s.data = text
                session.commit()
                session.close()
                
                #send to discord
                return text
                

def send_fixtures():
    """ Get fixture list, and format it to be readable in discord.
    """ 
    session = db.load_session()
    today = datetime.now().date()

    #if data for today is stored then skip scraping and send saved data
    for s in session.query(db.Application).filter(
        db.Application.type=='sched',
        db.Application.date==today
        ).order_by(
            sqlalchemy.desc(db.Application.id)
        ):

        text = s.data
        session.close()
        
        #send to discord
        return text
    
    #run if no data for today is stored
    fixtures = get_fixtures()
    text = ''
    
    for x in fixtures:
        row = '```css\n'
        row += x + '\n'
        row += '```'
        text += row
        
    #add to db
    text_to_db = db.Application(data=text,type='sched')
    session = db.load_session()
    session.add(text_to_db)
    session.commit()
    session.close()

    #send to discord
    return text

if __name__=="__main__":
    print(send_fixtures())