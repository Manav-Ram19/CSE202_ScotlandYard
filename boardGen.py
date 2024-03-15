import string
import copy

from board import SYTransport
from typing import Dict, Tuple


OUTPUT_DIR = "boards/"

SOURCE_FILE = "board.txt"

NUM_VERTICES = 200

def read_input_file(input_file_name: string) -> list:
    with open(input_file_name, 'r') as file:
        lines = file.readlines()
    
    num_vertices = int(lines[0])
    assert(num_vertices == NUM_VERTICES)

    rem_lines = lines[1:]
    return rem_lines

def convert_string_list_to_graph(lines: string) -> Dict[int, Tuple[int, SYTransport]]:
    edges = dict()
    for line in lines:
        line_split = line.replace("\n", "").split(" ")
        line_final = [int(line_split[0]), int(line_split[1]), SYTransport[line_split[2]].value]

        loc1 = line_final[0]
        loc2 = line_final[1]
        transport = line_final[2]

        if loc1 not in edges:
            edges[loc1] = []
        edges[loc1].append((loc2, transport))

        if loc2 not in edges:
            edges[loc2] = []
        edges[loc2].append((loc1, transport))
    return edges

def copy_graph_with_offset(original_graph: Dict[int, Tuple[int, SYTransport]],
                           offset: int) -> Dict[int, Tuple[int, SYTransport]]:
    copy_graph = dict()
    for node in original_graph:
        copy_graph[node+offset] = []
        for neighbor in original_graph[node]:
            (neighbor_node, transport) = neighbor
            copy_graph[node+offset].append((neighbor_node+offset, transport))
    return copy_graph

def build_long_graph(original_graph: Dict[int, Tuple[int, SYTransport]],
                    num_copies: int) -> Dict[int, Tuple[int, SYTransport]]:
    assert(num_copies > 1)

    cur_offset = 0
    final_graph = copy.deepcopy(original_graph)

    LEFT_CONNECT = [18, 43, 92, 120, 144, 176]
    RIGHT_CONNECT = [56, 91, 107, 119, 136, 162]

    for copy_count in range(1, num_copies):
        cur_offset = copy_count*len(original_graph)
        copied_graph = copy_graph_with_offset(original_graph, cur_offset)

        prev_offset = cur_offset - len(copied_graph)

        old_connect_nodes = [n + prev_offset for n in RIGHT_CONNECT]
        new_connect_nodes = [n + cur_offset for n in LEFT_CONNECT]
        
        final_graph = stitch_graphs(final_graph, copied_graph, old_connect_nodes, new_connect_nodes)

    return final_graph

def stitch_graphs(cur_graph: Dict[int, Tuple[int, SYTransport]],
                  new_graph: Dict[int, Tuple[int, SYTransport]],
                  old_connect_nodes: list,
                  new_connect_nodes: list) -> Dict[int, Tuple[int, SYTransport]]:
    
    # Add new nodes to cur_graph
    for node in new_graph:
        cur_graph[node] = []
        for neighbor in new_graph[node]:
            (neighbor_node, transport) = neighbor
            cur_graph[node].append((neighbor_node, transport))
    
    # Stitch old to new
    for old_node, new_node in zip(old_connect_nodes, new_connect_nodes):
        cur_graph[old_node].append((new_node, SYTransport.TAXI))
        cur_graph[new_node].append((old_node, SYTransport.TAXI))
    
    return cur_graph

def write_graph_to_file(output_file_name: string,
                        graph: Dict[int, Tuple[int, SYTransport]]):
    with open(output_file_name, 'w') as file:
        file.write(f"{len(graph)}\n")

        for node in graph:
            for neighbor in graph[node]:
                neighbor_node, transport_num = neighbor
                transport = SYTransport.TAXI

                if transport_num == 2: transport = SYTransport.BUS
                elif transport_num == 3: transport = SYTransport.RAIL

                print(node, neighbor_node, transport)
                file.write(f"{node} {neighbor_node} {transport.name}\n")

def main():
    inp_graph = convert_string_list_to_graph(read_input_file(SOURCE_FILE))

    for num_copies in range(2,11):
        new_graph = build_long_graph(inp_graph, num_copies)

        output_file_name = f"{OUTPUT_DIR}board_{num_copies*200}.txt"
        write_graph_to_file(output_file_name, new_graph)
    
    
if __name__ == "__main__":
    main()