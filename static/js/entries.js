var startDate = ""
var endDate = ""

$(document).ready(function() {
	getDateRange()
});

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

		getTextEntries()

		},
		error: function(chr) {
		 	console.log("Error!")
		}
	});
}

function getTextEntries() {
	console.log(startDate)
	$.ajax({
		type: "GET",
		url: "/api/entries",
		startDate: startDate,
		endDate: endDate,
		success: function(response) {
			for (var i in response.reverse()) {
				var date = response[i]["date"]
				var text = response[i]["text"]
				var type = response[i]["type"]
				var imgType = "text_pencil.png"
				if (type == "audio") imgType = "microphone.png"
				console.log(imgType)
				$("#allentries").append('<div class="entry_">' +
											'<img src="/static/img/' + imgType + '" ></img><h2 class="entry_title"><span class="date">' + date + '</span></h2>' +
											'<p class="entry_text">' + 
												text + 
											'</p>' +
											'<p class="spacer"></p>' +
										'</div>')
			}
		},
		error: function(chr) {
		 	console.log("Error!")
		}
	});
}


