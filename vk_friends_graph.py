#Для работы скрипта необходимо выполнить в терминале команду ниже
#py -m pip install vk_api
#py -m pip install networkx

import vk_api
import matplotlib.pyplot as plt
import networkx as nx
from random import randint

# Исходные данные
login = input('Введите логин:')
password = input('Введите пароль:')
maxFriends = int(input('Введите максимальное количество друзей:'))

# Попытка подключения к vk api
vkConnection = vk_api.VkApi(login, password)
try:
    vkConnection.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)

# Инициализация доступа к vk api
vk = vk_api.VkTools(vkConnection)
userId = 208131632

# Создание графа друзей
graphFriends = nx.Graph()
c1 = -1

# Добавление друзей и друзей друзей в граф
myFriends = vk.get_all('friends.get', 10, {'user_id': userId, 'count': maxFriends})
for myFriend in myFriends['items']:
  c1 = c1+1
  if c1 < maxFriends:
    graphFriends.add_edge(userId,myFriend)
    try:
      relatedFriends = vk.get_all('friends.get', 10, {'user_id': myFriend, 'count': maxFriends})
    except:
      print(f"У пользователя {myFriend} нет друзей :(")
    else:
      c2 = -1
      for relatedFriend in relatedFriends['items']:
        c2 = c2+1
        if c2 < maxFriends:
          graphFriends.add_edge(myFriend,relatedFriend)

close_centrality = nx.closeness_centrality(graphFriends)
close_centrality_id = max(close_centrality.items(), key = lambda k : k[1])

bet_centrality = nx.betweenness_centrality(graphFriends, normalized = True, endpoints = False)
bet_centrality_id = max(bet_centrality.items(), key = lambda k : k[1])

eig_centrality = nx.eigenvector_centrality(graphFriends)
eig_centrality_id = max(eig_centrality.items(), key = lambda k : k[1])

print(f"Близостная центральность: {close_centrality_id}\n")
print(f"Центральность по посредничеству: {bet_centrality_id}\n")
print(f"Центральность по собственному значению: {eig_centrality_id}\n")

plt.figure(figsize =(30, 15))
nx.draw_networkx(graphFriends, with_labels = True)
