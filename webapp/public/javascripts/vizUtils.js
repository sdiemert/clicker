/**
 * Created by sdiemert on 15-08-30.
 */

function toolTipMouseOut(div) {
    div.transition()
        .duration(500)
        .style("opacity", 0);
}

function toolTipMouseOver(num, den, div, parent, color) {

    var p = $(parent + " > svg").offset();

    if (typeof d.time != "object") {
        d.time = new Date(d.time * 1000);
    }
    div.transition()
        .duration(200)
        .style("opacity", 0.9);
    div.html(
        name + "<br/>" +
        "Ratio: " + (num / den * 100).toFixed(2) + " % <br/>" +
        "Total: " + num
    )
        .style("background", color)
        .style("top", (d3.event.pageY ) + "px")
        .style("left", (d3.event.pageX) + "px");
}
