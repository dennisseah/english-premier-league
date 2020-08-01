var width = 800,
    height = 800;

var projection = d3.geo
    .albers()
    .center([0, 55.4])
    .rotate([4.4, 0])
    .parallels([50, 60])
    .scale(1200 * 5)
    .translate([width / 3, height / 6]);

var path = d3.geo
    .path()
    .projection(projection)
    .pointRadius(2);

var svg = d3
    .select('body')
    .append('svg')
    .attr('width', width)
    .attr('height', height);

var tooltip = d3
    .select('body')
    .append('div')
    .attr('class', 'tooltip')
    .style('opacity', 0);

d3.json('map/uk.json', function (error, uk) {
    d3.csv('map/clubs.csv', function (clubs) {
        var subunits = topojson.object(uk, uk.objects.subunits);

        svg
            .selectAll('.subunit')
            .data(subunits.geometries)
            .enter()
            .append('path')
            .attr('class', function (d) {
                return 'subunit ' + d.id;
            })
            .attr('d', path);

        svg
            .append('g')
            .selectAll('path')
            .data(clubs)
            .enter()
            .append('circle')
            .attr('cx', function (d) {
                return projection([d.lon, d.lat])[0];
            })
            .attr('cy', function (d) {
                return projection([d.lon, d.lat])[1];
            })
            .attr('r', function (d) {
                return 4;
            })
            .style('fill', function (d) {
                return d.color;
            })
            .on('mouseover', function (d) {
                tooltip
                    .transition()
                    .duration(200)
                    .style('opacity', 0.9);
                tooltip
                    .html(d.club)
                    .style('left', d3.event.pageX + 'px')
                    .style('top', d3.event.pageY - 28 + 'px');
            })
            .on('mouseout', function (d) {
                tooltip
                    .transition()
                    .duration(500)
                    .style('opacity', 0);
            });
    });
});
