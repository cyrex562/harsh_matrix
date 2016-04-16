import graph_utils
import string
import random

graph_dict = graph_utils.get_elements_as_dict()

node_ids = {}







def run():
    # iterate over elements
    for element in graph_dict["elements"]:
        # record all old node_ids
        if element["group"] == "nodes":
            old_node_id = element["data"]["id"]
            new_node_id = gen_id()
            print "old_node_id: {0}, new_node_id: {1}".format(old_node_id,
                                                              new_node_id)
            #node_ids.append(dict(old_id=old_node_id, new_id=new_node_id))
            node_ids[old_node_id] = new_node_id

    for element in graph_dict["elements"]:
        if element["group"] == "nodes":
            # replace node id with new node id
            element["data"]["id"] = node_ids[element["data"]["id"]]

        elif element["group"] == "edges":
            element["data"]["id"] = gen_id()
            element["data"]["source"] = node_ids[element["data"]["source"]]
            element["data"]["target"] = node_ids[element["data"]["target"]]

    graph_utils.update_elements_with_dict(graph_dict)

if __name__ == "__main__":
    run()

# END OF FILE #
