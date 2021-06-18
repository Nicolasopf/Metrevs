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
	if (cookie.indexOf("chartsData") != 1) {
		var prs_array = cookie.split("chartsData=")[1].slice(1, -1).replace(/\\054/g, ",").split(", ")
		break;
	}
}
var types = ['bar', 'doughnut', 'polarArea', 'line'];
create_chart("myChart1", "polarArea", ["Total PRs", "Open PRs", "Closed PRs"], "PRs stats", prs_array);
// create_chart("myChart2", "bar", ["a"], "a", 1);
// create_chart("myChart3", "polarArea", ["b"], "b", 2);
// create_chart("myChart4", "line", ["c"], "c", 3);
