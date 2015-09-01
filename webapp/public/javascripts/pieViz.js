/**
 * Created by sdiemert on 15-08-30.
 */

function toolTipMouseOut(div) {
    div.transition()
        .duration(500)
        .style("opacity", 0);
}

function toolTipMouseOver(d, div, parent, color) {

    div.transition()
        .duration(200)
        .style("opacity", 0.9);
    div.html(
        d.data.name + "<br/>" +
        "Ratio: " + (d.data.count / d.data.total * 100).toFixed(2) + " % <br/>" +
        "Total: " + d.data.count
    ).style("background", color)
        .style("top", (d3.event.pageY ) + "px")
        .style("left", (d3.event.pageX) + "px");

}

function compute(data) {

    console.log(data);

    var sum = 0;

    for (var i in data) {

        sum += data[i];

    }

    var toReturn = [];

    for (i in data) {

        toReturn.push({
            name : i,
            value: data[i] / sum,
            count : data[i],
            total: sum
        })

    }

    console.log(toReturn);
    return toReturn;
}

function pieViz(data, parent) {

    var allData = compute(data);

    var div = d3.select("#tooltip-holder").append("div")
        .attr("class", "tooltip")
        .style({"opacity": 0, "width": "150"});

    var radius     = 150,
        margin     = 50,
        height     = 450;
    var width      = 450; //$(parent).width();


    var colors = ["#6FBF51", "#F90", "#FF4791", "#40CAFC"];
    var offColors = ["#8CCC74", "#FFAD33", "#FF6CA7", "#66D5FD"];

    var canvas = d3.select(parent)
        .append("svg:svg")
        .attr("width", width)
        .attr("height", (radius * 2 + 2 * margin) > height ? (radius * 2 + 2 * margin) : height)
        .append("svg:g")
        .attr("transform", "translate(" + (width/1.5) + "," + (1.5 * radius) + ")");

    var arc = d3.svg.arc()
        .outerRadius(radius)
        .innerRadius(radius / 2);

    var pie = d3.layout.pie()
        .value(function (d) {
            return d.value;
        }).sort(null);


    var g = canvas.selectAll(".arc")
        .data(pie(allData))
        .enter().append("g")
        .attr("class", "arc");

    g.append("path")
        .attr("d", arc)
        .style("fill", function (d, i) {
            return colors[i % colors.length];
        }).on("mouseover", function (d, i) {

            toolTipMouseOver(d, div, parent, offColors[i % offColors.length])

        }).on('mouseout', function (d, i) {

            toolTipMouseOut(div);

        });

    g.append("text")
        .attr("transform", function (d) {
            return "translate(" + arc.centroid(d) + ")";
        })
        .attr("dy", ".35em")
        .style("text-anchor", "middle");
}
