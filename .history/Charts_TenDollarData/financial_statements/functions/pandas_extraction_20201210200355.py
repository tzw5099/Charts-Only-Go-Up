<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <title>Home - Brand</title>
    <link rel="stylesheet" href="assets/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Catamaran:100,200,300,400,500,600,700,800,900">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato:100,100i,300,300i,400,400i,700,700i,900,900i">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=B612+Mono">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Fira+Code">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Fira+Mono">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Inconsolata">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Nunito+Sans">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Prompt">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto+Mono">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Source+Code+Pro">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.0/css/all.css">
    <link rel="stylesheet" href="assets/css/styles.min.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
</head>

<body>

  <script>
   document.addEventListener('DOMContentLoaded', function (data) {
    //     var myChart = Highcharts.setOptions({
    //     lang: {
    //         numericSymbols: [' thousands', ' millions', 'billions']
    //     }
    // });

        var myChart = Highcharts.stockChart('highbar', {
          // lang: {
          //     numericSymbols: [' thousands', ' millions', 'billions']
          // },
          chart: {
              borderWidth: 2,
              marginRight: 100
          },

                title: {
                    text: 'AAPL Stock Volume'
                },
                rangeSelector: {
                    inputPosition: {                    // align: 'left',
                        x: 0,                    y: 0                },
                    buttonPosition: {                    // align: 'right',
                        x: 0,                    y: 0                }
                    ,
                    buttons: [
            {
            type: 'year',        count: 3,        text: '3Y'    }, {
            type: 'year',        count: 5,        text: '5Y'    }, {
            type: 'year',        count: 10,        text: '10y'  }, {
            type: 'all',        text: 'All'    }                   ]
                },
                xAxis:{
                    tickInterval: 1 * 24 * 3600 * 1000 // interval of 1 day
                },
                yAxis:{
                  minPadding:100,
                          // lineColor:'#999',
                          // lineWidth:1,
                          // tickColor:'#666',
                          // tickWidth:1,
                          // tickLength:3,
                          // gridLineColor:'#ddd',
                          // title:{
                          //     text:'Y Axis Title',
                          //     rotation:0,
                          //     margin:50,
                          // },
                          tooltip: {
                          formatter: function (tooltip) {
                          }
                      },
        labels:{
                        align: 'right',
                  x: 50,
                  y: 0,
                          // formatter:function(){
                          //     return ('$' + this.value / 1000000000) + 'B';
                          // }
                          formatter:function(){
                      if(this.value >= 1000000000){
                          return ('$' + this.value / 1000000000) + 'B';
                      }
                      else if(this.value >= 1000000) {
                          return ('$' + this.value / 1000000) + 'M';
                      }
                      else if(this.value >= 1000) {
                          return ('$' + this.value / 1000) + 'K';
                      }
                      else {
                          return '$' + this.value;
                      }
                  }
        }
    },


                series: [{
                    type: 'column',
                    name: 'AAPL Stock Volume',
                    data:{{df_json}},

                }]

            });
        });
  </script>









