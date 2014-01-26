Completed_nodes=[]
Completed_links=[]


var ids=[1,4,6,7,8,12,13,14,15,16,17,18,19]
var maxForce
var minForce
var link
var node
var nodes
var links=[]

force = null;

function update_force_diagram(id){

    var category_id=ids.indexOf(parseInt(id))
    // console.log(nodes)

    // console.log(nodes)

    var nodesidx=[]
    nodes=[]
    // console.log(nodes)
    Completed_nodes.forEach(function(d_node){
        //¿update nodes weight?// first implement it
        if(d_node.type=='word'){
            d_node.categories.forEach(function(d,i){
                if(d.category==id){
                    nodes.push(d_node)
                    nodesidx.push(d_node.name)
                }
            })
        }else{
            nodes.push(d_node)
            nodesidx.push(d_node.name)
        }
    })

    // console.log(nodesidx)

    // console.log(nodes)


    links=[]
    Completed_links.forEach(function(d_link){
        d_link.categories.forEach(function(d,i){
            if(d.category == id){
                var new_s =nodesidx.indexOf(d_link.source_name)
                var new_t = nodesidx.indexOf(d_link.target_name)
                d_link.source=new_s
                d_link.target=new_t
                links.push(d_link)
            }
        })
    })
    // console.log(links)


    d3.selectAll('#force *').remove()

    draw_graph()

}

function draw_graph(){
        //links creation
        // console.log(minForce,maxForce)
        var opacityLinkMap = d3.scale.linear()
        .domain([minForce, maxForce])
        .range([0, 1])

        link = svg.selectAll(".link")
        .data(links)
        .enter()
            .append('line')
            .attr('class','link')
            .style('stroke-opacity',function(d,i){
                return opacityLinkMap(d.force)
            })

        //nodes creation
        node = svg.selectAll('.node')
        .data(nodes)
        .enter()
            .append('g')
            .attr('class',function(d,i){
                return "node "+d.type
            })

        var nodeSizeMap = d3.scale.linear()
        .domain([Math.log(1), Math.log(5000)])
        .range([1, 15])


        node.append('circle')
        .attr('r',function(d,i){
            return nodeSizeMap(Math.log(d.weightJSON))
        })



        node.append('text')
        .text(function(d){
            return d.name
        })
        .attr('dy',5)
        .attr('class', 'pointer-default');

        //Definition of the force layout
        var distanceMap = d3.scale.pow()
        .domain([-13, -0.07])
        .range([400,0])
        .exponent(10)

        var linkStrengthMap = d3.scale.pow()
        .domain([-13, -0.07])
        .range([0, 1])
        .exponent(0.1)

        force = d3.layout.force()
        .gravity(0.5)
        .linkDistance(function(d,i){
                // console.log(d.force, distanceMap(d.force))
                return distanceMap(d.force)
            })
        .linkStrength(function(d,i){
            return linkStrengthMap(d.force)
        })
        .charge(function(d,i){
            if (d.type=='word') return -10000
                else return -10000
            })
        .friction(0.1)
        .size([svg_width, svg_height]);





        //start the force
        force.nodes(nodes)
        .links(links)
        .start();

        //update the force operation
        force.on('tick',function(){
            link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

            node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

        })
}

function create_force_diagram(container,source_data){
        //creation of the SVG
        // console.log(source_data)
        svg_width  = d3.select('#seconcol').style('width').replace('px','')
        svg_height = d3.select('#seconcol').style('height').replace('px','')

        svg = d3.select('#force')
        .attr('height',svg_height)
        .attr('width',svg_width)



        //data preraration
        var edgesRead = source_data.edges
        nodes = source_data.nodes


        clustersDict = {}
        clustersData.forEach(function(category,i){
            category.words.forEach(function(d,i){
                if (clustersDict[d.name]==undefined){
                    clustersDict[d.name] = [{'wieght':d.weight,'category':category.cluster_id,'name':d.name}]
                }else{
                    clustersDict[d.name].push({'wieght':d.weight,'category':category.cluster_id,'name':d.name})
                }
            })
        })


        var nodesidx=[]
        nodes.forEach(function(d,i){
            // console.log(clustersDict[d.name])
            d.categories=clustersDict[d.name];
            d.weightJSON = d.weight
            nodesidx.push(d.name) //nodesidx helps the creation of the link array.
            Completed_nodes.push(d)
        })

        /*var links=[]*/
        maxForce=-10000;
        minForce=10000;
        edgesRead.forEach(function(d,i){
            s=nodesidx.indexOf(d.word)
            t=nodesidx.indexOf(d.source)
            categories_object_copy = clustersDict[d.word].slice(0);
            //links.push({'source':s,'target':t,'force':d.force,'big_force':d.force,'clusters':d.clusters,'categories':'test'} )
            links.push({'source':s,'target':t,'force':d.force,'big_force':d.force,'clusters':d.clusters,'categories':categories_object_copy} )
            Completed_links.push({'source':s,'source_name':d.word,'target':t,'target_name':d.source,'force':d.force,'big_force':d.force,'clusters':d.clusters,'categories':categories_object_copy} )
            if (d.force>maxForce) maxForce=d.force
                if (d.force<minForce) minForce=d.force
            //maxForce = d.force>maxForce : d.Force : maxForce
    })
        // console.log(links)

        draw_graph();
}


