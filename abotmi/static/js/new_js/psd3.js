/**
 * 
 */

function open_breakup_piechart(breakup_data, main_cats) {
    var mn_cats_color_meta_details = "";
    if (!$.isEmptyObject(main_cats)){
        $("#mn_cats_color_meta").empty();
        $.each(main_cats, function (mn_cat_name, mn_cat_color) {
            $("#mn_cats_color_meta").append(
                "<li>"+
                    "<div class='input-color'>"+
                        "<span>" + mn_cat_name.toUpperCase()+"</span>"+
                        "<div class='color-box' style='background-color: "+mn_cat_color+";'></div>"+    
                    "</div>"+
                "</li>"
            );
        });
    }
    var config = {
        containerId: "chartContainer",
        width: 300,
        height: 300,
        data: breakup_data,
        heading: {
            text: "Reputation Index",
            pos: "top"
        },
        value: "oaPercentage",
        inner: "children",
        tooltip: function (d) {
            var per = d.percentage;
            if (_this.zoomStack=="") {
                per = d.oaPercentage;
            }
            return "<p>" + d.name.replace(/_/g, ' ') + " <br/> " + per + "%</p>";
        },
        transition: "ease",//"bounce",
        transitionDuration: 500,
        donutRadius: 50,
        highlightColor: function (d) {
            return d.data.fill_color;
        }
    };
    var samplePie = new psd3.Pie(config);
}


function go_back() {
    if (_this.zoomStack != undefined && _this.zoomStack.length > 0) {
        var tmp = [];
        d3.select("#" + _this.tooltipId).remove();
        d3.select("#" + _this.config.containerId + "_svg") //.remove();
            .transition()
            .ease(_this.config.drilldownTransition)
            .duration(_this.config.drilldownTransitionDuration)
            .style("height", 0)
            .remove()
            .each("end", function () {
                tmp = _this.zoomStack.pop();
                _this.drawPie(tmp);
            });
    }
}

var psd3 = psd3 || {};
var _this = {};
psd3.Graph = function (config) {
    _this = this;
    _this.config = config;
    _this.defaults = {
        width: 400,
        height: 400,
        value: "value",
        inner: "inner",
        label: function (d) {
            return d.data.value;
        },
        tooltip: function (d) {
            if (_this.config.value !== undefined) {
                return d[_this.config.value];
            } else {
                return d.value;
            }

        },
        transition: "linear",
        transitionDuration: 1000,
        donutRadius: 0,
        gradient: false,
        colors: d3.scale.category20(),
        labelColor: "black",
        drilldownTransition: "linear",
        drilldownTransitionDuration: 0,
        stroke: "white",
        strokeWidth: 2,
        highlightColor: "orange"
    };
    for (var property in _this.defaults) {
        if (_this.defaults.hasOwnProperty(property)) {
            if (!config.hasOwnProperty(property)) {
                config[property] = _this.defaults[property];
            }
        }
    }
};

psd3.Pie = function (config) {
    psd3.Graph.call(_this, config);
    _this.zoomStack = [];
    var pos = "top";
    if (_this.config.heading !== undefined && _this.config.heading.pos !== undefined) {
        pos = _this.config.heading.pos;
    }
    _this.drawPie(config.data);
    //Commented for reference
    // if (pos == "top") {
    //     _this.setHeading();
    // }
    // if (pos == "bottom") {
    //     _this.setHeading();
    // }
};

_this = Object.create(psd3.Graph.prototype);

_this.constructor = psd3.Pie;

function isEmpty(data) {
    for (var key in data) {
        if (data.hasOwnProperty(key))
            return false;
    }
    return true;
}

_this.findMaxDepth = function (dataset) {
    if (dataset === null || dataset === undefined || dataset.length < 1) {
        return 0;
    }
    var currentLevel;
    var maxOfInner = 0;
    for (var i = 0; i < dataset.length; i++) {
        var maxInnerLevel = _this.findMaxDepth(dataset[i][_this.config.inner]);
        if (maxOfInner < maxInnerLevel) {
            maxOfInner = maxInnerLevel;
        }
    }
    currentLevel = 1 + maxOfInner;
    return currentLevel;
};

_this.setHeading = function () {
    if (this.config.heading !== undefined) {
        d3.select("#" + this.config.containerId)
            .append("div")
            .style("text-align", "center")
            .style("width", "" + this.config.width + "px")
            .style("padding-top", "20px")
            .style("padding-bottom", "20px")
            .append("strong")
            .text(this.config.heading.text);
    }
};

