/**
 * Created by Josh on 03-Apr-16.
 */

var app = angular.module('main_app', []);
var cy = {};

function update_graph($scope) {
    cy = cytoscape({
        //container: document.getElementById('cy'), // container to render in
        container: angular.element(document.querySelector('#cy')),
        elements: $scope.elements,

        style: [
            {
                selector: 'node',
                style: {
                    'background-color': '#666',
                    'label': 'data(id)'
                }
            },

            {
                selector: 'edge',
                style: {
                    'width': 3,
                    'line-color': '#ccc',
                    'target-arrow-color': '#ccc',
                    'target-arrow-shape': 'triangle'
                }
            }
        ],

        layout: {
            name: 'random',
            fit: false,
            padding: 30
        }

    });
    cy.on('tap', 'node', function(event) {
            var tapped_node = event.cyTarget;
            var tapped_node_id = tapped_node.id();
            console.log('tapped node id: ' + tapped_node_id);

            $scope.add_form_data.id = tapped_node_id;

            var sel_nodes = cy.collection();
            sel_nodes = sel_nodes.add(tapped_node);
            var sel_edges = sel_nodes.outgoers();

            var sel_tgt_ids = [];
            var sel_tgt_coll = sel_edges.targets();
            var sel_targets = [];
            for (var i = 0; i < sel_tgt_coll.length; i++) {
                sel_tgt_ids.push(sel_tgt_coll[i].id());
                sel_targets.push(sel_tgt_coll[i].json());
            }
            console.log("selected target ids: " + JSON.stringify(sel_tgt_ids));

            $scope.add_form_data.selected_nodes = sel_targets;
            $scope.$apply();
        });
}

function update_nodes($scope) {
    var node_coll = cy.collection("node");
    $scope.nodes = [];
    for (var i = 0; i < node_coll.length; i++) {
        $scope.nodes.push(node_coll[i].json());
    }

}

app.controller('main_controller', function ($scope, $http) {
    $http({
        method: 'GET',
        url: '/api/elements'
    }).then(function get_elements_success(response) {
        $scope.elements = response.data.elements;
        update_graph($scope);
        update_nodes($scope);

        // add_form code
        $scope.add_form_data = {};

        console.log('set selected nodes');
        $scope.add_form_data.selected_nodes = [$scope.nodes[0].data.id];

        $scope.add_form_btn_click = function () {
            $http({
                method: 'POST',
                url: '/api/node',
                data: $scope.add_form_data,
                headers: { 'Content-Type': 'application/json'}
            })
                .success(function (response) {
                    // update the graph, etc., again
                    $scope.elements = response.elements;
                    update_graph($scope);
                    update_nodes($scope);
                });
        };



    }, function get_elements_error() {
        console.log("failed to get elements from server");
    });
});

