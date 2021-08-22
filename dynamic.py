from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import pandas as pd
from geopy.distance import great_circle



"""Read from csv file"""
def read_csv(csv_file):
    try:
        return pd.read_csv(csv_file)
    except Exception as e:
        print("An exception occurred: ", e)

"""Calculate distance between 2 cities"""
def calculate_distance(set1, set2):
    return great_circle(set1, set2).km


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



def create_data_model(dist_matrix):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = dist_matrix  # yapf: disable
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

cities =read_csv('cities_all.csv')
dist_matrix = build_dist_matrix(cities)
data = create_data_model(dist_matrix)
manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                       data['num_vehicles'], data['depot'])
routing = pywrapcp.RoutingModel(manager)


def distance_callback(from_index, to_index):
    """Returns the distance between the two nodes."""
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data['distance_matrix'][from_node][to_node]


transit_callback_index = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print('Objective: {} km'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}km\n'.format(route_distance)

solution = routing.SolveWithParameters(search_parameters)
if solution:
    print_solution(manager, routing, solution)

