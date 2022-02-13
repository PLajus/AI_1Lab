"""
2022-02-13
Povilas Lajus
Ernest Petrovic
Mindaugas Gaidys
"""

from copy import deepcopy
from tkinter import *
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from search import *
from utils import PriorityQueue

root = None
city_coord = {}
romania_problem = None
algo = None
start = None
goal = None
counter = -1
city_map = None
frontier = None
front = None
node = None
next_button = None
explored = None

vilnius_map = UndirectedGraph(
    dict(
        Senamiestis=dict(
            Naujamiestis=2,
            Snipiskes=3,
            Zirmunai=5,
            Rasos=7,
            Antakalnis=15,
            Naujininkai=10,
        ),
        Vilkpede=dict(
            Naujamiestis=10, Lazdynai=5, Karoliniskes=7, Zverynas=12, Naujininkai=4
        ),
        Seskine=dict(
            Zverynas=6,
            Snipiskes=6,
            Verkiai=15,
            Fabijoniskes=3,
            Pasilaiciai=3,
            Justiniskes=5,
            Virsuliskes=8,
            Karoliniskes=12,
        ),
        Paneriai=dict(Grigiskes=12, Lazdynai=15, Vilkpede=22, Naujininkai=18),
        Pilaite=dict(Justiniskes=4, Virsuliskes=9, Karoliniskes=2),
        Naujoji_vilnia=dict(Antakalnis=16, Rasos=50),
        Antakalnis=dict(Verkiai=25, Zirmunai=11, Rasos=20),
        Naujininkai=dict(Rasos=8, Naujamiestis=25),
        Naujamiestis=dict(Zverynas=5, Snipiskes=11),
        Zirmunai=dict(Snipiskes=7, Verkiai=6),
        Pasilaiciai=dict(Fabijoniskes=13, Justiniskes=9),
        Verkiai=dict(Fabijoniskes=10, Zirmunai=13),
    )
)

vilnius_map.locations = dict(
    Senamiestis=(400, 350),
    Naujamiestis=(320, 340),
    Zverynas=(300, 390),
    Snipiskes=(360, 401),
    Zirmunai=(390, 450),
    Seskine=(300, 450),
    Virsuliskes=(250, 430),
    Karoliniskes=(230, 390),
    Lazdynai=(200, 310),
    Vilkpede=(240, 245),
    Naujininkai=(350, 150),
    Paneriai=(110, 50),
    Rasos=(430, 195),
    Grigiskes=(55, 150),
    Pilaite=(99, 425),
    Justiniskes=(221, 470),
    Pasilaiciai=(210, 526),
    Fabijoniskes=(302, 500),
    Verkiai=(360, 600),
    Antakalnis=(693, 523),
    Naujoji_vilnia=(680, 309),
)


def create_map(root):
    """Nupiesia zemelapi."""

    global city_map, start, goal
    vilnius_locations = vilnius_map.locations

    WIDTH = 750
    HEIGHT = 670
    MARGIN = 5
    city_map = Canvas(root, width=WIDTH, height=HEIGHT)
    city_map.pack()

    for start_node in vilnius_map.graph_dict:
        for end_node, dist in vilnius_map.graph_dict[start_node].items():
            make_line(
                city_map,
                vilnius_locations[start_node][0],
                HEIGHT - vilnius_locations[start_node][1],
                vilnius_locations[end_node][0],
                HEIGHT - vilnius_locations[end_node][1],
                vilnius_map.get(start_node, end_node),
            )

    for key, value in vilnius_locations.items():
        make_rectangle(
            city_map,
            vilnius_locations[key][0],
            HEIGHT - vilnius_locations[key][1],
            MARGIN,
            key,
        )

    make_legend(city_map)


def make_line(map, x0, y0, x1, y1, distance):
    """Nupiesia linijas zemelapyje tarp rajonu."""
    map.create_line(x0, y0, x1, y1)
    map.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=distance)


def make_rectangle(map, x0, y0, MARGIN, city_name):
    """Nupiesia kvadratus, kurie zymi rajonus"""
    global city_coord
    rect = map.create_rectangle(
        x0 - MARGIN, y0 - MARGIN, x0 + MARGIN, y0 + MARGIN, fill="white"
    )

    map.create_text(x0 - 2 * MARGIN, y0 - 2 * MARGIN, text=city_name, anchor=S)
    city_coord.update({city_name: rect})


def make_legend(map):
    """Nupiesia legenda"""
    map.create_rectangle(600, 10, 610, 20, fill="white")
    map.create_text(615, 15, anchor=W, text="Un-explored")

    map.create_rectangle(600, 25, 610, 35, fill="orange")
    map.create_text(615, 30, anchor=W, text="Frontier")

    map.create_rectangle(600, 40, 610, 50, fill="red")
    map.create_text(615, 45, anchor=W, text="Currently Exploring")

    map.create_rectangle(600, 55, 610, 65, fill="grey")
    map.create_text(615, 60, anchor=W, text="Explored")

    map.create_rectangle(600, 70, 610, 80, fill="dark green")
    map.create_text(615, 75, anchor=W, text="Final Solution")


