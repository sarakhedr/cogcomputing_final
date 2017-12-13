var startDate = ""
var endDate = ""
var toneBreakdownData = []

var toneTrendData = [['Day', 'Anger', 'Sadness', 'Happiness', 'Analytical'],
					 ['2017-12-05', 1, 1, 0, 1], 
					 ['2017-12-06', 1, 1, 0, 1],
					 ['2017-12-07', 0, 0, 1, 0],  
					 ['2017-12-08', 0, 0, 1, 0],  
					 ['2017-12-09', 0, 0, 1, 0],  
					 ['2017-12-10', 0, 0, 1, 0],  
					 ['2017-12-11', 0, 0, 1, 0]]  

$(document).ready(function() {
	google.charts.load("current", {packages:["corechart"]});
	getDateRange()
});

function getToneBreakdown() {
	$.ajax({
		type: "GET",
		url: "/api/tone-breakdown",
		data: {
			startDate: startDate,
			endDate: endDate
		},
		success: function(response) {
			toneBreakdownData = []
			toneBreakdownData.push(['Tone', 'Number of Entries'])
			$.each(response, function(key, element) {
				// console.log(key, element)
				toneBreakdownData.push([key, element])
			})
			drawPieChart()
		},
		error: function(chr) {
		 	console.log("Error!")
		}
	});
}

function getToneTrend() {
	$.ajax({
		type: "GET",
		url: "/api/tone-trend",
		data: {
			startDate: startDate,
			endDate: endDate
		},
		success: function(response) {
			console.log(response)
			toneTrendData = []
			var tones = ['Date']
			var toneRow = [0]
			$.each(response, function(key, element) {
				// console.log(key, element)
				for (var i in element) {
					if (tones.indexOf(element[i]) == -1) {
						tones.push(element[i])
						toneRow.push(0)
					}
				}
			})
			toneTrendData.push(tones)
			$.each(response, function(key, element) {
				// console.log(key, element)
				var row = toneRow.slice()
				row[0] = key
				for (var i in element) {
					var index = tones.indexOf(element[i])
					row[index] = 1
				}
				toneTrendData.push(row)
			})
			console.log(toneTrendData)
			drawStackedChart()
			// google.setOnLoadCallback(drawStackedChart());
		},
		error: function(chr) {
		 	console.log("Error!")
		}
	});
}

function getKeywords(emotion, i) {
	$.ajax({
		type: "GET",
		url: "/api/keywords",
		data: {
			startDate: startDate,
			endDate: endDate,
			emotion: emotion,
			k: 5,
		},
		success: function(response) {
			console.log(emotion)
			console.log(response)
			var className = "keywordRight"
			if (i%2 == 0) className = "keywordLeft"
			console.log(className)
			var emotionHTML = '<div class="' + className + '">' +
		 					'<center> <strong style="font-size: large">' + emotion + '</strong> </center>' +
		 					'<hr/>' +
			 				'<div id="topKeywords">'
			for (var j in response) {
				emotionHTML += '<div class="phrase">' +
						  		'<center>' + j  + '</center>' + 
								'</div>'
			}
			
			emotionHTML += '</div></div>'
			$("#emotionKeywords").append(emotionHTML)
		},
		error: function(chr) {
		 	console.log("Error!")
		}
	})
}



function getDateRange() {
	$.ajax({
		type: "GET",
		url: "/api/date-range",
		success: function(response) {
			startDate = response["max_date"]
			endDate = response["min_date"]

		$('input[name="daterange"]').daterangepicker(
		    {
		      locale: {
		        format: 'YYYY-MM-DD'
		      },
		      startDate: startDate,
		      endDate: endDate,
		      minDate: startDate,
		      maxDate: endDate
		    }, 
		    function(start, end, label) {
		      startDate = start.format('YYYY-MM-DD')
		      endDate = start.format('YYYY-MM-DD')
		})

		//google.charts.load("current", {packages:["corechart"]});
		google.setOnLoadCallback(getToneBreakdown());
		google.setOnLoadCallback(getToneTrend());
		getEmotionKeywords();

		},
		error: function(chr) {
		 	console.log("Error!")
		}
	});
}

function getEmotionKeywords() {
	console.log("Emotion Keywords")
	var emotionOptions = ["sadness", "joy", "fear", "anger", "disgust"]
	for (var i in emotionOptions) {
		console.log(emotionOptions[i])
		emotion = emotionOptions[i]
		getKeywords(emotion, i)
	}
}

function drawPieChart() {
	console.log("Got here!")
	console.log(toneBreakdownData)
	var options = {
		title: "Tone Breakdown",
		is3D: true,
		width: 400

	}

	var transformedData = google.visualization.arrayToDataTable(toneBreakdownData)
	var chart = new google.visualization.PieChart(document.getElementById('tonePieChart'));
	chart.draw(transformedData, options);
}

function drawStackedChart() {
	var options = {
        title: 'Tone Trend',
        animation: {startup: true, duration: 1000, easing: 'inAndOut'},
        isStacked: true,
        width: 600
    };

    var transformedData = google.visualization.arrayToDataTable(toneTrendData)
	var chart = new google.visualization.ColumnChart(document.getElementById('toneStackedChart'));
	chart.draw(transformedData, options);

}