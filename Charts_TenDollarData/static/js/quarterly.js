function mapData([x, y]) {
	return {
		name: x,
		x: x,
		y: Math.abs(y),
		actualY: y,
		color: y >= 0 ? "#7CB5EC" : "#E6496F",
		// '#20c08d': '#E6496F' //'#add6a6': '#E6496F' //'#19A419': '#E6496F'//
		// 7CB5EC, '#63CCA6' : '#E6496F'
	};
}

// function centerLabels(chart) {
// 	var $container = $(chart.target.highbar);
// 	var axes = chart.target.axes;
// 	var $labels = $highbar.find(".highcharts-axis-labels .timeline_label");
// 	var $thisLabel, $nextLabel, thisXPos, nextXPos, delta, newXPos;
// 	$labels.each(function () {
// 		$thisLabel = $(this).parent("span");
// 		thisXPos = parseInt($thisLabel.css("left"));
// 		$nextLabel = $thisLabel.next();
// 		nextXPos = $nextLabel.length
// 			? parseInt($nextLabel.css("left"))
// 			: axes[0].left + axes[0].width;
// 		delta = (nextXPos - thisXPos) / 2.0;
// 		newXPos = thisXPos + delta;
// 		if ($nextLabel.length || $(this).width() + newXPos < nextXPos) {
// 			$thisLabel.css("left", newXPos + "px");
// 		} else {
// 			$thisLabel.remove();
// 		}
// 	});
// }

