// **************** SVG SELECTION
cluster_svg = d3.select("#cluster");
timeline_svg = d3.select("#timeline");
force_svg = d3.select("#force");

// **************** ASPECT
//defining the color palette: array of 10 colors, already ordered
var my_palette_10 = ['#940A30', '#C63A3B', '#F44D4D', '#FF3333', '#F37035', '#F9B513', '#99C651', '#639670', '#277E70', '#163F46', '#1D5F73', '#00988E', '#1AB7AC'];
//console.log(my_palette_10)


// **************** DATA LOADING
// TODO: change source when run in server

// CLUSTER
var clustersData=null
d3.json('data/clusters.json', function(source_data){
    // logging
    console.log(source_data);
    clustersData=source_data;
    create_cluster_diagram(cluster_svg, source_data);


    updated_graph_from_file('data/force_testate.json');

});

function updated_graph_from_file(filename){
    d3.json(filename, function(source_data){
        // logging
        console.log(source_data);

        create_force_diagram(force_svg, source_data);
    });    
}


// TIMELINE
d3.json('data/timeline.json', function(source_data){
    // logging
    console.log(source_data);

    create_timeline_diagram(timeline_svg, source_data);
});