<div id="highbar" style="height: 400px; width:1000px;"></div>

    <nav class="navbar navbar-light navbar-expand-md navigation-clean-search" style="color: #212529;">
        <div class="container">
            <div class="squarelogo"><a class="navbar-brand dollar_data" href="#" style="color: #fec503;">10</a></div><button data-toggle="collapse" class="navbar-toggler" data-target="#navcol-1"><span class="sr-only">Toggle navigation</span><span class="navbar-toggler-icon"></span></button>
            <div
                class="collapse navbar-collapse" id="navcol-1">
                <ul class="nav navbar-nav">
                    <li class="nav-item" role="presentation"><a class="nav-link active" href="#">First Item</a></li>
                    <li class="nav-item" role="presentation"><a class="nav-link" href="#">Second Item</a></li>
                    <li class="nav-item" role="presentation"><a class="nav-link" href="#">Third Item</a></li>
                </ul>
                <ul class="nav navbar-nav">
                    <li class="nav-item" role="presentation">
                        <form class="form-inline mr-auto" target="_self">
                            <div class="form-group">
                                <form class="form-inline d-none d-sm-inline-block mr-auto ml-md-3 my-2 my-md-0 mw-100 navbar-search">
                                    <div class="input-group"><input class="bg-light form-control border-0 small" type="text" placeholder="Search for ...">
                                        <div class="input-group-append"><button class="btn btn-primary py-0" type="button"><i class="fas fa-search"></i></button></div>
                                    </div>
                                </form>
                            </div>
                        </form>
                    </li>
                </ul>
                <ul class="nav navbar-nav mx-auto">
                    <li class="nav-item" role="presentation"><a class="nav-link active" href="#">Link 1</a></li>
                    <li class="nav-item" role="presentation"><a class="nav-link" href="#">Link 2</a></li>
                    <li class="nav-item" role="presentation"><a class="nav-link" href="#">Link 3</a></li>
                    <li class="nav-item dropdown"><a class="dropdown-toggle nav-link" data-toggle="dropdown" aria-expanded="false" href="#">Dropdown </a>
                        <div class="dropdown-menu" role="menu"><a class="dropdown-item" role="presentation" href="#">First Item</a><a class="dropdown-item" role="presentation" href="#">Second Item</a><a class="dropdown-item" role="presentation" href="#">Third Item</a></div>
                    </li>
                </ul>
        </div>
        </div>
    </nav>
    <div class="d-flex flex-column" id="content-wrapper">
        <div class="row">
            <div class="col-md-8 col-lg-8 col-xl-8">
                <div class="text-dark h1_info">
                    <div class="card shadow mb-4">
                        <div class="col mr-2">
                            <div class="text-uppercase text-info font-weight-bold text-xs mb-1"><span><strong>Current Ratio Definition and formula.</strong></span></div>
                            <p>See:&nbsp;<br>Macrotrends &amp; Gurufocus definitions https://www.gurufocus.com/term/mktcap/AAPL/Market-Cap/Apple<br></p>
                            <div class="row no-gutters align-items-center">
                                <div class="col-auto">
                                    <div class="text-dark font-weight-bold h5 mb-0 mr-3"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <h1 class="text-primary mb-0 pad-10-top pad-10-bottom pad-10-left pad-10-right"><strong>Apple Inc. (AAPL) Current Ratio | 1984 - Present</strong><br></h1>
                    <h2 class="text-primary mb-0">Current Ratio: 0.98<br></h2>
                </div>
                <div class="pad-10-top pad-10-bottom pad-10-left pad-10-right">
                    <div>
                        <div class="chart-area"><canvas data-bs-chart="{&quot;type&quot;:&quot;line&quot;,&quot;data&quot;:{&quot;labels&quot;:[&quot;Jan&quot;,&quot;Feb&quot;,&quot;Mar&quot;,&quot;Apr&quot;,&quot;May&quot;,&quot;Jun&quot;,&quot;Jul&quot;,&quot;Aug&quot;],&quot;datasets&quot;:[{&quot;label&quot;:&quot;Earnings&quot;,&quot;fill&quot;:true,&quot;data&quot;:[&quot;0&quot;,&quot;10000&quot;,&quot;5000&quot;,&quot;15000&quot;,&quot;10000&quot;,&quot;20000&quot;,&quot;15000&quot;,&quot;25000&quot;],&quot;backgroundColor&quot;:&quot;rgba(78, 115, 223, 0.05)&quot;,&quot;borderColor&quot;:&quot;rgba(78, 115, 223, 1)&quot;}]},&quot;options&quot;:{&quot;maintainAspectRatio&quot;:false,&quot;legend&quot;:{&quot;display&quot;:false},&quot;title&quot;:{},&quot;scales&quot;:{&quot;xAxes&quot;:[{&quot;gridLines&quot;:{&quot;color&quot;:&quot;rgb(234, 236, 244)&quot;,&quot;zeroLineColor&quot;:&quot;rgb(234, 236, 244)&quot;,&quot;drawBorder&quot;:false,&quot;drawTicks&quot;:false,&quot;borderDash&quot;:[&quot;2&quot;],&quot;zeroLineBorderDash&quot;:[&quot;2&quot;],&quot;drawOnChartArea&quot;:false},&quot;ticks&quot;:{&quot;fontColor&quot;:&quot;#858796&quot;,&quot;padding&quot;:20}}],&quot;yAxes&quot;:[{&quot;gridLines&quot;:{&quot;color&quot;:&quot;rgb(234, 236, 244)&quot;,&quot;zeroLineColor&quot;:&quot;rgb(234, 236, 244)&quot;,&quot;drawBorder&quot;:false,&quot;drawTicks&quot;:false,&quot;borderDash&quot;:[&quot;2&quot;],&quot;zeroLineBorderDash&quot;:[&quot;2&quot;]},&quot;ticks&quot;:{&quot;fontColor&quot;:&quot;#858796&quot;,&quot;padding&quot;:20}}]}}}"></canvas></div>
                        <h2
                            class="text-primary historical">AAPL Historical Current Ratio Chart (by Fiscal Year)</h2>
                    </div>
                    <div>
                        <h3>Current Ratio Summary</h3>
                        <p>Apple, Inc's current ratio is 0.7, and it's a great one. A current ratio of 0.7 places it ahead of it's industry (Computer Hardware) average of 0.5 and sector (Technology) average. The industry includes the likes of GOOGL, FB,
                            AMZN, NFLX. The highest and lowest current ratio in the industry are 0.9 (NFLX) and 0.3 (GOOGL), respectively.</p>
                    </div>
                    <p>Apple celebrated it's 10th year anniversary with a current ratio of 10. By the looks of it's history (see: the chart and stats above), you can expect Apple to maintain a positive current ratio.</p><div class="container">
    <div id="accordion" class="accordion">
        <div class="card mb-0">
            <div class="card-header collapsed" data-toggle="collapse" href="#collapseOne">
                <a class="card-title">Current Ratio Definition and Formula (What is Current Ratio?)</a>
            </div>
            <div id="collapseOne" class="card-body collapse" data-parent="#accordion">
                <p> According to Investopedia...</p>
                <p> See: 
                    Macrotrends and Gurufocus definitions https://www.gurufocus.com/term/mktcap/AAPL/Market-Cap/Apple</p>
            </div>
            <div class="card-header collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseTwo">
                <a class="card-title"> Additional Information (Company Profile) </a>
            </div>
            <div id="collapseTwo" class="card-body collapse" data-parent="#accordion">
                <p>Website: <a href="https://apple.com">Apple, Inc.</a>
                <p>Apple, Inc. was founded on April 1, 1976. It listed 1990-01-02 on the NASDAQ exchange and started trading with the ticker "AAPL". </p>
                <p>It is based in Cupertino, California.</p>
                <p>

                <p>Apple Inc. (NASDAQ: AAPL) was founded on April 1, 1976.</p>
 
                </p>
                <div> </div>
                <p>
                Unique IDs
                    <ul>
                        <li>CIK: 320193</li>
                        <li>Bloomberg ID: EQ0010169500001000</li>
                        <li>LEI (Legal Entity Identifier): HWUPKR0MPOU8FGXBT394</li>
                	cik	bloomberg	figi	lei	country	industry	sector	marketcap	employees	phone	ceo	url	description	exchange	name	symbol	exchangeSymbol	hq_address	hq_state	hq_country	type	updated	tags	similar	active	sic	Short name
                1990-01-02	320193	EQ0010169500001000		HWUPKR0MPOU8FGXBT394	usa	Computer Hardware	Technology	9.08317E+11	123000	+1 408 996-1010	Timothy D. Cook	http://www.apple.com	Apple Inc is designs, manufactures and markets mobile communication and media devices and personal computers, and sells a variety of related software, services, accessories, networking solutions and third-party digital content and applications.	Nasdaq Global Select	Apple Inc.	AAPL	NGS	1 Infinite Loop Cupertino CA, 95014	CA	USA	CS	11/16/2018	['Technology', 'Consumer Electronics', 'Computer Hardware']	['MSFT', 'NOK', 'IBM', 'HPQ', 'GOOGL', 'BB', 'XLK']	TRUE	3571	Apple

                </p>
            </div>
            <div class="card-header collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseThree">
                <a class="card-title"> Comparables (Current Ratio vs Competition e.g. AMZN, FB, NFLX) </a>
            </div>
            <div id="collapseThree" class="collapse" data-parent="#accordion">
                <div class="card-body">Apple, Inc's current ratio is 0.7, and it's a great one. A current ratio of 0.7 places it ahead of it's industry (Computer Hardware) average of 0.5 and sector (Technology) average. The industry includes the likes of GOOGL, FB, AMZN, NFLX. The highest and lowest current ratio in the industry are 0.9 (NFLX) and 0.3 (GOOGL), respectively. </div>
            </div>
        </div>
    </div>
