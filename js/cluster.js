function create_cluster_diagram(container, source_data){
    // create a parameter to fit the number of cluster in the height of this graph
    total_height = container.style('height').replace('px', '');
    total_width = container.style('width').replace('px', '');

    last_node_pressed = null;

    console.log("eccola");
    console.log(source_data);

    // create a group for each topic
    var rect_height = 25;
    var occupied_height = rect_height * 8;
    var topic_groups = container.selectAll('g')
                .data(source_data)
                .enter()
                    // create a group for each cluster
                   .append('g')
                   .attr('class', function(d, i){
                        // console.log(d);
                        return 'topic-' + d.cluster_id;
                    });

    // create the group to contain the title
    var topic_name_groups = topic_groups.append('g')
                   .attr('transform', function(d, i){
                        return 'translate(' + ((i % 2) * (total_width / 2)) + ', ' + (Math.floor(i / 2) * rect_height) + ')';
                   })
                   .attr('class', 'topic-title');


   // add the rect for the topic name
   topic_name_groups.append('rect')
                   .attr('height', 30)
                   .attr('width', total_width / 2);


    // add the text for the topic
    var text_y_offset = 19;
    topic_name_groups.append('text')
                    .text(function(d){
                        return d.name;
                    })
                    .attr('text-anchor', 'middle')
                    // change the pointer to the text
                    .attr('class', 'pointer')
                    .attr('transform', 'translate(' + total_width / 4 + ', ' + text_y_offset + ')')

                   // set mouse hover events
                   .on('mouseover', function(){
                    // last_node_pressed.attr('class', parent_node.attr('class').replace(' hoverClus', ''));
                      var parent_node = d3.select(this.parentNode.parentNode);
                      //console.log(last_node_pressed == parent_node)
                      if (last_node_pressed != null){
                        //last_node_pressed.attr('class', last_node_pressed.attr('class').replace(' hoverClus', ''));
                          last_node_pressed.select(".word-cloud").style("opacity", 0);
                          parent_node.select(".word-cloud").style("opacity", 1);
                      }

                      if (last_node_pressed != parent_node) {
                          parent_node
                           .attr('class', parent_node.attr('class') + ' hoverClus');
                      }

                   })
                   .on('mouseout', function(){
                       var parent_node = d3.select(this.parentNode.parentNode);

                      if (last_node_pressed != null){
                        //last_node_pressed.attr('class', last_node_pressed.attr('class').replace(' hoverClus', ''));
                        if (last_node_pressed != parent_node) {
                          last_node_pressed.select(".word-cloud").style("opacity", 1);
                        }
                      }

                      if (last_node_pressed != parent_node) {
                          parent_node
                           .attr('class', parent_node.attr('class').replace(' hoverClus', ''));
                      }
                   })

                   // set the click mouse
                   .on('mousedown', function(d){
                        // update the other diagrams
                        // console.log(d3.select(this.parentNode).attr('class').split('-')[1].split(' ')[0]);
                       var cluster_id = d3.select(this.parentNode.parentNode).attr('class').split('-')[1].split(' ')[0];
                       selected_on_timeline(cluster_id);
                       update_force_diagram(cluster_id);

                       if (last_node_pressed != null){
                           var previous_class= last_node_pressed.attr('class');
                           last_node_pressed
                               .attr('class', previous_class.replace(' hoverClus', ''));
                          last_node_pressed.select(".word-cloud").style("opacity", 1);
                        }

                       last_node_pressed = d3.select(this.parentNode.parentNode);
                       var previous_class = last_node_pressed.attr('class');
                       last_node_pressed
                           .attr('class', previous_class + ' hoverClus');
                   });

       // create the group for the word cloud
       var word_cloud_height = total_height - occupied_height;
       var word_cloud_group = topic_groups.append('g')
                                            .attr('transform', 'translate(0, ' + occupied_height + ')')
                                            .attr('class', 'word-cloud');
       // add the rect to the group
       var word_cloud_height = total_height - occupied_height;
       word_cloud_group.append('rect')
                       .attr('rx', 20)
                       .attr('ry', 20)
                       .attr('height', word_cloud_height)
                       .attr('width', total_width);

      var real_cloud = word_cloud_group.append('g')
                                  .attr('transform', 'translate(' + total_width/2 + ', ' + (word_cloud_height/2) + ')')
                                  .attr('id', function(d, i){
                                    return 'wc' + (i+1);
                                  });
        


/*

       // define word position
       var word_positions =
                           [
                               [50, 50],
                               [total_width - 50, 50],
                               [30, word_cloud_height - 50],
                               [total_width - 50,  word_cloud_height - 50],
                               [150, 150]
                           ];

       // append words
       word_cloud_group.selectAll('text')
                           .data(function(d){
                                // console.log(d.words);
                                return d.words.filter(function(d, i){
                                                   return i < 5;
                                        });
                           })
                           .enter()
                               .append('text')
                               .text(function(d){
                                   return d.name;
                               })
                               .attr("transform", function(d, i) {
                                   return "translate(" + word_positions[i][0] + ',' + word_positions[i][1] + ')';
                               });
*/

      var wordsSizeMap = d3.scale.linear()
        .domain([0, 1])
        .range([16, 200]);  

      for (var idx = 0; idx < 13; idx++) {

          d3.layout.cloud().size([total_width, word_cloud_height])
          .words(source_data[idx].words.map(function(d) {
            return {text:d.name, size:wordsSizeMap(d.weight)};
          }))
          .padding(6)
          //.rotate(function() { return ~~(Math.random() * 2) * 90; })
          .rotate(function() { return 0; })
          //.font("Impact")
          .fontSize(function(d) { return d.size; })
          .on("end", draw)
          .start();


       function draw(words) {
          d3.select("#wc" + (idx+1))
          .selectAll("text")
            .data(words)
          .enter().append("text")
            .style("font-size", function(d) { return d.size + "px"; })
            //.style("font-family", "Impact")
            .style("fill", "white")
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
              return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function(d) { return d.text; });
        }
    }


    // update the tag cloud
    // var show_word_cloud = function(cluster_id, words){
        // console.log(cluster_id);

        // // add the rect to the group
        // var word_cloud_height = total_height - occupied_height;
        // word_cloud_group.append('rect')
        //                 .attr('rx', 20)
        //                 .attr('ry', 20)
        //                 .attr('height', word_cloud_height)
        //                 .attr('width', total_width)
        //                 .attr('y', occupied_height)
        //                 .style('fill', 'black')
        //                 // .attr('transform', 'translate(0, ' + occupied_height + ')')
        //                 .attr('class', 'topic-' + cluster_id);

        // // append words
        // var word_positions =
        //                     [
        //                         [word_cloud_height / 5, total_width / 6 * 3],
        //                         [word_cloud_height / 5 * 2, total_width / 6],
        //                         [word_cloud_height / 5 * 2, total_width / 6 * 4],
        //                         [word_cloud_height / 5 * 3, total_width / 6 * 2],
        //                         [word_cloud_height / 5 * 3, total_width / 6 * 3]
        //                     ];

        // word_cloud_group.selectAll('text')
        //                     .data(words.filter(function(d, i){
        //                                             return i < 4;
        //                     }))
        //                     .enter()
        //                         .append('text')
        //                         .style('fill', 'white')
        //                         .text(function(d){
        //                             return d.name;
        //                         })
        //                         .attr("transform", function(d, i) {
        //                             return "translate(" + word_positions[i][0] + ',' + word_positions[i][1] + ')';
        //                         });
        //                         // .attr('text-anchor', 'middle');
     // };

    // set initial group transition
    // cluster_groups.transition()
    //                 // delay works only in the first transition call when using sequenced transition
    //                 .duration(500)
    //                 .delay(function(d, i){
    //                     return i * 50;
    //                 })


    // **************** WORDS RECT
    // append a rect for each topic
    // var rect_offset = 120;
    // var rect_height = (total_height / source_data.length) - 5;
    // var rects_group = cluster_groups.append('rect')
    //                                     .attr('class', 'words-rect')
    //                                     .attr('height', rect_height * 2)
    //                                     .attr('width', total_width - rect_offset)
    //                                     .attr('x', rect_offset)
    //                                     .attr('y', -19)
    //                                     .attr('class', function(d, i){
    //                                         return 'topic-' + (i + 1);
    //                                     });

    // define the location of the text
    // text_y_positions = [rect_height - 5 , 15, rect_height - 5];

    // // define the map function
    // var max_radius = rect_height;
    // var mapRadius = d3.scale.linear()
    //                     .domain([0, 0.5])
    //                     .range([0, max_radius]);

}
