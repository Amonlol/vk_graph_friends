!pip install vk_api
import vk_api
import matplotlib.pyplot as plt
import networkx as nx
from random import randint

# Логин, пароль для авторизации
login = 'mail@email.com'
password = 'password'

# Ограничение на максимальное количество друзей
MAX_FRIENDS = 5

# Создание подключения к API
vk_session = vk_api.VkApi(login, password)

try:
    # Получение токена
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)

# Создание объекта с методами доступа к API
tools = vk_api.VkTools(vk_session)

# id первоначального юзера
my_id = 208131632

# Список друзей юзера
friends = tools.get_all('friends.get', 10, {'user_id': my_id, 'count': MAX_FRIENDS})

# Граф с друзьями и друзьями друзей
friends_graph = nx.Graph()

c1 = -1

# Добавление друзей и друзей друзей в граф
for friend_1 in friends['items']:
  c1 = c1+1
  # Добавить в граф связь: юзер-друг
  if c1 < MAX_FRIENDS:
    friends_graph.add_edge(my_id,friend_1)
    try:
      # Получить список друзей друга
      friends2 = tools.get_all('friends.get', 10, {'user_id': friend_1, 'count': MAX_FRIENDS})
    except:
      # Если страница удалена - вывести ошибку
      print(f"user {friend_1} has no friends")
    else:
      # Если список получен, добавить в граф связи: друг - друзья друга
      c2 = -1
      for friend_2 in friends2['items']:
        c2 = c2+1
        if c2 < MAX_FRIENDS:
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

#print(friends_graph.edges)

plt.figure(figsize =(30, 15))
nx.draw_networkx(friends_graph, with_labels = True)