// document.addEventListener('DOMContentLoaded', function (data) {
//     df_json = {{ df_json }};
//     year_df_json = {{ year_df_json }};
//     price_json = {{ price_json }};
//     function mapData([x, y]) {
//         return {
//             name: x,
//             x: x,
//             y: Math.abs(y),
//             actualY: y,
//             color: y >= 0 ? '#7CB5EC' : '#E6496F',
//             // '#20c08d': '#E6496F' //'#add6a6': '#E6496F' //'#19A419': '#E6496F'//
//             // 7CB5EC, '#63CCA6' : '#E6496F'
//         }
//     }
//     var groupings = ['sum', 'average', 'sum'];
//     Highcharts.dateFormats = {
//         q: function (timestamp) {
//             var date = new Date(timestamp),
//                 quarter = (Math.floor(date.getUTCMonth() / 3) + 1);
//             console.log(quarter);
//             return quarter;
//         }
//     };
//     (function (H) { // internal functions
//         function stopEvent(e) {
//             if (e) {
//                 if (e.preventDefault) {
//                     e.preventDefault();
//                 }
//                 if (e.stopPropagation) {
//                     e.stopPropagation();
//                 }
//                 e.cancelBubble = true;
//             }
//         }
//         // the wrap
//         H.wrap(H.Chart.prototype, 'render', function (proceed) {
//             var chart = this,
//                 mapNavigation = chart.options.mapNavigation;
//             proceed.call(chart);
//             // Add the mousewheel event
//             H.addEvent(chart.container, document.onmousewheel === undefined ? 'DOMMouseScroll' : 'mousewheel', function (event) {
//                 var delta,
//                     extr,
//                     step,
//                     newMin,
//                     newMax,
//                     axis = chart.xAxis[0];
//                 var dataMax = chart.xAxis[0].dataMax,
//                     dataMin = chart.xAxis[0].dataMin,
//                     stepDivisor = 5,
//                     newExtrMin,
//                     newExtrMax;
//                 e = chart.pointer.normalize(event);
//                 // Firefox uses e.detail, WebKit and IE uses wheelDelta
//                 delta = e.detail || -(e.wheelDelta / 120);
//                 delta = delta < 0 ? 1 : -1;
//                 if (chart.isInsidePlot(e.chartX - chart.plotLeft, e.chartY - chart.plotTop)) {
//                     extr = axis.getExtremes();
//                     step = (extr.max - extr.min) / stepDivisor * delta;
//                     if ((extr.min + step) <= dataMin) {
//                         newExtrMin = dataMin;
//                         newExtrMax = extr.max;
//                     } else if ((extr.max + step) >= dataMax) {
//                         newExtrMin = extr.min;
//                         newExtrMax = dataMax;
//                     } else {
//                         newExtrMin = extr.min + step;
//                         newExtrMax = extr.max + step;
//                     } axis.setExtremes(newExtrMin, newExtrMax, true, false);
//                 }
//                 stopEvent(event); // Issue #5011, returning false from non-jQuery event does not prevent default
//                 return false;
//             });
//         });
//     }(Highcharts));
//     var myChart = Highcharts.stockChart('highbar', {
//         // SECTION - Highcharts - top
//         legend: {
//             enabled: true,
//             // verticalAlign: 'top',
//             backgroundColor:'#FFFFFF',
//             borderColor:'#E9E9E9',
//             borderWidth:2,
//         },
//         // animation: false,
//         navigator: {
//             // enabled: false
//         },
//         tooltip: {
//             shared: true,
//             crosshairs: true
//         },
//         responsive: {
//             rules: [
//                 {
//                     condition: {
//                         maxWidth: 500
//                     },
//                     chartOptions: {
//                         chart: {},
//                         subtitle: {
//                             // text: null
//                         },
//                         navigator: {
//                             enabled: false
//                         },
//         plotOptions: { line:{
//             dataLabels:{
//                 // enabled:false,
//                 format: "FY {point.x:%y}",
//             }
//         }},
//         legend: {
//             enabled: true,
//             verticalAlign: 'bottom',
//         },
//                     }
//                 }
//             ]
//         },
//         chart: {
//             // margin: [0, 70, 0, 70],
//             alignTicks: true,
//             credits: {
//                 enabled: false
//             },
//             style: {
//                 fontFamily: "'Nunito Sans', Verdana, Arial, Helvetica, sans-serif",
//                 textOutline: false,
//                 fontSize: "14px"
//             },
//             // borderWidth: 2,
//             // marginRight: 100,
//             // marginLeft: 100,
//             marginTop: 10,
//             renderTo: 'highbar',
//             events: {
//                 render() {
//                     var ticks = this.xAxis[0].ticks,
//                         ticksPositions = this.xAxis[0].tickPositions,
//                         tick0x,
//                         tick1x,
//                         getPosition = function (tick) {
//                             var axis = tick.axis;
//                             return Highcharts.Tick.prototype.getPosition.call(tick, axis.horiz, tick.pos, axis.tickmarkOffset);
//                         };
//                     tick0x = getPosition(ticks[ticksPositions[0]]).x;
//                     tick1x = getPosition(ticks[ticksPositions[1]]).x;
//                     this.xAxis[0].labelGroup.translate((tick1x - tick0x) / 2)
//                 }
//             }
//         },
//         title: {
//             // text: '{{company_symbol}} Stock Price & {{ fin_metric_name }}',
//             // borderRadius: 5,
//             // backgroundColor: 'rgba(252, 255, 197, 0.7)',
//             // borderWidth: 1,
//             // borderColor: '#AAA',
//         useHTML: true,
//         style: {
//             color: '#000000',
//             'background-color': '#FFFFFF',
//             fontWeight: 'bold'
//         },
//             // verticalAlign: 'bottom',
//         },
//         rangeSelector: { // SECTION - Highcharts - range selector
//             selected: 2,
//             verticalAlign: 'bottom',
//             inputPosition: { align: 'center',
//                 x: 0,
//                 y: 0
//             },
//             buttonPosition: { // align: 'right',
//                 x: 0,
//                 y: 0
//             },
//             buttons: [
//                 {
//                     type: 'year',
//                     count: 3,
//                     text: '3Y',
//                     dataGrouping: {
//                         enable: true
//                     }
//                 }, {
//                     type: 'year',
//                     count: 5,
//                     text: '5Y',
//                     dataGrouping: {
//                         enable: true
//                     }
//                 }, {
//                     type: 'year',
//                     count: 10,
//                     text: '10y',
//                     dataGrouping: {
//                         enable: false
//                     }
//                 }, {
//                     type: 'all',
//                     text: 'All',
//                     dataGrouping: {
//                         enable: false,
//                         approximation: groupings[4]
//                     }
//                 }
//             ]
//         },
//         xAxis: [
//             {
//                 // SECTION - Highcharts - xAxis = top
//                 // height:1,
//                 events: {
//                     afterSetExtremes: function () {
//                         this.displayBtn ? $('.highcharts-scrollbar').show() : $('.highcharts-scrollbar').hide()
//                     },
//                 },
//                 scrollbar: {
//                     enabled: true
//                 },
//                 // zoomType: 'x',
//                 events: {
//                     load: function () {
//                         $('.highcharts-scrollbar').hide()
//                     }
//                 },
//                 labels: {
//                     style: {
//                         color: '#black', // 'red'
//                         fontSize: '14px'
//                     }
//                 },
//                 // visible: false,
//                 crosshair: {
//                     width: 2,
//                     color: '#1C9179',
//                     snap: false,
//                     className: "x_crosshair",
//                     zIndex: 100
//                 },
//                 type: 'datetime',
//                 dateTimeLabelFormats: {
//                     month: 'Q%q %Y', //'%Y', // 'Q%q - %y',
//                     year: '%Y'
//                 },
//                 // alternateGridColor: '#FDFFD5', // '#FEF8E3'
//                 minPadding: 0,
//                 // pointInterval: 1,//1000 * 3600 * 24 * 91.
//                 // labels: {
//                 //     enabled: false,
//                 //     // step: 1
//                 // }
//             }, {
//                 labels: {
//                     style: {
//                         color: 'black', // 'red'
//                         fontSize: '14px',
//                         fontWeight: 'bold'
//                     }
//                 },
//                 crosshair: {
//                     width: 2,
//                     color: '#1C9179',
//                     snap: false,
//                     className: "x_crosshair",
//                     zIndex: 100
//                 },
//                 type: 'datetime',
//                 dateTimeLabelFormats: {},
//                 format: '{value:%Y}',
//                 minPadding: 0
//             },
//         ],
//         plotOptions: {
//             // SECTION - Highcharts - plotOptions
//             // series: { // SECTION - Highcharts - plotOptions - series - all
//             //     connectNulls: true,
//             //     dataLabels: {
//             //         enabled: true,
//             //         formatter: function () { // if last point
//             //             if (this.point === this.series.data[this.series.data.length - 1]) {
//             //                 return this.series.name;
//             //             }
//             //         }
//             //     }
//             // },
//             line: { // SECTION - Highcharts - plotOptions - line
//                 allowPointSelect: true,
//                 connectNulls: true,
//                 dataLabels: {
//                     enabled: true,
//                     // format: "FY {point.x:%Y}", // "{point.x:%b %e}",
//                     borderRadius: 5,
//                     formatter: function() {
//                         var point1 = this.series.data[this.series.data.length - 1];
//                         if(((Highcharts.dateFormat('%y', this.x)) % 2 == 0) && (this.point != point1)) {
//                             return '<span style="color:black; opacity:1;">FY ' + Highcharts.dateFormat('%Y', this.x) +'</span>';
//                         }
//                         else if ((Highcharts.dateFormat('%y', this.x)) % 2 != 0){
//                         return '';} //'%b/%e/%Y'
//                         else if (this.point == point1){
//                             var latest_stock_price = this.y;
//                         // return Highcharts.dateFormat('%Y', this.x);}
//                         // return '';}
//                         return '<span style="color:black; opacity:1;">FY ' + Highcharts.dateFormat('%Y', this.x) +'</span>';}
//                         // return '<span style="color:black; opacity:1;">Last 12 Months' + '</span>' +'<br /><span style="color: #177737;font-size: 17px;">{{ last_4_quarters_str }}' + '</span><br>'+'Stock Price<br>';}
//                     },
//                     backgroundColor: "#FFFFFF", //'rgba(252, 255, 197, 0.7)',
//                     // backgroundColor: 'rgba(252, 255, 197, 0.7)',
//                     borderWidth: 1,
//                     borderColor: '#AAA',
//                     // x:10,
//                     // y: 50,
//                     opacity: 1,
//                 },
//                 pointPlacement: 'on'
//             },
//             spline: { // SECTION - Highcharts - plotOptions - area
//                 // dataLabels:{
//                 //                 className: 'chart_fy_metric',
//                 //                 fontWeight: 'bold',
//                 //                 padding: 5,
//                 //                 enabled: true, //false, //true,
//                 //                 // useHTML: true,
//                 //                 borderRadius: 5,
//                 //                 backgroundColor: '#FFFFFF',
//                 //                 opacity: .7,
//                 //                 zIndex:180,
//                 //                 crop: false,
//                 //                 overflow: 'visible',
//                 //                 y: -10,
//                 //                 x: -40,
//                 //                 formatter: function () {
//                 //                     // var point1 = this.series.data[this.series.data.length - 1];
//                 //                     var point1 = this.series.data[this.series.data.length - 5];
//                 //                     // return point1
//                 //                     if (this.point == point1) {
//                 //                         var latest_stock_price = this.y;
//                 //                         return "<div class=\"chart_current_metric\">Last 4 Qtrs<br/>"  + "{{currency_symbol}}" + this.y + 'B</div>'
//                 //                         };}
//                 // },
//             },
//             column: { // SECTION - Highcharts - plotOptions- column
//                 groupPadding: 0.1,
//                 color: '#D6D9BF',
//                 // dataLabels:{
//                 //     formatter: function () {
//                 //                     var dataMax = this.series.dataMax;
//                 //                     var dataMin = this.series.dataMin;
//                 //                     if (this.y === dataMax) {
//                 //                         return('<b>Top<br />' + max_min_num) + '</b>';
//                 //                         // return this.y;
//                 //                     }
//                 //                     if (this.y === dataMin) {
//                 //                         return('<b>Bottom<br />' + max_min_num) + '</b>';
//                 //                     }
//                 //                 }
//                 // },
//                 // dataLabels:{
//                 //                 className: 'chart_fy_metric',
//                 //                 fontWeight: 'bold',
//                 //                 padding: 5,
//                 //                 enabled: true,
//                 //                 // useHTML: true,
//                 //                 borderRadius: 5,
//                 //                 backgroundColor: '#FFFFFF',
//                 //                 opacity: .7,
//                 //                 zIndex:180,
//                 //                 crop: false,
//                 //                 overflow: 'visible',
//                 //                 y: -10,
//                 //                 x: 40,
//                 //                 formatter: function () {
//                 //                     var point1 = this.series.data[this.series.data.length - 1];
//                 //                     // return point1
//                 //                     if (this.point == point1) {
//                 //                         return "<div class=\"chart_current_metric\">Last 4 Qtrs<br/>"  + "{{currency_symbol}}" + this.y + 'B</div>'
//                 //                         };}
//                 // },
//             },
//             series: {
//                 name: 'Quarterly Data',
//                 groupPadding: 0,
//                 dataGrouping: {
//                     enabled: false
//                 },
//                 type: 'line',
//                 xAxis: 1,
//             },
//             series: {
//                 type: 'area',
//                 marker: {
//                     radius: 4,
//                     // fillColor: '#1ebd1e',
//                     enabled: true,
//                     zIndex: 100
//                 },
//                 xAxis: 0,
//                 name: "Full-Year (FY)   {{ fin_metric_name }}",
//                 dataGrouping: {
//                     enabled: false
//                 },
//                 states: {
//                     inactive: {
//                         opacity: 1
//                     }
//                 }
//             }
//         },
//         yAxis: [ // SECTION - Highcharts - yAxis
//             {
//                 // SECTION - Highcharts - yAxis - stock price - percent
//                 // min:1,
//                 // title: {
//                 //     // align: 'high',
//                 //     offset: 0,
//                 //     text:  "Stock Price",
//                 //     fontSize: '140000px',
//                 //     rotation: 0,
//                 //     y: -10,
//                 //     enabled: true,
//                 // style: {
//                 //     visibility: 'visible'},
//                 // },
//                 // showFirstLabel: false,
//                 // showLastLabel: false,
//                 yAxis: 1,
//                 maxPadding: 0.1,
//                 crosshair: {
//                     width: 2,
//                     color: '#1C9179',
//                     snap: false,
//                     className: "y_crosshair",
//                     zIndex: 100
//                 },
//                 // tickAmount: 6,
//                 opposite: false,
//                 gridLineColor: 'transparent',
//                 // height:'90%',
//                 // tickPixelInterval: 70,
//                 tickPositioner: function () {
//                     var positions = [],
//                         tick = this.dataMin, // Math.floor(this.dataMin),
//                         // https://stackoverflow.com/questions/31925204/highcharts-line-charts-out-of-memory
//                         // increment = Math.ceil((this.dataMax - this.dataMin) / 6);
//                         increment = Math.max(1,Math.ceil((this.dataMax - this.dataMin) / 6));
//                     for (; tick - increment <= this.dataMax; tick += increment) {
//                         positions.push(tick);
//                     }
//                     return positions;
//                 },
//                 // tickPositioner() {
//                 //     let tickPositions = this.tickPositions;
//                 //     tickPositions[0] = this.dataMin; // Math.round(this.dataMin);
//                 //     tickPositions[tickPositions.length - 1] = this.dataMax;
//                 //     return tickPositions;
//                 // },
//                 // top:10,
//                 labels: {
//                     style: {
//                         color: '#4285F4', // 'red'
//                         fontSize: '14px',
//                         // fontWeight: 'bold',
//                     },
//                     overflow: 'justify',
//                     formatter: function(){
//                         zoom_values_stock_price = $(this.axis.tickPositions)
//                         price_percent = Math.round(100 * this.value / zoom_values_stock_price[0])-100
//                         price_percent = price_percent.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
//                         return '<span style="">' + '<b>{{ currency_symbol }}' + Math.round(this.value*100)/100 +'</b><br>' + price_percent + '' + '%' + '</span>'; // zoom_values[0];//
//                     },
//                     align: 'right'
//                 },
//                 // tickPixelInterval: 70,
//             },
//             {// SECTION - Highcharts - yAxis - metric - percent
//                 opposite:true,
//                 yAxis: 1,
//                 title:'metric',
//                 // height: '80%',
//                 // min: 1,
//                 // tickPixelInterval: 70,
//                 // showFirstLabel: false,
//                 // showLastLabel: false,
//                 // tickInterval: 10,
//                 // tickAmount: 6,
//                 // maxPadding: 0.1,
//                 // gridLineColor: 'transparent',
//                 // top: 10,
//                 // offset: 0,
//                 {% if statement_or_ratio != "sratios" %}
//                 tickPositioner: function () {
//                     // var positions = [],
//                     //     tick = (this.dataMin),
//                     //     increment = ((this.dataMax - this.dataMin) / 6);
//                     // for (; tick - increment <= this.dataMax; tick += increment) {
//                     //     positions.push(tick);
//                     // }
//                     var positions = [],
//                         tick = Math.floor(this.dataMin*100),
//                         // increment = Math.ceil((this.dataMax*100 - this.dataMin*100) / 6);
//                         increment = Math.max(1,Math.ceil((this.dataMax*100 - this.dataMin*100) / 6));
//                     for (; tick - increment <= this.dataMax*100; tick += increment) {
//                         positions.push(tick/100);
//                     }
//                     return positions;
//                 },
//                 {% endif %}
//                 // {% if statement_or_ratio == "sratios" %}
//                 // tickPositioner() {
//                 //     let tickPositions = this.tickPositions;
//                 //     tickPositions[0] = this.dataMin; // Math.round(this.dataMin);
//                 //     tickPositions[tickPositions.length - 1] = this.dataMax;
//                 //     return tickPositions;
//                 // },
//                 // {% endif %}
//                 labels: { // SECTION - Highcharts - yAxis - labels
//                     style: {
//                         color: '#177737', // 'red'
//                         fontSize: '14px'
//                     },
//                     overflow: 'justify',
//                     // x: 50,
//                     align: 'left',
//                     formatter: function () {
//                         zoom_values_fy_metric = $(this.axis.tickPositions)
//                         metric_percent = (Math.round(100 * this.value / zoom_values_fy_metric[0]))-100;
//                         metric_percent = metric_percent.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
//                         if (this.value >= 1000000000) {
//                             billion_rounded = Math.round((this.value / 1000000000) * 1) / 1;
//                             return('<b>  {{ currency_symbol }}' + billion_rounded + 'B</b>' + '<br>' + metric_percent + '%');
//                         } else if (this.value >= 1000000) {
//                             million_rounded = Math.round((this.value / 1000000) * 1) / 1;
//                             return('<b>  {{ currency_symbol }}' + million_rounded) + 'M</b>' + '<br>' + metric_percent + '%';
//                         } else if (this.value >= 10000) {
//                             thousand_rounded = Math.round((this.value / 1000) * 1) / 1;
//                             return('<b>  {{ currency_symbol }}' + this.value / 1000) + 'K</b>' + '<br>' + metric_percent + '%';
//                         } else { // return '<b>$' + this.y + '</b>';
//                             million_rounded = Math.round((this.value / 1) * 100) / 100;
//                             return('<b>' + million_rounded) + '</b>' + '<br>' + metric_percent + '%';
//                         }
//                     }
//                 },
//                 // tickPixelInterval: 70,
//             },
//         ],
//         // SECTION - Highcharts - yAxis - tooltip (formatter)
//         series: [
//             {
//                 type: 'spline',
//                 name: 'Stock Price',
//                 color: '#4285F4', // robinhood green
//                 // pointInterval: 1,
//                 // pointIntervalUnit: 'year',
//                 tooltip: {
//                     // TODO make the datapoint markers better
//                     backgroundColor: '#FFFFFF', // '#1ebd1e', // 'red'
//                     opacity: .7,
//                     style: {
//                         color: '#000000',
//                         fontSize: '14px',
//                         fontWeight: 'bold'
//                     },
//                     enabled: true,
//                     shared: true,
//                     valuePrefix: "{{ currency_symbol }}",
//                     pointFormatter: function () {
//                         // https://stackoverflow.com/questions/25973920/how-to-display-highchart-series-line-marker-symbol-from-tooltip-formatter
//                         // ●♦■▲▼
//                         stock_price = Math.round((this.y) * 100) / 100;
//                         return '♦ ' + this.series.name + ' <b>  {{ currency_symbol }}' + stock_price + '</b>';
//                     }
//                 },
//                 data: price_json,
//                 zIndex: 98,
//                 yAxis: 0,
//             },
//             {
//                 // SECTION - Highcharts - series - all
//                 type: 'area',
//                 lineWidth: 0,
//                 fillOpacity: .1,
//                 // color: "#177737",
//                 marker: {
//                     // symbol: 'triangle',
//                     radius: 5,
//                     states: {
//                         hover: {
//                             enabled: true,
//                             lineColor: 'rgb(100,100,100)'
//                         }
//                     }
//                 },
//                 name: 'Quarterly (Q)   {{ fin_metric_name }}',
//                 pointInterval: 1,
//                 pointIntervalUnit: 'year',
//                 tooltip: {
//                     // split: true,
//                     shared: true,
//                     xDateFormat: 'Q%q %Y',
//                     shadow: true,
//                     borderWidth: 1,
//                     borderColor: '#AAA',
//                     backgroundColor: '#FFFFFF', // '#1ebd1e', // 'red'
//                     opacity: .7,
//                     style: {
//                         color: '#000000',
//                         fontSize: '14px',
//                         fontWeight: 'bold'
//                     },
//                     enabled: true,
//                     // shared: false,
//                     valuePrefix: "{{ currency_symbol }}",
//                     pointFormatter: function () {
//                         // ●♦■▲▼
//                         // this.series.name
//                         tooltip_legend = Highcharts.dateFormat('Q%q %Y', this.x) + ' '; // '● '+ this.series.name
//                         if (this.y >= 1000000000) {
//                             billion = this.y / 1000000000;
//                             billion_rounded = Math.round((billion) * 10) / 10;
//                             return(tooltip_legend + '<b>  {{ currency_symbol }}' + billion_rounded) + 'B</b>';
//                         } else if (this.y >= 1000000) {
//                             million = this.y / 1000000
//                             million_rounded = Math.round((million) * 10) / 10;
//                             return(tooltip_legend + '<b>  {{ currency_symbol }}' + million_rounded) + 'M</b>';
//                         } else if (this.y >= 10000) {
//                             thousand = this.y / 1000
//                             thousand_rounded = Math.round((thousand) * 10) / 10;
//                             return(tooltip_legend + '<b>  {{ currency_symbol }}' + this.y / 1000) + 'K</b>';
//                         } else { // return '<b>$' + this.y + '</b>';
//                             ratio = this.y / 1
//                             million_rounded = Math.round((ratio) * 100) / 100;
//                             return(tooltip_legend + '<b>' + million_rounded) + '</b>';
//                         }
//                     },
//                     positioner: function (width, height, point) {
//                         var chart = this.chart,
//                             position;
//                         if (point.isHeader) {
//                             position = {
//                                 x: Math.max(
//                                     // Left side limit
//                                     chart.plotLeft,
//                                     Math.min(point.plotX + chart.plotLeft - width / 2,
//                                     // Right side limit
//                                     chart.chartWidth - width - chart.marginRight)
//                                 ),
//                                 y: point.plotY
//                             };
//                         } else {
//                             position = {
//                                 x: point.series.chart.plotLeft,
//                                 y: point.series.yAxis.top - chart.plotTop
//                             };
//                         }
//                         return position;
//                     },
//                     shape: 'square',
//                     headerShape: 'callout',
//                     borderWidth: 1,
//                     borderColor: '#AAA',
//                     shadow: false
//                 },
//                 data: df_json,
//                 zIndex: 98,
//                 yAxis: 1
//             }, {
//                 type: 'line',
//                 yAxis: 1,
//                 zIndex: 100,
//                 tooltip: {
//                     shared: true,
//                     xDateFormat: 'FY %Y',
//                     // '%b - %Y'
//                     // backgroundColor: '#1ebd1e',
//                     // tooltip_legend = '● '+ this.series.name
//                     // tooltip_legend +
//                     valuePrefix: "{{ currency_symbol }}",
//                     pointFormatter: function () {
//                         // ●♦■▲▼
//                         // tooltip_legend = this.series.name + ' '; //'● '+ this.series.name
//                         tooltip_legend = Highcharts.dateFormat('FY %Y', this.x) + ' '; // '● '+ this.series.name
//                         if (this.y >= 1000000000) {
//                             billion = this.y / 1000000000;
//                             billion_rounded = Math.round((billion) * 10) / 10;
//                             return(tooltip_legend + '<b>  {{ currency_symbol }}' + billion_rounded) + 'B</b>';
//                         } else if (this.y >= 1000000) {
//                             million = this.y / 1000000
//                             million_rounded = Math.round((million) * 10) / 10;
//                             return(tooltip_legend + '<b>  {{ currency_symbol }}' + million_rounded) + 'M</b>';
//                         } else if (this.y >= 10000) {
//                             thousand = this.y / 1000
//                             thousand_rounded = Math.round((thousand) * 10) / 10;
//                             return(tooltip_legend + '<b>  {{ currency_symbol }}' + this.y / 1000) + 'K</b>';
//                         } else { // return '<b>$' + this.y + '</b>';
//                             ratio = this.y / 1
//                             million_rounded = Math.round((ratio) * 100) / 100;
//                             return(tooltip_legend + '<b>' + million_rounded) + '</b>';
//                         }
//                     }
//                 },
//                 pointInterval: 3,
//                 pointIntervalUnit: 'month',
//                 color: '#177737', // '#343A40', // '#1C9179',
//                 lineWidth: 3,
//                 xDateFormat: '%Y',
//                 findNearestPointBy: 'xy',
//                 data: year_df_json
//             },
//         ]
//     });
// });
