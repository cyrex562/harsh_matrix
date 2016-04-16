/**
 * Created by Josh on 03-Apr-16.
 */

var app = angular.module('main_app', []);
var cy = {};

function update_graph($scope) {
    cy = cytoscape({
        container: angular.element(document.querySelector('#cy')),
        elements: $scope.elements,

        boxSelectionEnabled: true,
        selectionType: 'additive',

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
            },
            {
                selector: 'node:selected',
                style: {
                    'background-color': '#ff6666'
                }
            }
        ],

        layout: {
            name: 'random',
            fit: false,
            padding: 30
        }

    });
    cy.on('tap', 'node', function (event) {
        var tapped_node = event.cyTarget;
        $scope.node_form_data.node_id = tapped_node.id();
        console.log('tapped node id: ' + $scope.node_form_data.node_id);

        var idx_to_remove = -1;
        for (var i = 0; i < $scope.sel_nodes.length; i++) {
            if ($scope.sel_nodes[i] === tapped_node.id()) {
                idx_to_remove = i;
            }
        }
        if (idx_to_remove >  -1) {
            $scope.sel_nodes.splice(idx_to_remove, 1);
        } else {
            $scope.sel_nodes.push(tapped_node.id());
        }

        if ($scope.sel_nodes.length === 1) {
            $scope.edge_form_data.edge_source = $scope.sel_nodes[0];
        } else if ($scope.sel_nodes.length === 2) {
            $scope.edge_form_data.edge_target = $scope.sel_nodes[1];
        }

        $scope.$apply();
    });

    cy.on('tap', 'edge', function (event) {
        var tapped_edge = event.cyTarget;
        $scope.edge_form_data.edge_id = tapped_edge.id();
        $scope.edge_form_data.edge_source_id = tapped_edge.source().id();
        $scope.edge_form_data.edge_target_id = tapped_edge.target().id();
        console.log("tapped edge id: " + $scope.edge_form_data.edge_id);
        console.log("tapped edge source: " + $scope.edge_form_data.edge_source_id);
        console.log("tapped edge target: " + $scope.edge_form_data.edge_target_id);
        $scope.$apply();
    });
}

function update_nodes($scope) {
    var node_coll = cy.collection("node");
    $scope.sources = [];
    $scope.targets = [];
    for (var i = 0; i < node_coll.length; i++) {
        $scope.sources.push(node_coll[i].json());
        $scope.targets.push(node_coll[i].json());
    }
}

app.controller('main_controller', function ($scope, $http) {
    $http({
        method: 'GET',
        url: '/api/elements'
    }).then(function get_elements_success(response) {
        // node form code
        $scope.num_sel_nodes = 0;
        $scope.sel_nodes = [];
        $scope.node_form_data = {};
        $scope.edge_form_data = {};

        $scope.elements = response.data.elements;
        update_graph($scope);
        update_nodes($scope);

        $scope.create_node_btn_click = function () {
            $http({
                method: 'POST',
                url: '/api/node',
                data: {"node_id": ""},
                headers: {'Content-Type': 'application/json'}
            })
                .success(function (response) {
                    $scope.elements = response.elements;
                    update_graph($scope);
                    update_nodes($scope);
                });
        };

        $scope.update_node_btn_click = function () {
            $http({
                method: 'POST',
                url: '/api/node',
                data: $scope.node_form_data,
                headers: {'Content-Type': 'application/json'}
            })
                .success(function (response) {
                    $scope.elements = response.elements;
                    update_graph($scope);
                    update_nodes($scope);
                });
        };

        $scope.delete_node_btn_click = function() {
            $http({
                method: 'DELETE',
                url: '/api/node',
                data: $scope.node_form_data,
                headers: {'Content-Type': 'application/json'}
            })
                .success(function (response) {
                    update_graph($scope);
                    update_nodes($scope);
                });
        };

        $scope.upsert_edge_btn_click = function () {
            $http({
                method: 'POST',
                url: '/api/edge',
                data: $scope.edge_form_data,
                headers: {'Content-Type': 'application/json'}
            })
                .success(function (response) {
                    $scope.elements = response.elements;
                    update_graph($scope);
                    update_nodes($scope);
                });
        };


    }, function get_elements_error() {
        console.log("failed to get elements from server");
    });
});

