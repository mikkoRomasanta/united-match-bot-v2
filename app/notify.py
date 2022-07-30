import datetime as dt
import scraper


def send_notification(data):
    """"""
    #convert seconds to hours and minutes
    time = data["time"]
    if time >= 3600:
        hours = round(time / 3600,2)
        time_remaining = f'{hours} hours'
    else:
        minutes = round(time / 60,2)
        time_remaining = f'{minutes} minutes'
    
    #format discord message
    text = f'<@&{data["role"]}> Match will start in **{time_remaining}**.'
    text += '```css\n'
    text += f'{data["info"]}\n'
    text += '```'
    
    return text
    
def check_date_difference():
    """"""
    #get next match's datetime info
    sched = scraper.get_fixtures('-notify')
    match_datetime = sched["match_datetime"]
    match_info = sched["match_info"]
    now = dt.datetime.now()
    now = now.astimezone()
    diff = match_datetime - now
    #set time for notification
    notify1 = 36000 #20 hours
    notify2 = 7200 #2 hours
    
    #send match data and delay the next task.loop if sending notification. 
    #notify if less than 1 day
    if diff.days < 1 and diff.days >= 0 and diff.seconds > notify1:
        #send discord notification
        data = {
            'notify': True,
            'time': diff.seconds,
            'info': match_info,
            'diff': diff
        }
    #notify if less than 2 hours
    elif diff.days < 1 and diff.days >= 0 and diff.seconds < notify2:
        #send discord notification
        data = {
            'notify': True,
            'time': diff.seconds,
            'info': match_info,
            'diff': diff
        }        
    else:
        data = {
            'notify': False,
            'diff':diff
        }
        
    return data