</div></div>
            </div>
            <div class="col">
                <div class="card shadow border-left-primary py-2" style="margin: 10px;">
                    <div class="card-body">
                        <h2 class="text-primary mb-0 historical">Historical Current Ratio Stats (1984 - 2020)</h2>
                        <div class="text-dark font-weight-bold h5 mb-0"></div>
                    </div>
                    <div class="card-body">
                        <div class="text-dark font-weight-bold h5 mb-0"></div>
                        <div class="table-responsive">
                            <table class="table">
                                <thead class="fin_metric-stats">
                                    <tr>
                                        <th>Statistic</th>
                                        <th>Ratio</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>Mean (μ)</td>
                                        <td>.7</td>
                                    </tr>
                                    <tr>
                                        <td>Std Dev. (σ)<br></td>
                                        <td>Cell 2</td>
                                    </tr>
                                    <tr>
                                        <td>Top 25%</td>
                                        <td>Cell 4</td>
                                    </tr>
                                    <tr>
                                        <td>Bottom 25%</td>
                                        <td>Cell 2</td>
                                    </tr>
                                    <tr>
                                        <td>Max</td>
                                        <td>Cell 2</td>
                                    </tr>
                                    <tr>
                                        <td>Min</td>
                                        <td>Cell 2</td>
                                    </tr>
                                    <tr>
                                        <td>% Change (since inception)</td>
                                        <td>40%</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div class="button_div"><button class="btn btn-primary button_buy" type="button">Historical Financial Ratios Data for entire Industry $5, Sector $10</button></div>
                        <p>We exist bc we want to provide affordable data. Ultimately, only high-level analysis in excel gives you the bigger picture</p>
                    </div>
                </div>
            </div>
        </div>
        <div id="content">
            <div class="row">
                <div class="col">
                    <div class="card shadow border-left-info py-2">
                        <div class="card-body" style="padding: 10px;"></div>
                    </div>
                </div>
            </div>
            <div class="row flex-grow-1">
                <div class="col-md-4 col-xl-6" style="padding: 10px;">
                    <div class="card shadow border-left-primary py-2">
                        <div class="card-body" style="padding: 10px;">
                            <h6 class="text-primary mb-0" style="color: rgb(78,115,223);">Current Ratio in 1984 was 0.94<br>Today CR (2020): 1.5<br></h6>
                            <div class="row align-items-center no-gutters">
                                <div class="col mr-2">
                                    <div class="text-uppercase text-success font-weight-bold text-xs mb-1"><span>Overall change %</span></div>
                                    <div class="text-dark font-weight-bold h5 mb-0"><span>+50%</span></div>
                                </div>
                                <div class="col mr-2">
                                    <div class="text-uppercase text-success font-weight-bold text-xs mb-1"><span>change % (annualized)</span></div>
                                    <div class="text-dark font-weight-bold h5 mb-0"><span>2000%</span></div>
                                </div>
                            </div>
                            <div class="text-dark font-weight-bold h5 mb-0"></div>
                        </div>
                        <div class="card-body" style="padding: 10px;">
                            <h6 class="text-primary mb-0" style="color: rgb(78,115,223);">Lowest CR (1996): 0.5<br>Highest CR (2013): 2<br></h6>
                            <div class="row align-items-center no-gutters">
                                <div class="col mr-2">
                                    <div class="text-uppercase text-success font-weight-bold text-xs mb-1"><span>Overall change %</span></div>
                                    <div class="text-dark font-weight-bold h5 mb-0"><span>+50%</span></div>
                                </div>
                                <div class="col mr-2">
                                    <div class="text-uppercase text-success font-weight-bold text-xs mb-1"><span>change % (annualized)</span></div>
                                    <div class="text-dark font-weight-bold h5 mb-0"><span>$215,000</span></div>
                                </div>
                            </div>
                            <div class="text-dark font-weight-bold h5 mb-0"></div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 col-xl-6 mb-4" style="margin: 0px;margin-bottom: 0px;padding: 10px;">
                    <div class="card shadow border-left-info py-2">
                        <div class="card-body" style="padding: 10px;">
                            <div class="row align-items-center no-gutters" style="padding: 10px;">
                                <div class="col mr-2">
                                    <div class="text-uppercase text-info font-weight-bold text-xs mb-1"><span><strong>Current Ratio Definition and formula.</strong></span></div>
                                    <p>See:&nbsp;<br>Macrotrends &amp; Gurufocus definitions https://www.gurufocus.com/term/mktcap/AAPL/Market-Cap/Apple<br></p>
                                    <div class="row no-gutters align-items-center">
                                        <div class="col-auto">
                                            <div class="text-dark font-weight-bold h5 mb-0 mr-3"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row flex-grow-1 justify-content-center">
                <div class="col">
                    <div class="card shadow mb-4">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h6 class="text-primary font-weight-bold m-0">Apple Inc. (AAPL) Historical Current Ratio Table</h6>
                            <div class="dropdown no-arrow"><button class="btn btn-link btn-sm dropdown-toggle" data-toggle="dropdown" aria-expanded="false" type="button"><i class="fas fa-ellipsis-v text-gray-400"></i></button>
                                <div class="dropdown-menu shadow dropdown-menu-right animated--fade-in"
                                    role="menu">
                                    <p class="text-center dropdown-header">dropdown header:</p><a class="dropdown-item" role="presentation" href="#">&nbsp;Action</a><a class="dropdown-item" role="presentation" href="#">&nbsp;Another action</a>
                                    <div class="dropdown-divider"></div><a class="dropdown-item" role="presentation" href="#">&nbsp;Something else here</a></div>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th>2014</th>
                                            <th>2015</th>
                                            <th>2016</th>
                                            <th>2017</th>
                                            <th>2018</th>
                                            <th>2019</th>
                                            <th>2020</th>
                                            <th>2021</th>
                                            <th>2022</th>
                                            <th>2023</th>
                                            <th>2024</th>
                                            <th>2025</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>Cell 1</td>
                                            <td>Cell 2</td>
                                            <td>Cell 2</td>
                                            <td>Cell 2</td>
                                            <td>Cell 2</td>
                                            <td>Cell 2</td>
                                            <td>Cell 2</td>
                                            <td>Cell 2</td>
                                            <td>Cell 2</td>
                                            <td>Cell 2</td>
                                            <td>Cell 2</td>
                                            <td>Cell 2</td>
                                        </tr>
                                        <tr></tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    <div class="card shadow border-left-primary py-2" style="margin: 0px;padding: 10px;">
                        <div class="card-body" style="padding: 10px;">
                            <p>Popular Stats &amp; Analyses:<br>-&nbsp;<a href="#collapse-1"><span style="text-decoration: underline;">Company Info (CEO, IPO Date, HQ.</span></a>..)<br>-&nbsp;<a href="#collapse-1">[Past] "If I bought AAPL at ______."</a><br>-&nbsp;
                                <a
                                    href="#collapse-1">[Present] "Should I buy AAPL today?"</a><br><br></p>
                            <div class="text-dark font-weight-bold h5 mb-0"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="container-fluid">
                <div class="card shadow border-left-success py-2">
                    <div class="card-body">
                        <h4 class="text-dark mb-0">Lifetime Metrics</h4>
                        <div class="row align-items-center no-gutters">
                            <div class="col mr-2">
                                <div class="text-uppercase text-success font-weight-bold text-xs mb-1"><span>Earnings (annual)</span></div>
                                <div class="text-dark font-weight-bold h5 mb-0"><span>$215,000</span></div>
                            </div>
                            <div class="col mr-2">
                                <div class="text-uppercase text-success font-weight-bold text-xs mb-1"><span>Earnings (annual)</span></div>
                                <div class="text-dark font-weight-bold h5 mb-0"><span>$215,000</span></div>
                            </div>
                        </div>
                        <div class="row align-items-center no-gutters">
                            <div class="col mr-2">
                                <div class="text-uppercase text-success font-weight-bold text-xs mb-1"><span>Earnings (annual)</span></div>
                                <div class="text-dark font-weight-bold h5 mb-0"><span>$215,000</span></div>
                            </div>
                            <div class="col mr-2">
                                <div class="text-uppercase text-success font-weight-bold text-xs mb-1"><span>Earnings (annual)</span></div>
                                <div class="text-dark font-weight-bold h5 mb-0"><span>$215,000</span></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card" style="background-color: rgba(0,0,0,0.48);margin: 10px;">
                    <div class="card-body" style="padding: 2px;"></div>
                </div>
                <div class="row">
                    <div class="col">
                        <p><strong><span style="text-decoration: underline;">Yearly Breakdown</span></strong></p>
                    </div>
                    <div class="col">
                        <p>"If I bought AAPL&nbsp;at the top / bottom / beginning..."</p>
                    </div>
                    <div class="col">
                        <p>Number of Up Days</p>
                    </div>
                    <div class="col">
                        <p>Daily Volatility (+/-% Change)</p>
                    </div>
                </div>
                <div class="col">
                    <div></div>
                    <div class="card" style="background-color: rgba(0,0,0,0.48);margin: 10px;">
                        <div class="card-body" style="padding: 2px;"></div>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        <div>
                            <ul class="nav nav-tabs">
                                <li class="nav-item"><a class="nav-link" role="tab" data-toggle="tab" href="#tab-1">Annual Reports (10K)</a></li>
                                <li class="nav-item"><a class="nav-link" role="tab" data-toggle="tab" href="#tab-4">Quarterly Earnings Report (10Q)</a></li>
                                <li class="nav-item"><a class="nav-link active" role="tab" data-toggle="tab" href="#tab-2">Financial Ratios</a></li>
                                <li class="nav-item"><a class="nav-link" role="tab" data-toggle="tab" href="#tab-3">Key Metrics</a></li>
                                <li class="nav-item"><a class="nav-link" role="tab" data-toggle="tab" href="#tab-3">Earnings Call Transcript</a></li>
                                <li class="nav-item"><a class="nav-link" role="tab" data-toggle="tab" href="#tab-3">Press Releases</a></li>
                            </ul>
                            <div class="tab-content">
                                <div class="tab-pane" role="tabpanel" id="tab-1">
                                    <div class="col"></div>
                                </div>
                                <div class="tab-pane active" role="tabpanel" id="tab-2">
                                    <div class="col">
                                        <div>
                                            <ul class="nav nav-tabs">
                                                <li class="nav-item"><a class="nav-link" role="tab" data-toggle="tab" href="#tab-1">Financial Statements</a></li>
                                                <li class="nav-item"><a class="nav-link active" role="tab" data-toggle="tab" href="#tab-2">Financial Ratios</a></li>
                                                <li class="nav-item"><a class="nav-link" role="tab" data-toggle="tab" href="#tab-3">Tab 3</a></li>
                                            </ul>
                                            <div class="tab-content">
                                                <div class="tab-pane" role="tabpanel" id="tab-1">
                                                    <div class="col"></div>
                                                </div>
                                                <div class="tab-pane active" role="tabpanel" id="tab-2">
                                                    <div class="col">
                                                        <nav class="navbar navbar-light navbar-expand-md">
                                                            <div class="container-fluid"><a class="navbar-brand" href="#">Brand</a><button data-toggle="collapse" class="navbar-toggler" data-target="#navcol-1"><span class="sr-only">Toggle navigation</span><span class="navbar-toggler-icon"></span></button>
                                                                <div
                                                                    class="collapse navbar-collapse" id="navcol-1">
                                                                    <ul class="nav navbar-nav">
                                                                        <li class="nav-item" role="presentation"><a class="nav-link active" href="#">First Item</a></li>
                                                                        <li class="nav-item" role="presentation"><a class="nav-link" href="#">Second Item</a></li>
                                                                        <li class="nav-item" role="presentation"><a class="nav-link" href="#">Third Item</a></li>
                                                                    </ul>
                                                            </div>
                                                    </div>
                                                    </nav>
                                                </div>
                                            </div>
                                            <div class="tab-pane" role="tabpanel" id="tab-3">
                                                <div class="col"></div>
                                            </div>
                                        </div>
                                    </div>
                                    <nav class="navbar navbar-light navbar-expand-md">
                                        <div class="container-fluid"><a class="navbar-brand" href="#">Brand</a><button data-toggle="collapse" class="navbar-toggler" data-target="#navcol-1"><span class="sr-only">Toggle navigation</span><span class="navbar-toggler-icon"></span></button>
                                            <div
                                                class="collapse navbar-collapse" id="navcol-1">
                                                <ul class="nav navbar-nav">
                                                    <li class="nav-item" role="presentation"><a class="nav-link active" href="#">First Item</a></li>
                                                    <li class="nav-item" role="presentation"><a class="nav-link" href="#">Second Item</a></li>
                                                    <li class="nav-item" role="presentation"><a class="nav-link" href="#">Third Item</a></li>
                                                </ul>
                                        </div>
                                </div>
                                </nav>
                            </div>
                        </div>
                        <div class="tab-pane" role="tabpanel" id="tab-3">
                            <div class="col"></div>
                        </div>
                        <div class="tab-pane" role="tabpanel" id="tab-4">
                            <p>Tab content.</p>
                        </div>
                        <div class="tab-pane" role="tabpanel" id="tab-5">
                            <div class="col"></div>
                        </div>
                        <div class="tab-pane" role="tabpanel" id="tab-6">
                            <div class="col">
                                <div>
                                    <ul class="nav nav-tabs">
                                        <li class="nav-item"><a class="nav-link" role="tab" data-toggle="tab" href="#tab-1">Financial Statements</a></li>
                                        <li class="nav-item"><a class="nav-link active" role="tab" data-toggle="tab" href="#tab-2">Financial Ratios</a></li>
                                        <li class="nav-item"><a class="nav-link" role="tab" data-toggle="tab" href="#tab-3">Tab 3</a></li>
                                    </ul>
                                    <div class="tab-content">
                                        <div class="tab-pane" role="tabpanel" id="tab-1">
                                            <div class="col"></div>
                                        </div>
                                        <div class="tab-pane active" role="tabpanel" id="tab-2">
                                            <div class="col">
                                                <nav class="navbar navbar-light navbar-expand-md">
                                                    <div class="container-fluid"><a class="navbar-brand" href="#">Brand</a><button data-toggle="collapse" class="navbar-toggler" data-target="#navcol-1"><span class="sr-only">Toggle navigation</span><span class="navbar-toggler-icon"></span></button>
                                                        <div
                                                            class="collapse navbar-collapse" id="navcol-1">
                                                            <ul class="nav navbar-nav">
                                                                <li class="nav-item" role="presentation"><a class="nav-link active" href="#">First Item</a></li>
                                                                <li class="nav-item" role="presentation"><a class="nav-link" href="#">Second Item</a></li>
                                                                <li class="nav-item" role="presentation"><a class="nav-link" href="#">Third Item</a></li>
                                                            </ul>
                                                    </div>
                                            </div>
                                            </nav>
                                        </div>
                                    </div>
                                    <div class="tab-pane" role="tabpanel" id="tab-3">
                                        <div class="col"></div>
                                    </div>
                                </div>
                            </div>
                            <nav class="navbar navbar-light navbar-expand-md">
                                <div class="container-fluid"><a class="navbar-brand" href="#">Brand</a><button data-toggle="collapse" class="navbar-toggler" data-target="#navcol-1"><span class="sr-only">Toggle navigation</span><span class="navbar-toggler-icon"></span></button>
                                    <div
                                        class="collapse navbar-collapse" id="navcol-1">
                                        <ul class="nav navbar-nav">
                                            <li class="nav-item" role="presentation"><a class="nav-link active" href="#">First Item</a></li>
                                            <li class="nav-item" role="presentation"><a class="nav-link" href="#">Second Item</a></li>
                                            <li class="nav-item" role="presentation"><a class="nav-link" href="#">Third Item</a></li>
                                        </ul>
                                </div>
                        </div>
                        </nav>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </div>
    <div class="row">
        <div class="col-md-6 col-xl-3 mb-4">
            <div class="card shadow border-left-primary py-2">
                <div class="card-body">
                    <div class="row align-items-center no-gutters">
                        <div class="col mr-2">
                            <div class="text-uppercase text-primary font-weight-bold text-xs mb-1"><span>Earnings (monthly)</span><span>Earnings (monthly)</span></div>
                            <div class="text-dark font-weight-bold h5 mb-0"><span>$40,000</span></div>
                        </div>
                        <div class="col-auto"><i class="fas fa-calendar fa-2x text-gray-300"></i></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-xl-3 mb-4">
            <div class="card shadow border-left-success py-2">
                <div class="card-body">
                    <div class="row align-items-center no-gutters">
                        <div class="col mr-2">
                            <div class="text-uppercase text-success font-weight-bold text-xs mb-1"><span>Earnings (annual)</span></div>
                            <div class="text-dark font-weight-bold h5 mb-0"><span>$215,000</span></div>
                        </div>
                        <div class="col-auto"><i class="fas fa-dollar-sign fa-2x text-gray-300"></i></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-xl-3 mb-4">
            <div class="card shadow border-left-info py-2">
                <div class="card-body">
                    <div class="row align-items-center no-gutters">
                        <div class="col mr-2">
                            <div class="text-uppercase text-info font-weight-bold text-xs mb-1"><span>Tasks</span></div>
                            <div class="row no-gutters align-items-center">
                                <div class="col-auto">
                                    <div class="text-dark font-weight-bold h5 mb-0 mr-3"><span>50%</span></div>
                                </div>
                                <div class="col">
                                    <div class="progress progress-sm">
                                        <div class="progress-bar bg-info" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width: 50%;"><span class="sr-only">50%</span></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-auto"><i class="fas fa-clipboard-list fa-2x text-gray-300"></i></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-xl-3 mb-4">
            <div class="card shadow border-left-warning py-2">
                <div class="card-body">
                    <div class="row align-items-center no-gutters">
                        <div class="col mr-2">
                            <div class="text-uppercase text-warning font-weight-bold text-xs mb-1"><span>Pending Requests</span></div>
                            <div class="text-dark font-weight-bold h5 mb-0"><span>18</span></div>
                        </div>
                        <div class="col-auto"><i class="fas fa-comments fa-2x text-gray-300"></i></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </div>
    </div>
    </div>
    <section>
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-6 order-lg-2">
                    <div class="p-5"><img class="rounded-circle img-fluid" src="assets/img/03.jpg"></div>
                </div>
                <div class="col-lg-6 order-lg-1">
                    <div class="p-5">
                        <h2 class="display-4">Let there be rock!</h2>
                        <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quod aliquid, mollitia odio veniam sit iste esse assumenda amet aperiam exercitationem, ea animi blanditiis recusandae! Ratione voluptatum molestiae adipisci, beatae obcaecati.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.0/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.min.js"></script>
    <script src="assets/js/script.min.js"></script>
</body>

</html>