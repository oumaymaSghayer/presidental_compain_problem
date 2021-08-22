import pandas as pd
from geopy.distance import great_circle
from sys import maxsize

"""Read from csv file"""
def read_csv(csv_file):
    try:
        return pd.read_csv(csv_file)
    except Exception as e:
        print("An exception occurred: ", e)

"""Calculate distance between 2 cities"""
def calculate_distance(set1, set2):
    return round(great_circle(set1, set2).km,3)

"""Build the distance matrix"""
def build_dist_matrix(cities):
    print('Calculating distances matrix...')
    cities_distances = []
    for i, row1 in cities.iterrows():
        int_array = []
        for j, row2 in cities.iterrows():
            int_array.append(
                calculate_distance((row1['Latitude'], row1['Longitude']), (row2['Latitude'], row2['Longitude'])))
        cities_distances.append(int_array)
    return cities_distances

"""Logic"""
def logic(dist_matrix , starting_city_index):
    n=len(dist_matrix)

    memo =setup(dist_matrix,starting_city_index)
    solve(dist_matrix, memo, starting_city_index)

    shortest_path=find_shortest_path(dist_matrix, memo, starting_city_index, n)

    return shortest_path

"""Solve shortest path between 2 nodes and store visitied nodes"""
def setup(dist_matrix,starting_city):
    print('setting up memo table ...')
    memo=[]
    for i in range(len(dist_matrix)):
        if i!= starting_city:
            memo.append([dist_matrix[starting_city][i],[starting_city,i]])
    return memo

"""Solve shortest path between n nodes and store visitied nodes"""
def solve(dist_matrix,memo,starting_city):
    print('solving...')
    n=len(dist_matrix)
    for i in range(3,n+1):
        for k in range(len(memo)):
            dist = memo[k][0]
            visited_nodes= memo[k][1]
            """Find optimal path with i nodes"""
            min_path = maxsize
            next_node=0
            for j in range(n):
                if j not in visited_nodes:
                    distance=dist_matrix[visited_nodes[len(visited_nodes)-1]][j]
                    if distance < min_path:
                        min_path = distance
                        next_node=j
            visited_nodes.append(next_node)
            dist+=min_path
            memo[k]=[dist,visited_nodes]


def find_shortest_path(dist_matrix,memo,starting_city,n):
    print('finding shortest path...')
    for i in range(len(memo)):
        ending_city=memo[i][1][len(dist_matrix)-1]
        dist = dist_matrix[starting_city][ending_city]
        memo[i][1].append(starting_city)
        memo[i][0]+=dist
    print(memo)
    min_path=maxsize
    path=[]
    for dist,visited_cities in memo:
        if(dist<min_path):
            min_path=dist
            path=visited_cities
    return (min_path,path)


"""Display list of cities"""
def find_cities_list(cities,shortest_path):
    print('finding cities list...')
    print("Here it goes !")
    print("---------------------------")
    i=1
    for city_index in shortest_path[1]:
        print(i , cities.iloc[city_index]['City'])
        i+=1
    print("Total distance is " , round(shortest_path[0],3), 'km')



cities =read_csv('cities_all.csv')
dist_matrix = build_dist_matrix(cities)
shortest_path = logic(dist_matrix,0)
find_cities_list(cities,shortest_path)

