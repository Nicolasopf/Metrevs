function create_chart(chart_name, chart_type, items, label_name, items_data) {
        var ctx = document.getElementById(chart_name);

        var myChart = new Chart(ctx, {
                type: chart_type,
                data: {
                        labels: items,
                        datasets: [{
                                label: label_name,
                                data: items_data,
                                backgroundColor: [
                                        'rgba(255, 99, 132, 0.2)',
                                        'rgba(54, 162, 235, 0.2)',
                                        'rgba(255, 206, 86, 0.2)',
                                        'rgba(75, 192, 192, 0.2)',
                                        'rgba(153, 102, 255, 0.2)',
                                        'rgba(255, 159, 64, 0.2)'
                                ],
                                borderColor: [
                                        'rgba(255, 99, 132, 1)',
                                        'rgba(54, 162, 235, 1)',
                                        'rgba(255, 206, 86, 1)',
                                        'rgba(75, 192, 192, 1)',
                                        'rgba(153, 102, 255, 1)',
                                        'rgba(255, 159, 64, 1)'
                                ],
                                borderWidth: 1
                        }]
                },
                options: {
                        scales: {
                                y: {
                                        beginAtZero: true
                                }
                        }
                }
        });
};

var cookies = document.cookie.split(";");
for (cookie of cookies) {
	if (cookie.indexOf("chartsData") != -1) {
		var arrays = cookie.split("chartsData=")[1].slice(1, -1).replace(/\\054/g, ",").split("-");
		var prs_array = arrays[0].split(",");
		var time_merge_list = arrays[1].split(", ");
		var time_merge_obj = {}

		for (var data of time_merge_list) {
			try {
				var tmp = data.split(":")
				if (tmp[1] === undefined) {
					break
				}
				time_merge_obj[tmp[0]] = tmp[1]
			}
			catch {
				break
			}
		}

		var comments = arrays[2].split(", ")
		var comments_obj = {}

		for (data of comments) {
			try {
				var tmp = data.split(":")
				if (tmp[1] === undefined) {
					break
				}
				comments_obj[tmp[0]] = tmp[1]
			}
			catch {
				break
			}
		}

		var merged = arrays[3].split(", ")
		var merged_obj = {}

		for (data of merged) {
			try {
				var tmp = data.split(":")
				if (tmp[1] === undefined) {
					break
				}
				merged_obj[tmp[0]] = tmp[1]
			}
			catch {
				break
			}
		}
		break;
	}
}

if (prs_array[0] != "0") {
	create_chart("myChart1", "polarArea", ["Total PRs", "Open PRs", "Closed PRs"], "PRs stats", prs_array);
}
if (time_merge_obj[0]) {
	create_chart("myChart2", "doughnut", Object.keys(time_merge_obj), "Time merge from create", Object.values(time_merge_obj));
}
if (comments_obj[0]) {
	create_chart("myChart3", "bar", Object.keys(comments_obj), "Comments in PRs", Object.values(comments_obj));
}
if (merged_obj[0]) {
	create_chart("myChart4", "pie", Object.keys(merged_obj), "Merged PRs", Object.values(merged_obj));
}
