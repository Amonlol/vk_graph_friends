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
vk_session = vk_api.VkApi(login, password)
try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)

# Инициализация доступа к vk api
tools = vk_api.VkTools(vk_session)
my_id = 208131632
friends = tools.get_all('friends.get', 10, {'user_id': my_id, 'count': maxFriends})

# Создание графа друзей
friends_graph = nx.Graph()
c1 = -1

# Добавление друзей и друзей друзей в граф
for friend_1 in friends['items']:
  c1 = c1+1
  if c1 < maxFriends:
    friends_graph.add_edge(my_id,friend_1)
    try:
      friends2 = tools.get_all('friends.get', 10, {'user_id': friend_1, 'count': maxFriends})
    except:
      print(f"user {friend_1} has no friends")
    else:
      c2 = -1
      for friend_2 in friends2['items']:
        c2 = c2+1
        if c2 < maxFriends:
          friends_graph.add_edge(friend_1,friend_2)

# Близостная центральность
close_centrality = nx.closeness_centrality(friends_graph)
close_centrality_id = max(close_centrality.items(), key = lambda k : k[1])
print("Близостная центральность:")
print(close_centrality_id)

# Центральность по посредничеству
bet_centrality = nx.betweenness_centrality(friends_graph, normalized = True, endpoints = False)
bet_centrality_id = max(bet_centrality.items(), key = lambda k : k[1])
print("Центральность по посредничеству:")
print(bet_centrality_id)

# Центральность по собственному значению
eig_centrality = nx.eigenvector_centrality(friends_graph)
eig_centrality_id = max(eig_centrality.items(), key = lambda k : k[1])
print("Центральность по собственному значению:")
print(eig_centrality_id)

plt.figure(figsize =(30, 15))
nx.draw_networkx(friends_graph, with_labels = True)
