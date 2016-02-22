// Setup before functions
var typingTimer;                // Timer identifier
var doneTypingInterval = 1000;  // Time in MS
var $input = $('#inputActorName');

// On keyup, start the countdown
$input.on('keyup', function () {
  clearTimeout(typingTimer);
  typingTimer = setTimeout(generateChart, doneTypingInterval);
});

//on keydown, clear the countdown 
$input.on('keydown', function () {
  clearTimeout(typingTimer);
});

// Function to "proper case" names
function toProperCase(str) {
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

// The function to run when the user is finished typing
function generateChart () {

    var movie_processed_json = new Array();
    var baby_processed_json = new Array();

    // Parse form data and get first name
    var actor_full_name = toProperCase($('#inputActorName').val());
    var actor_first_name = actor_full_name.split(" ")[0];

    // Parse popular movies data
    $.getJSON('http://127.0.0.1:5000/popular-movies/'.concat(actor_full_name), function (movie_data) {

      // Parse baby name data
      $.getJSON('http://127.0.0.1:5000/segment-baby-names?name='.concat(actor_first_name), function (baby_data) {

          // Populate series
          for (i = 0; i < baby_data.length; i++) {
            // Check for movies in each year
            for (j=0; j < movie_data.length; j++) {
              // Check years
              if (movie_data[j]['year'] == baby_data[i]['year']) {
                movie_processed_json.push({'x': movie_data[j]['year'], 'y': baby_data[i]['count'], 'title': movie_data[j]['title'], 'link': movie_data[j]['link']})
              }
            }

            // Add baby data to array
            baby_processed_json.push([baby_data[i]['year'], baby_data[i]['count']])
          }

          // Add commas to tooltip values
          Highcharts.setOptions({
            lang: {
              thousandsSep: ','
            }
          });

          // Construct chart
          $('#linechart').highcharts({
              chart: {
                  zoomType: 'x'
              },
              title: {
                  text: 'Baby Names Over Time: '.concat(actor_first_name)
              },
              subtitle: {
                  text: document.ontouchstart === undefined ?
                          'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
              },
              xAxis: {
                  title: {
                    text: 'Year'
                  },
                  min: 1910
              },
              yAxis: {
                  title: {
                      text: 'Yearly Name Count'
                  }
              },
              tooltip: {
                shared: true,
                useHTML: true,
                formatter: function() {
                  if (this.points[1] == null) {
                    return '<div style="text-align: center;"><strong>' + this.points[0].x + '</strong>' + '<br>' + '<strong>' + this.points[0].y + '</strong> babies named <strong>' + actor_first_name + '</strong></div>'
                  } else {
                    return '<div style="text-align: center;"><strong>' + this.points[0].x + '</strong>' + '<br>' + '<strong>' + this.points[0].y + '</strong> babies named <strong>' + actor_first_name + '</strong>' + '<br>' + '<strong>' + actor_full_name + '</strong>, <strong>' + this.points[1].point.title + '</strong></div>'
                  }
                }
              },
              legend: {
                  enabled: true
              },
              plotOptions: {
                  series: {
                      states: {
                          hover: {
                              enabled: false
                          }
                      }
                  }
              },
              series: [{
                  type: 'line',
                  name: 'Baby Name Count',
                  data: baby_processed_json,
                  lineWidth: 3,
                  marker: {
                    enabled: false
                  },
                  zIndex: 0
                },
                {
                  type: 'line',
                  name: 'Popular Movies',
                  data: movie_processed_json,
                  lineWidth: 0,
                  marker: {
                    enable: true,
                    symbol: 'square',
                    radius: 5
                  },
                  zIndex: 1
              }],
              exporting: {
                enabled: false
              }
          });
      });
  });
}