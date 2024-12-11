from core import Maze

empty_data = [
    ["E","WSE","WE","EW","EW","WE","WE","EW","WE","WE","WE","WE","WSE","WSE","WSE","W"],
    ["S","NE","WE","WS","SE","WS","SE","EW","WS","SE","EW","WS","NS","NS","NE","WS"],
    ["NES","WE","WS","NE","WN","NS","NE","WS","NE","WN","SE","WN","NE","NWE","WE","WNS"],
    ["NES","W","NS","SE","WS","NE","WS","NE","EW","WS","NE","WS","SE","EW","WS","NS"],
    ["NES","W","NE","WN","NE","SW","NSE","WS","SE","WNS","SE","WN","NE","WS","NS","NS"],
    ["NS","SE","WSE","W","SE","WN","N","NE","WN","N","NE","WS","SE","WN","NS","NS"],
    ["NS","NS","NS","E","NSEW","W","SE","EW","EW","WS","E","NWS","NS","SE","WN","NS"],
    ["NS","NS","NE","WS","NE","WS","NS","ES","WSE","WNS","SE","WN","NS","NE","WS","NS"],
    ["NS","NS","SE","WN","SE","WN","NS","NE","WN","NS","NE","WS","NE","WS","NS","NS"],
    ["NS","NS","NS","E","NSEW","W","NSE","W","SE","WN","E","NWS","SE","WN","NS","NS"],
    ["NS","NS","NE","WS","NE","WS","NE","WS","NE","WS","SE","WN","NS","SE","WN","NS"],
    ["NS","NSE","W","NE","EW","NSW","SE","WNS","SE","NW","NE","WS","NS","NE","WS","NS"],
    ["NS","NE","EW","EWS","W","N","NS","NS","NS","S","S","NE","NW","SE","NW","NS"],
    ["NS","E","WS","NS","SE","WS","NS","NSE","NSEW","NSWE","NSW","SE","WS","NS","E","NSW"],
    ["NS","E","NSW","NE","NW","NE","NW","N","N","N","NE","NW","NE","NW","SE","NSW"],
    ["NE","EW","EWN","EW","EW","EW","EW","EW","EW","EW","EW","EW","EW","EW","WN","N"]
]

maze = Maze(16, start=(0,0), end=(8,7), full=True)

for y in range(16):
    for x in range(16):
        cardinals = list(empty_data[y][x])
        for cc in cardinals:
            maze.grid[y][x].walls[cc] = 0

maze.save('resources/japan_2017.pickle')

