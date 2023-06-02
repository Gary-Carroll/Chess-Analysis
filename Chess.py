#!/usr/bin/env python
# coding: utf-8

# In[140]:


import lichess.api
from lichess.format import PYCHESS
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import pandas as pd
from collections import Counter


# In[2]:


user = lichess.api.user('GarethC13')
print(user['perfs']['bullet']['rating'])


# In[3]:


games = lichess.api.user_games('GarethC13', max=3000, perfType='bullet')
gameslist = list(games)


# In[4]:


whitegames = []
blackgames = []
for game in gameslist:
    players = game['players']
    colour = players.get('white')
    user = colour.get('user')
    i_d = user.get('id')
    if i_d == 'garethc13':
        whitegames.append(game)
    else:
        blackgames.append(game)
print(len(gameslist),'total bullet games.')
print(len(whitegames),'as white.')
print(len(blackgames),'as black.')


# # Opponents' opening moves

# In[5]:


move = ['a3','a4','b3','b4','c3','c4','d3','d4','e3','e4','f3','f4','g3','g4','h3','h4','Nf3','Nb3','Na3','Nh3']
values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
squares = [[2,7],[3,7],[2,6],[3,6],[2,5],[3,5],[2,4],[3,4],[2,3],[3,3],[2,2],[3,2],[2,1],[3,1],[2,0],[3,0],
           [2,2],[2,6],[2,7],[2,0]]

uniform_data = np.zeros([8,8])
for i in blackgames:
    j = i['moves'].split()
    for m,v,s in zip(move,range(20),squares):
        if j[0] == m:
            values[v] += 1
            
print(values)

for v,s in zip(values,squares):
    s0 = s[0]
    s1 = s[1]
    uniform_data[s0,s1] = v

cmap = sns.cm.rocket_r
for v,s in zip(values,squares):
    s0 = s[0]
    s1 = s[1]
    uniform_data[s0,s1] = v

data_avg = uniform_data/sum(values)    

x_axis_labels = ['h','g','f','e','d','c','b','a']
y_axis_labels = [1,2,3,4,5,6,7,8]

ax = sns.heatmap(data_avg,square=True,xticklabels=x_axis_labels, yticklabels=y_axis_labels,
                 cmap=cmap,linewidth=0.5)
plt.title('Opening Moves of my Opponents as White')
plt.savefig('openings.png')
plt.show()
sum(values)


# # My opening moves

# In[6]:


move = ['a3','a4','b3','b4','c3','c4','d3','d4','e3','e4','f3','f4','g3','g4','h3','h4','Nf3','Nb3','Na3','Nh3']
values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
squares = [[2,7],[3,7],[2,6],[3,6],[2,5],[3,5],[2,4],[3,4],[2,3],[3,3],[2,2],[3,2],[2,1],[3,1],[2,0],[3,0],
           [2,2],[2,6],[2,7],[2,0]]

uniform_data = np.zeros([8,8])
for i in whitegames:
    j = i['moves'].split()
    for m,v,s in zip(move,range(20),squares):
        if j[0] == m:
            values[v] += 1
for v,s in zip(values,squares):
    s0 = s[0]
    s1 = s[1]
    uniform_data[s0,s1] = v
cmap = sns.cm.rocket_r

data_avg = uniform_data/sum(values)    
    
x_axis_labels = ['h','g','f','e','d','c','b','a']
y_axis_labels = [1,2,3,4,5,6,7,8]

ax = sns.heatmap(data_avg,square=True,xticklabels=x_axis_labels, yticklabels=y_axis_labels,
                 cmap=cmap,linewidth=0.5)
plt.title('Opening Moves by Me as White')
ax.invert_xaxis()
ax.invert_yaxis()
plt.show()
print(values)


# # Square of black king at checkmate

# In[7]:


letters = ['a','b','c','d','e','f','g','h']
move = []
values = [0]*64
squares = []
v = 0
for i in letters:
    for j in range(1,9,1):
        k = i+str(j)
        move.append(k)

