import jsonpickle
from bottle import route, run, static_file, get, post, request, redirect

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
def add_or_update_node():
    node_id = request.json["node_id"]
    curr_elements = jsonpickle.decode(get_elements())

    if node_id == "":
        # create new node
        new_node = dict(group="nodes", data=dict(id=graph_utils.gen_id()))
        curr_elements["elements"].append(new_node)
    else:
        # TODO: update node in place
        pass
        # # update existing node
        #
        # node_to_remove = None
        # source_edges = []
        # # get node to remove
        # for ce in curr_elements["elements"]:
        #     if ce["group"] == "nodes":
        #         if ce["data"]["id"] == node_id:
        #             node_to_remove = ce
        #     elif ce["group"] == "elements":
        #         if ce["data"]["source"] == node_id:
        #
        # # get elements to remove
        #
        # if node_to_remove is not None:
        #     curr_elements["elements"].remove(node_to_remove)

    graph_utils.update_elements_with_dict(curr_elements)
    return jsonpickle.encode(curr_elements)


@post('/api/edge')
def add_or_update_edge():
    curr_elements = jsonpickle.decode(get_elements())
    # element_edge_targets = request.json["selected_nodes"]
    edge_id = request.json.get("edge_id", "")
    edge_source = request.json.get("edge_source", "")
    edge_target = request.json.get("edge_target", "")

    # FIXME: if edge_source or edge_target are not present, then return an error

    if edge_id == "":
        # create new edge
        new_edge = dict(group="edges", data=dict(id=graph_utils.gen_id(), source=edge_source, target=edge_target))
        curr_elements["elements"].append(new_edge)
    else:
        # update existing edge
        for ce in curr_elements["elements"]:
            if ce["group"] == "edges":
                if ce["data"]["id"] == edge_id:
                    ce["data"]["source"] = edge_source
                    ce["data"]["target"] = edge_target
                    break

    graph_utils.update_elements_with_dict(curr_elements)

    return jsonpickle.encode(curr_elements)

# entry point #
run(host='localhost', port=8080, debug=True)

# end of file #