def display_frontier(queue):
    """Nuspalvina rajonus i kuriuos galima eiti oranzinia"""
    global city_map, city_coord

    queue_temp = deepcopy(queue)
    while queue_temp:
        node = queue_temp.pop()
        for city, value in city_coord.items():
            if node.state == city:
                city_map.itemconfig(city_coord[city], fill="orange")


def display_current(node):
    """Nuspalvina rajono langeli, kuriame esama siuo metu raudonai"""
    global city_map, city_coord

    city = node.state
    city_map.itemconfig(city_coord[city], fill="red")


def display_explored(node):
    """Nuspalvina aplankytus rajonus pilkai"""
    global city_map, city_coord

    city = node.state
    city_map.itemconfig(city_coord[city], fill="gray")


def display_final(cities):
    """Nuspalvina sprendimo kelia zaliai"""
    global city_map, city_coord

    for city in cities:
        city_map.itemconfig(city_coord[city], fill="green")


def breadth_first_tree_search(problem):
    """BFS implementacija"""
    global frontier, counter, node
    if counter == -1:
        frontier = deque()

    if counter == -1:
        frontier.append(Node(problem.initial))

        display_frontier(frontier)
    if counter % 3 == 0 and counter >= 0:
        node = frontier.popleft()

        display_current(node)
    if counter % 3 == 1 and counter >= 0:
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))

        display_frontier(frontier)
    if counter % 3 == 2 and counter >= 0:
        display_explored(node)
    return None


def depth_first_tree_search(problem):
    """DFS implementacija"""
    # This search algorithm might not work in case of repeated paths.
    global frontier, counter, node
    if counter == -1:
        frontier = []  # stack

    if counter == -1:
        frontier.append(Node(problem.initial))

        display_frontier(frontier)
    if counter % 3 == 0 and counter >= 0:
        node = frontier.pop()

        display_current(node)
    if counter % 3 == 1 and counter >= 0:
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))

        display_frontier(frontier)
    if counter % 3 == 2 and counter >= 0:
        display_explored(node)
    return None


def on_click():
    """
    Funkcija kvieciama paspaudus mygtuka "Next", vykdomas pasirinktas paieskos algoritmas
    """
    global algo, counter, next_button, vilnius_problem, start, goal

    vilnius_problem = GraphProblem(start.get(), goal.get(), vilnius_map)

    if "Breadth-First Tree Search" == algo.get():
        node = breadth_first_tree_search(vilnius_problem)
        if node is not None:
            final_path = breadth_first_tree_search(vilnius_problem).solution()
            final_path.append(start.get())
            display_final(final_path)
            next_button.config(state="disabled")
        counter += 1

    elif "Depth-First Tree Search" == algo.get():
        node = depth_first_tree_search(vilnius_problem)
        if node is not None:
            final_path = depth_first_tree_search(vilnius_problem).solution()
            final_path.append(start.get())
            display_final(final_path)
            next_button.config(state="disabled")
        counter += 1


def reset_map():
    """Isvalo zemelapi"""
    global counter, city_coord, city_map, next_button
    counter = -1

    for key, value in city_coord.items():
        city_map.itemconfig(city_coord[key], fill="white")
    next_button.config(state="normal")


if __name__ == "__main__":
    root = Tk()

    root.title("Vilniaus rajonu zemelapis")

    root.geometry("950x1150")

    algo = StringVar(root)
    start = StringVar(root)

    goal = StringVar(root)

    algo.set("Breadth-First Tree Search")
    start.set("Senamiestis")
    goal.set("Naujoji_vilnia")

    cities = sorted(vilnius_map.locations.keys())
    algorithm_menu = OptionMenu(
        root, algo, "Breadth-First Tree Search", "Depth-First Tree Search"
    )

    Label(root, text="\n Search Algorithm").pack()
    algorithm_menu.pack()
    Label(root, text="\n Start Rajonas").pack()

    start_menu = OptionMenu(root, start, *cities)
    start_menu.pack()

    Label(root, text="\n Goal Rajonas").pack()

    goal_menu = OptionMenu(root, goal, *cities)
    goal_menu.pack()

    frame1 = Frame(root)

    next_button = Button(
        frame1,
        width=6,
        height=2,
        text="Next",
        command=on_click,
        padx=2,
        pady=2,
        relief=GROOVE,
    )
    next_button.pack(side=TOP)

    reset_button = Button(
        frame1,
        width=6,
        height=2,
        text="Reset",
        command=reset_map,
        padx=2,
        pady=2,
        relief=GROOVE,
    )

    reset_button.pack(side=TOP)

    frame1.pack(side=BOTTOM)

    create_map(root)

    root.mainloop()