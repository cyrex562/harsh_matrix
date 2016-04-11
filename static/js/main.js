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
}

function update_nodes($scope) {
    $scope.nodes = [];
    // for (var i = 0; i < $scope.elements.length; i++) {
    //     if ($scope.elements[i].group === "nodes") {
    //         $scope.nodes.push($scope.elements[i]);
    //     }
    // }
    $scope.nodes = 
}

app.controller('main_controller', function ($scope, $http) {
    $http({
        method: 'GET',
        url: '/api/elements'
    }).then(function get_elements_success(response) {
        $scope.elements = response.data.elements;
        update_nodes($scope);
        update_graph($scope);

        // add_form code
        $scope.add_form_data = {};
        // TODO: fix option selection
        $scope.add_form_data.selected_nodes = [$scope.nodes[0].data];

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
                    update_nodes($scope);
                    update_graph($scope);
                });
        };

        cy.on('tap', 'node', function(event) {
            var tapped_node = event.cyTarget;
            console.log('tapped node id: ' + tapped_node.id());
            var tapped_node_id = event.cyTarget.id();

            // TODO: fill in form with selected data
            $scope.add_form_data.id = tapped_node_id;

            // set selected options by getting source edges
            var sel_edges = cy.$('#' + tapped_node_id).outgoers();
            var sel_targets = sel_edges.targets();
            $scope.add_form_data.selected_nodes = [];
            for (var i = 0; i < sel_targets.length; i++) {
                var sel_tgt_id = sel_targets[i].id();
                $scope.add_form_data.selected_nodes.push(sel_tgt_id);
            }
        });

    }, function get_elements_error() {
        console.log("failed to get elements from server");
    });
});