_this.mouseover = function (d) {
    d3.select("#" + _this.tooltipId)
        .style("left", (d3.event.clientX + window.scrollX) + "px")
        .style("top", (d3.event.clientY + window.scrollY) + "px")
        .select("#value")
        .html(_this.config.tooltip(d.data, _this.config.label));
    d3.select("#" + _this.tooltipId).classed("psd3Hidden", false);
    var breadcrumb_data =  "";
    if (d.data.mn_cat_name != undefined){
        breadcrumb_data = breadcrumb_data + "<span class='breadcrumb-span'>" + d.data.mn_cat_name.replace(/_/g, ' ') + "</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
    }
    if (d.data.sb_cat_name != undefined) {
        breadcrumb_data = breadcrumb_data + "<span class='breadcrumb-span'>" + d.data.sb_cat_name.replace(/_/g, ' ') + "</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
    } 
    breadcrumb_data = breadcrumb_data + "<span class='breadcrumb-span'>" + d.data.name.replace(/_/g, ' ') + "</span>" + " &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span style='font-weight:600' class='breadcrumb-span-points'>"+d.data.points+"</span>"
    $('#show_breadcrumbs').html(breadcrumb_data)
};

_this.mouseout = function (d) {
    d3.select("#" + _this.tooltipId).classed("psd3Hidden", true);
    $('#show_breadcrumbs').text("Hover on map element to see breadcrumb and points.");
};

_this.drawPie = function (dataset) {
    $('#show_breadcrumbs').text("Hover on map element to see breadcrumb and points.");
    if (_this.zoomStack.length == 0 && dataset.length == 3) {
        $("#go_back_breakup_btn").hide();
    } else {
        $("#go_back_breakup_btn").show();
    }
    if (dataset === null || dataset === undefined || dataset.length < 1) {
        return;
    }
    _this.arcIndex = 0;
    var svg = d3.select("#" + _this.config.containerId)
        .append("svg")
        .attr("id", _this.config.containerId + "_svg")
        .attr("width", _this.config.width)
        .attr("height", _this.config.height);
    _this.tooltipId = _this.config.containerId + "_tooltip";
    var tooltipDiv = d3.select("#" + _this.config.containerId).append("div")
        .attr("id", _this.tooltipId)
        .attr("class", "psd3Hidden psd3Tooltip");
    tooltipDiv.append("p")
        .append("span")
        .attr("id", "value")
        .text("100%");

    // to contain pie cirlce
    var radius;
    if (_this.config.width > _this.config.height) {
        radius = _this.config.width / 2;
    } else {
        radius = _this.config.height / 2;
    }
    var innerRadius = _this.config.donutRadius;
    var maxDepth = _this.findMaxDepth(dataset);
    var outerRadius = innerRadius + (radius - innerRadius) / maxDepth;
    var originalOuterRadius = outerRadius;
    var radiusDelta = outerRadius - innerRadius;
    //Draw function variables and function call ----------------------------
    var totalRadius = radius;
    var startAngle = 0;
    var endAngle = 360 * 22 / 7 / 180;
    var parentCentroid = [0, 0];
    draw(svg, totalRadius, dataset, dataset, dataset.length, innerRadius, outerRadius, radiusDelta, startAngle, endAngle, parentCentroid)
    //end Draw function variables and function call ----------------------------
};


_this.customArcTween = function (d) {
    var start = {
        startAngle: d.startAngle,
        endAngle: d.startAngle
    };
    var interpolate = d3.interpolate(start, d);
    return function (t) {
        return d.arc(interpolate(t));
    };
};

_this.textTransform = function (d) {
    return "translate(" + d.arc.centroid(d) + ")";
};

_this.textTitle = function (d) {
    return d.data[_this.config.value];
};

