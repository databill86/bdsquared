function selected_on_timeline(cluster_id){
    var ids=[1,4,6,7,8,12,13,14,15,16,17,18,19]
    ids.forEach(function(d,i){
        var path = d3.select('#timeline path.topic-'+d)
        var previous_class= path.attr('class');

        if (d==cluster_id){
            var previous_class= path.attr('class');
            var new_class=previous_class.replace('unselected','');
            // console.log('same')
            // console.log(path.attr('class'));
            path.attr('class',new_class+" selected")
            // console.log(path.attr('class'));
        }else{
            var previous_class= path.attr('class');
            var new_class=previous_class.replace('selected','');
            // console.log('diferent')
            // console.log(path.attr('class'));
            path.attr('class',new_class+" unselected")
            // console.log(path.attr('class'));
        }
    });


}

function create_timeline_diagram(container, source_data){

    // create the axes
    // console.log(source_data)
    timeline_width = d3.select('#timeline').style('width').replace('px','');
    timeline_height = d3.select('#timeline').style('height').replace('px','');
    var margin_bottom = 5;
    var margin_left= 15;
    var margin_right= 10;
    var margin_top= 20;
    var timeline_height=timeline_height-margin_bottom;

    var timeline_width=timeline_width-margin_left-margin_right


    //defining my own palette: array of 10 colors, already ordered
    var my_palette_10 = ['#940A30', '#F44D4D', '#9FF3333', '#F9B513', '#99C651', '#639670', '#163F46', '#1D5F73', '#00988E', '#1AB7AC']



    //perperaing the data:
    source_data.forEach(function(d,i){
        d.months.forEach(function(d,i){
            //creation of the dateobject
            d.month_obj=new Date(d.month_id.split('-')[0], d.month_id.split('-')[1]-1)
        });

    });
    source_data.forEach(function(d,i){
        //sorting the array
        d.months.sort(function(a,b){
            if (a.month_obj<b.month_obj) return -1
            if (a.month_obj>b.month_obj) return 1
            if (a.month_obj==b.month_obj) return 0
        })

    });


    d3.json('data/clusters.json', function(cluster_data){
        //filter the non important clusters: /*Everything is appended again, becaus is unsiconrinized otherwise*/
        var ids=[]
        cluster_data.forEach(function(d,i){
            ids.push(d.cluster_id)
        })
        var counter=0
        source_data=source_data.filter(function(d,i,a){
            return ids.indexOf(d.cluster_id) != -1
        })

        //limits discovering
        var maxmonths=d3.max(source_data,function(d,i){
            return d3.max(d.months,function(d,i){ return d.month_obj})
        })

        var minmonths=d3.min(source_data,function(d,i){
            return d3.min(d.months,function(d,i){ return d.month_obj })
        })

        var max_y =d3.max(source_data,function(d,i){
            return d3.max(d.months,function(d,i){ return d.weight })
        })


        var min_y=0;

        //proportional division for axes according to the source_data
        var mapx = d3.time.scale()
                    .domain([minmonths, maxmonths])
                    .range([margin_left, timeline_width])

        var mapy = d3.scale.linear()
                    .domain([min_y, max_y])
                    .range([timeline_height-margin_bottom, margin_top])


        // create the trend lines
        line = d3.svg.area()
                    .x(function(d, i){

                            return mapx(d.month_obj);

                    })
                    .y(function(d, i){

                            return mapy(d.weight);
                    })
                    .interpolate('basis')
                    .y0(mapy(0))

        var elements = container.selectAll('path')
                        .data(source_data)
                        .enter()
                           .append('path')
                           .attr('d',function(d,i){
                                return line(d.months)
                           })//line(source_data[0]))
                           .attr('class',function(d,i){
                                return 'timePath topic-'+d.cluster_id
                            })


        //axis creation:

        var padding = 5

        maxmonths.setMonth( maxmonths.getMonth()+1 ) /*this is make because otherwise it ends at december*/
        var mapxAxis = d3.time.scale()
                    .domain([minmonths, maxmonths])
                    .range([margin_left, timeline_width])

        var xAxis = d3.svg.axis()
                            .scale(mapxAxis)
                            .tickSize(timeline_height-padding-12,2)
                            .tickPadding(5)
                            .tickValues([new Date(2011,0),new Date(2012,0),new Date(2013,0)])
                            .orient('top')

        container.append('g')
                 .attr('class','xAxis')
                 .attr('transform','translate(0,'+timeline_height+')')
                 .call(xAxis);

    });
}
