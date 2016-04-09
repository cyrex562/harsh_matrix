/**
 * Created by Josh on 03-Apr-16.
 */

var config = {
    dataSource: 'data/test.json',
};

var cy = cytoscape({
    container: document.getElementById('cy'), // container to render in

    elements: [
        {
            data: {id: '0'}
        },
        {
            data: {id: '1'}
        },
        {
            data: {id: '010', source: '0', target: '1'}
        },
        {
            data: {id: '011', source: '0', target: '1'}
        }
    ],

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
        name: 'grid',
        rows: 1
    }

});