function draw(svg, totalRadius, dataset, originalDataset, originalDatasetLength, innerRadius, outerRadius, radiusDelta, startAngle, endAngle, parentCentroid) {
    if (dataset === null || dataset === undefined || dataset.length < 1) {
        return;
    }
    psd3.Pie.prototype.textText = function (d) {
        return _this.config.label(d);
    };

    var pie = d3.layout.pie();
    pie.sort(null);
    pie.value(function (d) {
        return d[_this.config.value];
    });
    pie.startAngle(startAngle)
        .endAngle(endAngle);

    var dblclick = function (d) {
        _this.reDrawPie(d, originalDataset);
    };

    var arc = d3.svg.arc().innerRadius(innerRadius)
        .outerRadius(outerRadius);
    //Set up groups
    _this.arcIndex = _this.arcIndex + 1;
    var clazz = "arc" + _this.arcIndex;

    var storeMetadataWithArc = function (d) {
        d.path = _this;
        d.fill = _this.fill;
        d.arc = arc;
        d.length = dataset.length;
    };

    var arcs = svg.selectAll("g." + clazz)
        .data(pie(dataset))
        .enter()
        .append("g")
        .attr("class", "arc " + clazz)
        .attr("transform",
        "translate(" + (totalRadius) + "," + (totalRadius) + ")")
        .on("dblclick", dblclick)
        .on("click", dblclick);

    var gradient = svg.append("svg:defs")
        .append("svg:linearGradient")
        .attr("id", "gradient_" + _this.arcIndex)
        .attr("x1", "0%")
        .attr("y1", "0%")
        .attr("x2", "100%")
        .attr("y2", "100%")
        .attr("spreadMethod", "pad");

    var values = [];
    var fill_color = {};
    for (var i = 0; i < dataset.length; i++) {
        fill_color['color'] = dataset[i].fill_color;
    }
    var startColor, endColor;
    if (!isEmpty(fill_color)) {
        startColor = endColor = fill_color['color'];
    } else if (_this.config.gradient) {
        var index = 2 * _this.arcIndex;
        var endIndex = index + 1;
        startColor = _this.config.colors(index);
        endColor = _this.config.colors(endIndex);
    } else {
        startColor = endColor = _this.config.colors(_this.arcIndex);
    }

    gradient.append("svg:stop")
        .attr("offset", "0%")
        .attr("stop-color", startColor)
        .attr("stop-opacity", 1);

    gradient.append("svg:stop")
        .attr("offset", "100%")
        .attr("stop-color", endColor)
        .attr("stop-opacity", 1);

    //Draw arc paths
    var paths = arcs.append("path")
        .attr("fill", "url(#gradient_" + _this.arcIndex + ")")
        .style("stroke", _this.config.stroke)
        .style("stroke-width", _this.config.strokeWidth);
    for (var i = 0; i <= paths[0].length; i++) {
        if (dataset[i] != undefined) {
            d3.select(paths[0][i]).style("fill", dataset[i].fill_color)
        }
    }

    paths.on("mouseover", _this.mouseover);

    paths.on("mouseout", _this.mouseout);

    paths.each(storeMetadataWithArc);

    paths.transition()
        .duration(_this.config.transitionDuration)
        .delay(_this.config.transitionDuration * (_this.arcIndex - 1))
        .ease(_this.config.transition)
        .attrTween("d", _this.customArcTween);

    //Labels
    var texts = arcs.append("text")
        .attr("x", function () {
            return parentCentroid[0];
        })
        .attr("y", function () {
            return parentCentroid[1];
        })
        .transition()
        .ease(_this.config.transition)
        .duration(_this.config.transitionDuration)
        .delay(_this.config.transitionDuration * (_this.arcIndex - 1))
        .attr("transform", function (d) {
            var a = [];
            a[0] = arc.centroid(d)[0] - parentCentroid[0];
            a[1] = arc.centroid(d)[1] - parentCentroid[1];
            return "translate(" + a + ")";
        })
        .attr("text-anchor", "middle")
        .text(_this.textText)
        .style("fill", _this.config.labelColor)
        .attr("title", _this.textTitle);

    for (var j = 0; j < dataset.length; j++) {
        if (dataset[j][_this.config.inner] !== undefined) {
            draw(svg, totalRadius, dataset[j][_this.config.inner], originalDataset, originalDatasetLength, innerRadius + radiusDelta, outerRadius + radiusDelta, radiusDelta, paths.data()[j].startAngle, paths.data()[j].endAngle, arc.centroid(paths.data()[j]));
        }
    }
}

_this.reDrawPie = function (d, ds) {
    var tmp = [];
    d3.select("#" + _this.tooltipId).remove();
    d3.select("#" + _this.config.containerId + "_svg") //.remove();
        .transition()
        .ease(_this.config.drilldownTransition)
        .duration(_this.config.drilldownTransitionDuration)
        .style("height", 0)
        .remove()
        .each("end", function () {
            if (d.length == 1 && _this.zoomStack.length != 0) {
                tmp = _this.zoomStack.pop();
            } else if (_this.zoomStack.length == 0) {
                tmp.push(d.data);
                _this.zoomStack.push(ds);
            } else {
                tmp.push(d.data);
                _this.zoomStack.push(ds);
            }
            _this.drawPie(tmp);
        });
};