x = 7
while x >= 0:
    for f in range(0,8):
        for i in range(0,8):
            j = [i,x]
            squares.append(j)
        x-=1

        
for x in blackgames:
    if x['status'] == 'mate' and x['winner'] == 'white':
        y = x['moves']
        y = list(y.split(' '))
        y = y[1::2]
        king = 0
        for i in y:
            if i[0] == 'K':
                king = i[-2:]
            elif i == 'O-O':
                king = 'g8'
            elif i == 'O-O-O':
                king = 'c8'
        for m,v in zip(move,range(64)):
            if m == king:
                values[v] += 1
        if king == 0:
            values[39] += 1
            
data = np.zeros([8,8])
for v,s in zip(values,squares):
    s0 = s[0]
    s1 = s[1]
    data[s0,s1] = v


# In[8]:


x_axis_labels = ['h','g','f','e','d','c','b','a']
y_axis_labels = [1,2,3,4,5,6,7,8]
data = data/(sum(sum(data)))
ax = sns.heatmap(data,square=True,xticklabels=x_axis_labels, yticklabels=y_axis_labels,
                 cmap=cmap,linewidth=0.5)
plt.title('Square of king at checkmate, black pieces.')
plt.savefig('blackmate.png')
plt.show()


# # Square of white king at checkmate

# In[9]:


letters = ['a','b','c','d','e','f','g','h']
move = []
values = [0]*64
squares = []
v = 0
for i in letters:
    for j in range(1,9,1):
        k = i+str(j)
        move.append(k)

x = 7
while x >= 0:
    for f in range(0,8):
        for i in range(0,8):
            j = [i,x]
            squares.append(j)
        x-=1

        
for x in whitegames:
    if x['status'] == 'mate' and x['winner'] == 'black':
        y = x['moves']
        y = list(y.split(' '))
        y = y[0::2]
        king = 0
        for i in y:
            if i[0] == 'K':
                king = i[-2:]
            elif i == 'O-O':
                king = 'g1'
            elif i == 'O-O-O':
                king = 'c1'
        for m,v in zip(move,range(64)):
            if m == king:
                values[v] += 1
        if king == 0:
            values[32] += 1
            
data = np.zeros([8,8])
for v,s in zip(values,squares):
    s0 = s[0]
    s1 = s[1]
    data[s0,s1] = v


# In[10]:


x_axis_labels = ['h','g','f','e','d','c','b','a']
y_axis_labels = [1,2,3,4,5,6,7,8]
data = data/(sum(sum(data)))
ax = sns.heatmap(data,square=True,xticklabels=x_axis_labels, yticklabels=y_axis_labels,
                 cmap=cmap,linewidth=0.5)
plt.title('Square of king at checkmate, white pieces.')
ax.invert_xaxis()
ax.invert_yaxis()
plt.savefig('whitemate.png')
plt.show()


# # Performance by hour and day

# In[20]:


hour_dictionary = {key: {'win' : 0, 'draw' : 0, 'loss' : 0} for key in range(24)}
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_dictionary = {key: {'win' : 0, 'draw' : 0, 'loss' : 0} for key in days}

for game in whitegames:
    time = datetime.fromtimestamp(game['createdAt']/1000)
    hour = int(time.strftime("%H"))
    day = time.strftime("%A")
    
    winner = game.get('winner')
    if winner == 'white':
        hour_dictionary[hour]['win'] += 1
        day_dictionary[day]['win'] += 1
    elif winner == 'black':
        hour_dictionary[hour]['loss'] += 1
        day_dictionary[day]['loss'] += 1
    else:
        hour_dictionary[hour]['draw'] += 1
        day_dictionary[day]['draw'] += 1
        
