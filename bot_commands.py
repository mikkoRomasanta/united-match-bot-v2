commands = [
    {'command': 'gg', 'desc': 'returns MU!'},
    {'command': 'sched', 'desc': 'returns the next 5 matches'},
    {'command': 'table', 'desc': 'returns the current Premiere League Table'}
]

def send_commands():
    text = '```css\n'
    
    for x in commands:
        text += f'{x["command"]} : {x["desc"]} \n'
        
    text += '```'
    
    return text

if __name__ == "__main__":
    print(send_commands())