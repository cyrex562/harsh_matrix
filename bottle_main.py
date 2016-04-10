import os

import jsonpickle
from bottle import route, run, static_file, get, post, request

# DEFS #
STATIC_FILE_DIR = 'D:\\dev\\harsh_matrix\\static'
DATA_DIR = 'D:\\dev\\harsh_matrix\\data'


# FUNCTIONS #
@route('/main')
def main():
    return static_file('html/main.html', root=STATIC_FILE_DIR)


@route('/js/<filepath>')
def serve_angular_min(filepath):
    return static_file('/js/' + filepath, root=STATIC_FILE_DIR)


@route('/css/<filepath>')
def serve_bootstrap_min_css(filepath):
    return static_file('/css/' + filepath, root=STATIC_FILE_DIR)


@route('/data/<filepath>')
def serve_data_file(filepath):
    return static_file(filepath, root=DATA_DIR)


@get('/api/elements')
def get_elements():
    elements_file = open(os.path.join(DATA_DIR, "elements.json"), "r")
    elements_buf = elements_file.read()
    elements_file.close()
    elements_dict = jsonpickle.decode(elements_buf)
    elements_json = jsonpickle.encode(elements_dict)
    return elements_json


def update_elements(elements):
    elements_json = jsonpickle.encode(elements)
    elements_file = open(os.path.join(DATA_DIR, "elements.json"), "w+")
    elements_file.write(elements_json)
    elements_file.close()


@post('/api/node')
def add_or_update_node():
    element_update_id = request.json["id"]
    element_edge_targets = request.json["selected_nodes"]
    curr_elements = jsonpickle.decode(get_elements())
    edges_to_remove = []
    node_to_remove = None
    for ce in curr_elements["elements"]:
        if ce["group"] == "nodes":
            if ce["data"]["id"] == element_update_id:
                node_to_remove = ce
        elif ce["group"] == "edges":
            if ce["data"]["source"] == element_update_id:
                edges_to_remove.append(ce)
    if node_to_remove is not None:
        curr_elements["elements"].remove(node_to_remove)
    for etr in edges_to_remove:
        curr_elements["elements"].remove(etr)
    new_ele = dict(group="nodes", data=dict(id=element_update_id))
    new_edges = []
    for eet in element_edge_targets:
        target_node_id = eet["data"]["id"]
        new_edge = dict(
            group="edges",
            data=dict(id=element_update_id+target_node_id,
                      source=element_update_id,
                      target=target_node_id))
        new_edges.append(new_edge)
    curr_elements["elements"].append(new_ele)
    for ne in new_edges:
        curr_elements["elements"].append(ne)

    update_elements(curr_elements)

    return jsonpickle.encode(curr_elements)

# entry point #
run(host='localhost', port=8080, debug=True)

# end of file #
