import jsonpickle
from bottle import route, run, static_file, get, post, request, redirect, delete, \
    put

import graph_utils

# DEFS #
STATIC_FILE_DIR = 'D:\\dev\\harsh_matrix\\static'
DATA_DIR = 'D:\\dev\\harsh_matrix\\data'


# FUNCTIONS #
@route('/')
def default_route():
    return redirect("/main")


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
    elements_dict = graph_utils.get_elements_as_dict()
    elements_json = jsonpickle.encode(elements_dict)
    return elements_json


@post('/api/node')
def create_node():
    # node_id = request.json["node_id"]
    curr_elements = jsonpickle.decode(get_elements())
    new_node = dict(group="nodes", data=dict(id=graph_utils.gen_id()))
    curr_elements["elements"].append(new_node)
    graph_utils.update_elements_with_dict(curr_elements)
    return jsonpickle.encode(curr_elements)


@put('/api/node')
def update_node():
    node_id = request.json["node_id"]
    node_desc = request.json["node_desc"]
    node_name = request.json["node_name"]
    curr_elements = jsonpickle.decode(get_elements())
    for ce in curr_elements["elements"]:
        if ce["group"] == "nodes" and ce["data"]["id"] == node_id:
            # update node name
            if ce["data"]["description"] != node_desc.strip():
                ce["data"]["description"] = node_desc.strip()
            # update node desc
            if ce["data"]["name"] != node_name.strip():
                ce["data"]["name"] = node_name.strip()
    graph_utils.update_elements_with_dict(curr_elements)
    return jsonpickle.encode(curr_elements)


@delete('/api/node')
def delete_node():
    curr_elements = jsonpickle.decode(get_elements())
    node_id = request.json["node_id"]
    node_to_remove = None
    edges_to_remove = []
    for ce in curr_elements["elements"]:
        if ce["group"] == "nodes" and ce["data"]["id"] == node_id:
            node_to_remove = ce
        elif ce["group"] == "edges" and \
                (ce["data"]["source"] == node_id or
                         ce["data"]["target"] == node_id):
            edges_to_remove.append(ce)

    if node_to_remove is not None:
        curr_elements["elements"].remove(node_to_remove)

    if len(edges_to_remove) > 0:
        for edge in edges_to_remove:
            curr_elements["elements"].remove(edge)

    graph_utils.update_elements_with_dict(curr_elements)
    return jsonpickle.encode(curr_elements)


@post('/api/edge')
def create_edge():
    curr_elements = jsonpickle.decode(get_elements())
    # edge_id = request.json.get("edge_id", "")
    edge_source = request.json.get("edge_source", "")
    edge_target = request.json.get("edge_target", "")

    # FIXME: if edge_source or edge_target are not present, then return an error

    new_edge = dict(group="edges",
                    data=dict(id=graph_utils.gen_id(),
                              source=edge_source,
                              target=edge_target))
    curr_elements["elements"].append(new_edge)

    graph_utils.update_elements_with_dict(curr_elements)
    return jsonpickle.encode(curr_elements)


@put('/api/edge')
def update_edge():
    curr_elements = jsonpickle.decode(get_elements())
    edge_id = request.json.get("edge_id", "")
    edge_source = request.json.get("edge_source", "")
    edge_target = request.json.get("edge_target", "")

    for ce in curr_elements["elements"]:
        if ce["group"] == "edges":
            if ce["data"]["id"] == edge_id:
                ce["data"]["source"] = edge_source
                ce["data"]["target"] = edge_target
                break

    graph_utils.update_elements_with_dict(curr_elements)
    return jsonpickle.encode(curr_elements)


@delete('/api/edge')
def delete_edge():
    curr_elements = jsonpickle.decode(get_elements())
    edge_id = request.json["edge_id"]

    edge_to_remove = None
    for ce in curr_elements["elements"]:
        if ce["group"] == "edges" and ce["data"]["id"] == edge_id:
            edge_to_remove = ce

    if edge_to_remove is not None:
        curr_elements["elements"].remove(edge_to_remove)
        graph_utils.update_elements_with_dict(curr_elements)

    return jsonpickle.encode(curr_elements)


# entry point #
run(host='localhost', port=8080, debug=True)

# end of file #
