

<script async src="https://www.googletagmanager.com/gtag/js?id=G-KBLRSKKZSG"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-KBLRSKKZSG');
</script>
        <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1" />
        <link rel="stylesheet" href="https://chartsonlygoup.com/static/bootstrap/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://chartsonlygoup.com/static/bootstrap/css/styles.min.css">
        <link rel="stylesheet" href="https://chartsonlygoup.com/static/css/primary.min.css">
        <meta http-equiv="x-dns-prefetch-control" content="on">
        <link rel="shortcut icon" href="https://chartsonlygoup.com/static/favicon.ico">
        <link rel='preconnect' href='//stackpath.bootstrapcdn.com' crossorigin>
        <link rel="preconnect" href="//ajax.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com/" crossorigin>
        <link rel="dns-prefetch" href="https://fonts.gstatic.com/">
        <link rel="preconnect" href="https://use.fontawesome.com" crossorigin>
        <link rel="dns-prefetch" href="https://use.fontawesome.com">
        <link rel="preconnect" href="//cdnjs.cloudflare.com">
        <link rel="preconnect" href="//www.googletagmanager.com">
        <link rel="preconnect" href="//www.google-analytics.com">
        <link rel="preconnect" href="//cdn.datatables.net">
        <link rel="dns-prefetch" href="//cdn.datatables.net">
        <link rel="dns-prefetch" href="//s3.amazonaws.com">
        <link rel="dns-prefetch" href="//ajax.googleapis.com">
        <link rel="dns-prefetch" href="//cdnjs.cloudflare.com">
        <link rel="dns-prefetch" href="//www.googletagmanager.com">
        <link rel="dns-prefetch" href="//www.google-analytics.com">
        <link rel="dns-prefetch" href="//fonts.googleapis.com">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Nunito+Sans">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto+Condensed">
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
        <script src="https://chartsonlygoup.com/static/js/chart.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"
            integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous">
        </script>
        <script type="text/javascript" src="https://code.jquery.com/jquery-3.5.1.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js"
            integrity="sha384-ho+j7jyWK8fNQe+A12Hb8AhRq26LrZ/JpcUGGOn+Y7RsweNrtN/tE3MoK7ZeZDyx" crossorigin="anonymous">
        </script>
        <script>
            document.addEventListener('DOMContentLoaded', function (data) {
                var groupings = ['sum', 'average', 'sum']; // NOTE: FSDF
                Highcharts.dateFormats = {
                    q: function (timestamp) {
                        var date = new Date(timestamp),
                            quarter = (Math.floor(date.getUTCMonth() / 3) + 1);
                        // console.log(quarter);
                        return quarter;
                    }
                };
                var myChart = Highcharts.stockChart('highbar', {
                    // SECTION - Highcharts - top
                    chart: {
                        zoomType: 'x'
                    },
                    legend: {
                        enabled: true,
                        // verticalAlign: 'top',
                        backgroundColor: '#FFFFFF',
                        borderColor: '#E9E9E9',
                        borderWidth: 2,
                    },
                    // animation: false,
                    navigator: {
                        // enabled: false
                    },
                    tooltip: {
                        shared: true,
                        crosshairs: true
                    },
                    mapNavigation: {
                        enabled: true,
                        enableButtons: true, //false
                    },
                    responsive: {
                        rules: [{
                            condition: {
                                maxWidth: 500
                            },
                            // width: '1000',
                            chartOptions: {
                                chart: {},
                                subtitle: {
                                    // text: null
                                },
                                navigator: {
                                    // enabled: false
                                },
                                rangeSelector: {
                                    inputEnabled: false
                                },
                                plotOptions: {
                                    line: {
                                        dataLabels: {
                                            // opposite: true,
                                            // enabled:false,
                                            // format: "FY {point.x:%y}",
                                        }
                                    },
                                    spline: {
                                        // visible:false,
                                        labels: {
                                            // enabled: false,
                                            // visible:false,
                                        }
                                    }
                                },
                                legend: {
                                    enabled: true,
                                    verticalAlign: 'top',
                                },
                                mapNavigation: {
                                    enabled: false,
                                    enableButtons: false, //false
                                },
                                yAxis: [{
                                        yAxis: 2,
                                        opposite: false,
                                        labels: {
                                            // enabled: false,
                                        },
                                    },
                                    {
                                        yAxis: 1,
                                        opposite: false,
                                        labels: {
                                            enabled: false,
                                        },
                                    },
                                    {
                                        yAxis: 1,
                                        opposite: true,
                                        labels: {
                                            // enabled: false,
                                        },
                                    },
                                    {
                                        yAxis: 0,
                                        enabled: false,
                                        // opposite: true,
                                        labels: {
                                            enabled: false,
                                        },
                                    },
                                ],
                                xAxis: {
                                    labels: {
                                        // enabled: false,
                                    },
                                    scrollbar: {
                                        enabled: false
                                    },
                                },
                            }
                        }]
                    },
                    chart: {
                        // margin: [0, 70, 0, 70],
                        alignTicks: true,
                        credits: {
                            enabled: false
                        },
                        style: {
                            fontFamily: "'Nunito Sans', Verdana, Arial, Helvetica, sans-serif",
                            textOutline: false,
                            fontSize: "14px"
                        },
                        // borderWidth: 2,
                        // marginRight: 100,
                        // marginLeft: 100,
                        marginTop: 10,
                        renderTo: 'highbar',
                        events: {
                            render() {
                                var ticks = this.xAxis[0].ticks,
                                    ticksPositions = this.xAxis[0].tickPositions,
                                    tick0x,
                                    tick1x,
                                    getPosition = function (tick) {
                                        var axis = tick.axis;
                                        return Highcharts.Tick.prototype.getPosition.call(tick, axis
                                            .horiz, tick.pos, axis.tickmarkOffset);
                                    };
                                tick0x = getPosition(ticks[ticksPositions[0]]).x;
                                tick1x = getPosition(ticks[ticksPositions[1]]).x;
                                this.xAxis[0].labelGroup.translate((tick1x - tick0x) / 2)
                            }
                        },
                        zoomType: 'x',
                        // resetZoomButton: {
                        //     position: {
                        //         // align: 'right', // by default
                        //         // verticalAlign: 'top', // by default
                        //         x: 0,
                        //         y: -30
                        //     }
                        // }
                    },
                    title: {
                        // text: 'AAPL Stock Price & Net Revenue (Sales)',
                        // borderRadius: 5,
                        // backgroundColor: 'rgba(252, 255, 197, 0.7)',
                        // borderWidth: 1,
                        // borderColor: '#AAA',
                        // useHTML: true,
                        style: {
                            color: '#000000',
                            backgroundColor: '#FFFFFF',
                            fontWeight: 'bold',
                            // font: 'bold 10pt "Arial Narrow"',
                            // wordWrap:'break-word',
                            // width : "100px"
                        },
                        // verticalAlign: 'bottom',
                    },
                    rangeSelector: { // SECTION - Highcharts - range selector
                        selected: 3,
                        inputBoxWidth: 100,
                        // verticalAlign: 'bottom',
                        inputDateFormat: '  %Y-%m-%d',
                        inputEditDateFormat: '%Y-%m-%d',
                        inputPosition: {
                            // align: 'center',
                            // x: 10,
                            // y: 0,
                        },
                        buttonPosition: { // align: 'right',
                            x: 0,
                            y: 0
                        },
                        buttons: [{
                            type: 'year',
                            count: 3,
                            text: '3Y',
                            dataGrouping: {
                                enable: true
                            }
                        }, {
                            type: 'year',
                            count: 5,
                            text: '5Y',
                            dataGrouping: {
                                enable: true
                            }
                        }, {
                            type: 'year',
                            count: 10,
                            text: '10y',
                            dataGrouping: {
                                enable: false
                            }
                        }, {
                            type: 'all',
                            text: 'All',
                            dataGrouping: {
                                enable: false,
                                approximation: groupings[4]
                            }
                        }]
                    },
                    xAxis: [{
                        // opposite: true,
                        // SECTION - Highcharts - xAxis = top
                        // top:100,
                        startOnTick: true,
                        endOnTick: true,
                        // events: {
                        //     afterSetExtremes: function () {
                        //         this.displayBtn ? $('.highcharts-scrollbar').show() : $('.highcharts-scrollbar').hide()
                        //     },
                        // },
                        scrollbar: {
                            enabled: false
                        },
                        // zoomType: 'x',
                        // events: {
                        //     afterSetExtremes: function () {
                        //         this.displayBtn ? $('.highcharts-scrollbar').show() : $('.highcharts-scrollbar').hide()
                        //     },
                        //     load: function () {
                        //         $('.highcharts-scrollbar').hide()
                        //     }
                        // },
                        labels: {
                            style: {
                                color: '#black', // 'red'
                                fontSize: '14px'
                            }
                        },
                        // visible: false,
                        crosshair: {
                            width: 2,
                            color: '#1C9179',
                            snap: false,
                            className: "x_crosshair",
                            zIndex: 100
                        },
                        type: 'datetime',
                        dateTimeLabelFormats: {
                            month: 'Q%q %Y', //'%Y', // 'Q%q - %y',
                            year: '%Y'
                        },
                        // alternateGridColor: '#FDFFD5', // '#FEF8E3'
                        minPadding: 0,
                    }, {
                        labels: {
                            style: {
                                color: 'black', // 'red'
                                fontSize: '14px',
                                fontWeight: 'bold'
                            }
                        },
                        crosshair: {
                            width: 2,
                            color: '#1C9179',
                            snap: false,
                            className: "x_crosshair",
                            zIndex: 100
                        },
                        type: 'datetime',
                        dateTimeLabelFormats: {},
                        format: '{value:%Y}',
                        minPadding: 0
                    }, ],
                    plotOptions: {
                        // series: {
                        //     dataLabels:{
                        //         // overflow: "allow",
                        //         // crop: "false",
                        //     }
                        // },
                        // !!!!!!
                        line: { // SECTION - Highcharts - plotOptions - line
                            allowPointSelect: true,
                            connectNulls: true,
                            dataLabels: {
                                // overflow: "allow",
                                // crop: "false",
                                enabled: true,
                                // format: "FY {point.x:%Y}", // "{point.x:%b %e}",
                                borderRadius: 5,
                                formatter: function () {
                                    var point1 = this.series.data[this.series.data.length - 1];
                                    if (((Highcharts.dateFormat('%y', this.x)) % 4 == 0) && (this
                                            .point != point1)) {
                                        return '<span style="color:black; opacity:1;">FY ' +
                                            Highcharts.dateFormat('%Y', this.x) + '</span>';
                                    } else if ((Highcharts.dateFormat('%y', this.x)) % 4 != 0) {
                                        return '';
                                    } //'%b/%e/%Y'
                                    else if (this.point == point1) {
                                        var latest_stock_price = this.y;
                                        // return Highcharts.dateFormat('%Y', this.x);}
                                        // return '';}
                                        return '<span style="color:black; opacity:1;">FY ' +
                                            Highcharts.dateFormat('%Y', this.x) + '</span>';
                                    }
                                },
                                backgroundColor: "#FFFFFF", //'rgba(252, 255, 197, 0.7)',
                                // backgroundColor: 'rgba(252, 255, 197, 0.7)',
                                borderWidth: 1,
                                borderColor: '#AAA',
                                // x:10,
                                // y: 50,
                                opacity: 1,
                            },
                            pointPlacement: 'on'
                        },
                        spline: { // SECTION - Highcharts - plotOptions - area
                        },
                        // column: { // SECTION - Highcharts - plotOptions- column
                        //     groupPadding: 0.1,
                        //     color: '#D6D9BF',
                        // },
                        series: {
                            name: 'Quarterly Data',
                            groupPadding: 0,
                            dataGrouping: {
                                enabled: false
                            },
                            type: 'line',
                            xAxis: 0,
                            visible: false,
                            labels: {
                                visible: false,
                            }
                        },
                        series: {
                            type: 'area',
                            // type: 'column',
                            marker: {
                                radius: 4,
                                // fillColor: '#1ebd1e',
                                enabled: true,
                                zIndex: 100
                            },
                            xAxis: 0,
                            name: "Full-Year (FY)   Net Revenue (Sales)",
                            dataGrouping: {
                                enabled: false
                            },
                            states: {
                                inactive: {
                                    opacity: 1
                                }
                            }
                        }
                    },
                    yAxis: [ // SECTION - Highcharts - yAxis
                        {
                            yAxis: 1,
                            maxPadding: 0.1,
                            crosshair: {
                                width: 2,
                                color: '#1C9179',
                                snap: false,
                                className: "y_crosshair",
                                zIndex: 100
                            },
                            // tickAmount: 6,
                            opposite: false,
                            gridLineColor: 'transparent',
                            // height:'90%',
                            // tickPixelInterval: 70,
                            tickPositioner: function () {
                                var positions = [],
                                    tick = this.dataMin, // Math.floor(this.dataMin),
                                    // https://stackoverflow.com/questions/31925204/highcharts-line-charts-out-of-memory
                                    // increment = Math.ceil((this.dataMax - this.dataMin) / 6);
                                    increment = Math.max(1, Math.ceil((this.dataMax - this
                                        .dataMin) / 6));
                                for (; tick - increment <= this.dataMax; tick += increment) {
                                    positions.push(tick);
                                }
                                return positions;
                            },
                            labels: {
                                style: {
                                    color: '#4285F4', // '#3D7198', // '#4285F4', // 'red'
                                    fontSize: '14px',
                                    // fontWeight: 'bold',
                                },
                                overflow: 'justify',
                                formatter: function () {
                                    zoom_values_stock_price = $(this.axis.tickPositions)
                                    price_percent = Math.round(100 * this.value /
                                        zoom_values_stock_price[0]) - 100
                                    price_percent = price_percent.toString().replace(
                                        /\B(?=(\d{3})+(?!\d))/g, ",")
                                    return '<span style="">' + '<b>$' + Math.round(this.value *
                                            100) / 100 + '</b><br>' + price_percent + '' + '%' +
                                        '</span>'; // zoom_values[0];//
                                },
                                align: 'right'
                            },
                            // tickPixelInterval: 70,
                        },
                        {
                            yAxis: 2,
                            opposite: false,
                            visible: false,
                            labels: {
                                enabled: false,
                            }
                        },
                        { // SECTION - Highcharts - yAxis - metric - percent
                            opposite: true,
                            yAxis: 1,
                            title: 'metric',
                            tickPositioner: function () {
                                the_minimum = this.dataMin
                                var positions = [],
                                    tick = Math.floor(this.dataMin * 100),
                                    // increment = Math.ceil((this.dataMax*100 - this.dataMin*100) / 6);
                                    increment = Math.max(1, Math.ceil((this.dataMax * 100 - this
                                        .dataMin * 100) / 6));
                                for (; tick - increment <= this.dataMax * 100; tick +=
                                    increment) {
                                    positions.push(tick / 100);
                                }
                                return positions;
                            },
                            labels: { // SECTION - Highcharts - yAxis - labels
                                style: {
                                    color: "#19a419", // '#177737', // 'red'
                                    fontSize: '14px'
                                },
                                overflow: 'justify',
                                // x: 50,
                                align: 'left',
                                formatter: function () {
                                    zoom_values_fy_metric = $(this.axis.tickPositions)
                                    var old = this.axis.defaultLabelFormatter.call(this)
                                    if (zoom_values_fy_metric[0] != 0) {
                                        metric_percent = (Math.round(100 * this.value /
                                            zoom_values_fy_metric[0])) - 100;
                                        metric_percent = metric_percent.toString().replace(
                                                /\B(?=(\d{3})+(?!\d))/g, ",").replace("-", "")
                                            .replace("NaN", "") + '%'
                                    } else if (zoom_values_fy_metric[0] == 0) {
                                        metric_percent = ""
                                    }
                                    // metric_percent = zoom_values_fy_metric[0]
                                    if (this.value >= 1000000000 || this.value <= -1000000000) {
                                        billion_rounded = Math.round((this.value / 1000000000) *
                                            1) / 1;
                                        return ('<b>  $' + billion_rounded + 'B</b>' + '<br>' +
                                            metric_percent);
                                    } else if (this.value >= 1000000 || this.value <= -
                                        1000000) {
                                        million_rounded = Math.round((this.value / 1000000) *
                                            1) / 1;
                                        return ('<b>  $' + million_rounded) + 'M</b>' + '<br>' +
                                            metric_percent;
                                    } else if (this.value >= 1000 || this.value <= -1000) {
                                        thousand_rounded = Math.round((this.value / 1000) * 1) /
                                            1;
                                        return ('<b>  $' + this.value / 1000) + 'K</b>' +
                                            '<br>' + metric_percent;
                                    }
                                    // else if (this.value <= 10000 &&  this.value => -10000) {
                                    //     million_rounded = Math.round((this.value / 1) * 100) / 100;
                                    //     return('<b>' + million_rounded) + '</b>' + '<br>' + metric_percent + '%';
                                    // }
                                    else { // return '<b>$' + this.y + '</b>';
                                        million_rounded = Math.round((this.value / 1) * 100) /
                                            100;
                                        return ('<b>' + million_rounded) + '</b>' + '<br>' +
                                            metric_percent;
                                    }
                                }
                            },
                            // tickPixelInterval: 70,
                        },
                    ],
                    // SECTION - Highcharts - yAxis - tooltip (formatter)
                    series: [{
                            type: 'spline',
                            name: 'Stock Price',
                            color: '#4285F4', // '#3D7198', //#4285F4', // robinhood green
                            // pointInterval: 1,
                            // pointIntervalUnit: 'year',
                            tooltip: {
                                // TODO make the datapoint markers better
                                backgroundColor: '#FFFFFF', // '#1ebd1e', // 'red'
                                opacity: .7,
                                style: {
                                    color: '#000000',
                                    fontSize: '14px',
                                    fontWeight: 'bold'
                                },
                                enabled: true,
                                shared: true,
                                valuePrefix: "$",
                                pointFormatter: function () {
                                    // https://stackoverflow.com/questions/25973920/how-to-display-highchart-series-line-marker-symbol-from-tooltip-formatter
                                    // ●♦■▲▼
                                    stock_price = Math.round((this.y) * 100) / 100;
                                    return '♦ ' + this.series.name + ' <b>  $' + stock_price +
                                        '</b>';
                                }
                            },
                            data: price_json,
                            zIndex: 98,
                            yAxis: 0,
                        },
                        {
                            // SECTION - Highcharts - series - all
                            type: 'area', // type: 'column',
                            lineWidth: 0,
                            color: 'transparent',
                            borderColor: 'transparent',
                            showInLegend: false,
                            // fillOpacity: .1,
                            // color: "#19a419", //"#177737",
                            // marker: {
                            //     // symbol: 'triangle',
                            //     radius: 1,
                            //     states: {
                            //         hover: {
                            //             enabled: true,
                            //             lineColor: 'rgb(100,100,100)'
                            //         }
                            //     }
                            // },
                            name: 'Quarterly (Q)   Net Revenue (Sales)',
                            // pointInterval: 1,
                            // pointIntervalUnit: 'year',
                            tooltip: {
                                // split: true,
                                shared: true,
                                xDateFormat: 'Q%q %Y',
                                shadow: true,
                                borderWidth: 1,
                                borderColor: '#AAA',
                                backgroundColor: '#FFFFFF', // '#1ebd1e', // 'red'
                                opacity: .7,
                                style: {
                                    color: '#000000',
                                    fontSize: '14px',
                                    fontWeight: 'bold'
                                },
                                enabled: true,
                                // shared: false,
                                valuePrefix: "$",
                                pointFormatter: function () {
                                    // ●♦■▲▼
                                    // this.series.name
                                    tooltip_legend = Highcharts.dateFormat('Q%q %Y', this.x) +
                                        ' '; // '● '+ this.series.name
                                    if (this.y >= 1000000000 || this.y <= -1000000000) {
                                        billion = this.y / 1000000000;
                                        billion_rounded = Math.round((billion) * 10) / 10;
                                        return (tooltip_legend + '<b>  $' + billion_rounded) +
                                            'B</b>';
                                    } else if (this.y >= 1000000 || this.y <= -1000000) {
                                        million = this.y / 1000000
                                        million_rounded = Math.round((million) * 10) / 10;
                                        return (tooltip_legend + '<b>  $' + million_rounded) +
                                            'M</b>';
                                    } else if (this.y >= 10000 || this.y <= -10000) {
                                        thousand = this.y / 1000
                                        thousand_rounded = Math.round((thousand) * 10) / 10;
                                        return (tooltip_legend + '<b>  $' + this.y / 1000) +
                                            'K</b>';
                                    } else { // return '<b>$' + this.y + '</b>';
                                        ratio = this.y / 1
                                        million_rounded = Math.round((ratio) * 100) / 100;
                                        return (tooltip_legend + '<b>' + million_rounded) +
                                            '</b>';
                                    }
                                },
                                positioner: function (width, height, point) {
                                    var chart = this.chart,
                                        position;
                                    if (point.isHeader) {
                                        position = {
                                            x: Math.max(
                                                // Left side limit
                                                chart.plotLeft,
                                                Math.min(point.plotX + chart.plotLeft -
                                                    width / 2,
                                                    // Right side limit
                                                    chart.chartWidth - width - chart
                                                    .marginRight)
                                            ),
                                            y: point.plotY
                                        };
                                    } else {
                                        position = {
                                            x: point.series.chart.plotLeft,
                                            y: point.series.yAxis.top - chart.plotTop
                                        };
                                    }
                                    return position;
                                },
                                shape: 'square',
                                headerShape: 'callout',
                                borderWidth: 1,
                                borderColor: '#AAA',
                                shadow: false
                            },
                            data: df_json,
                            zIndex: 98,
                            yAxis: 1,
                            // xAxis: 0,
                        }, {
                            type: 'line',
                            yAxis: 2,
                            zIndex: 100,
                            tooltip: {
                                shared: true,
                                xDateFormat: 'FY %Y',
                                // '%b - %Y'
                                // backgroundColor: '#1ebd1e',
                                // tooltip_legend = '● '+ this.series.name
                                // tooltip_legend +
                                valuePrefix: "$",
                                pointFormatter: function () {
                                    // formatter: function () {
                                    // ●♦■▲▼
                                    // tooltip_legend = this.series.name + ' '; //'● '+ this.series.name
                                    tooltip_legend = Highcharts.dateFormat('FY %Y', this.x) +
                                        ' '; // '● '+ this.series.name
                                    if (this.y >= 1000000000 || this.y <= -1000000000) {
                                        billion = this.y / 1000000000;
                                        billion_rounded = Math.round((billion) * 10) / 10;
                                        return (tooltip_legend + '<b>  $' + billion_rounded) +
                                            'B</b>';
                                    } else if (this.y >= 1000000 || this.y <= -1000000) {
                                        million = this.y / 1000000
                                        million_rounded = Math.round((million) * 10) / 10;
                                        return (tooltip_legend + '<b>  $' + million_rounded) +
                                            'M</b>';
                                    } else if (this.y >= 10000 || this.y <= -10000) {
                                        thousand = this.y / 1000
                                        thousand_rounded = Math.round((thousand) * 10) / 10;
                                        return (tooltip_legend + '<b>  $' + this.y / 1000) +
                                            'K</b>';
                                    } else { // return '<b>$' + this.y + '</b>';
                                        ratio = this.y / 1
                                        million_rounded = Math.round((ratio) * 100) / 100;
                                        return (tooltip_legend + '<b>' + million_rounded) +
                                            '</b>';
                                    }
                                },
                            },
                            // pointInterval: 1,
                            // pointIntervalUnit: 'year',
                            color: "#19a419", //'#177737', // '#343A40', // '#1C9179',
                            lineWidth: 3,
                            xDateFormat: '%Y',
                            findNearestPointBy: 'xy',
                            data: year_df_json
                        },
                    ]
                });
                var screen_size = $(window).width();
                if (screen_size < 768)
                // var x = window.matchMedia("(max-width: 700px)")
                // if (x.matches)
                {
                    // document.getElementsByClassName("highbar_mobile")[0].style.marginLeft = (-.1*screen_size)+"px";
                    // myChart.setSize(screen_size*1.1);
                } else {
                    // alert('More than 960');
                    // myChart.setSize(200);
                }
            });
        </script>
<script src="https://chartsonlygoup.com/static/js/quarterly.js"></script>