for game in blackgames:
    time = datetime.fromtimestamp(game['createdAt']/1000)
    hour = int(time.strftime("%H"))
    
    winner = game.get('winner')
    if winner == 'white':
        hour_dictionary[hour]['loss'] += 1
        day_dictionary[day]['loss'] += 1
    elif winner == 'black':
        hour_dictionary[hour]['win'] += 1
        day_dictionary[day]['win'] += 1
    else:
        hour_dictionary[hour]['draw'] += 1
        day_dictionary[day]['draw'] += 1


# In[21]:


hour_dictionary


# In[28]:


hour_data = pd.DataFrame(hour_dictionary)
hour_data=hour_data.T
hour_data.head()


# In[29]:


normalised_hour_data = hour_data.div(hour_data.sum(axis=1), axis=0)
normalised_hour_data.plot(kind='bar', stacked=True, title = 'Performance by hour', colormap = 'viridis',figsize=(14,6))
plt.xlabel('Hour')
plt.ylabel('Result')
plt.legend(prop={'size': 18}, loc='upper right')


# In[67]:


hour_data.plot(kind='bar', title = 'Performance by hour', colormap = 'viridis',figsize=(14,6));
plt.legend(prop={'size': 18}, loc='upper left')


# In[25]:


day_dictionary


# In[33]:


day_data = pd.DataFrame(day_dictionary)
day_data=day_data.T
day_data.head()


# In[68]:


day_data.plot(kind='bar', title = 'Performance by day', colormap = 'viridis',figsize=(14,6));
plt.legend(prop={'size': 18}, loc='upper left')


# # Rating progression and average of me and my opponents

# In[102]:


my_rating = []
opponent_rating = []
time = []
limit = 0

while limit < 3000:
    game = gameslist[limit]
    players = game['players']
    white = players.get('white')
    white_user = white.get('user')
    white_id = white_user.get('id')
    white_rating = white.get('rating')
    
    black = players.get('black')
    black_user = black.get('user')
    black_id = black_user.get('id')
    black_rating = black.get('rating')
    
    if white_id == 'garethc13':
        my_rating.append(white_rating)
        opponent_rating.append(black_rating)
    else:
        my_rating.append(black_rating)
        opponent_rating.append(white_rating)
        
    time.append(game['createdAt'])
    limit += 1


# In[117]:


plt.figure(figsize=(15,6))
plt.plot(time, my_rating, label = 'My rating',linestyle='-')
plt.plot(time, [np.mean(my_rating)] * len(time), label='Average')

plt.title('My rating progression')
plt.ylabel('Rating')
plt.xlabel('Time')
plt.legend()
plt.legend(prop={'size': 15}, loc='lower left')
plt.grid()
print('My average rating: '+str(round(np.mean(my_rating),2)))


# In[116]:


plt.figure(figsize=(15,6))
plt.plot(time, opponent_rating, label = 'Opponent rating')
plt.plot(time, [np.mean(opponent_rating)] * len(time), label='Average')

plt.title('Opponent rating progression')
plt.ylabel('Rating')
plt.xlabel('Time')
plt.legend()
plt.legend(prop={'size': 15}, loc='lower left')
plt.grid()
print('Average opponent rating: '+str(round(np.mean(opponent_rating),2)))


# # Outcome of games

# In[176]:


win_status = []
lose_status = []
for game in whitegames:
    winner = game.get('winner')
    if winner == 'white':
        win_status.append(game['status'])
    elif winner == 'black':
        lose_status.append(game['status'])

for game in blackgames:
    winner = game.get('winner')
    if winner == 'black':
        win_status.append(game['status'])
    elif winner == 'white':
        lose_status.append(game['status'])

win_counter = Counter(win_status)
win_elements = list(win_counter.keys())
win_counts = list(win_counter.values())

lose_counter = Counter(lose_status)
lose_elements = list(lose_counter.keys())
lose_counts = list(lose_counter.values())

plt.figure()
plt.bar(win_elements,win_counts)
plt.title('Result of games I win')

plt.figure()
plt.bar(lose_elements,lose_counts)
plt.title('Result of games I lose')
plt.show()
print('Note: \'timeout\' means that the loser left the game before it was over.')

