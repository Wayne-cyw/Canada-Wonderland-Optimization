import interface 
import json
import search

def load_json(filename: str) -> list:
    """
    Loads the rides from a JSON file and returns them as a list of lists.
    Each inner list represents a group of rides.
    """
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

if __name__ == "__main__":
    #load json file of rides, and their times
    RIDES = load_json("rides.json")
    
    
    #run acis art
    interface.ascii_art()
    
    #run interface for selection rides, input list of rides
    selected_rides = interface.select_rides_2(*RIDES)

    
    #ask budget time   
    start_time, end_time, budget_time = interface.ask_budget()
    
    
    #get optimal path through bitmask dynamic programming
    
    optimal_path = search.find_optimal_path(selected_rides, budget_time)
    
    #print out the best route to take, and the total time taken for the route
    interface.display_optimal_path(optimal_path)
