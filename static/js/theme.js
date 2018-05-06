Highcharts.theme = {
    colors: ['#514F78', '#42A07B', '#9B5E4A', '#72727F', '#1F949A',
        '#82914E', '#86777F', '#42A07B'],
    chart: {
        backgroundColor: 'transparent',
        className: 'skies',
        borderWidth: 0,
        plotShadow: true,
        plotBackgroundColor: {
            stops: [
                [0, 'rgba(255, 255, 255, 1)'],
                [1, 'rgba(255, 255, 255, 0)']
            ]
        },
        plotBorderWidth: 1
    },
    title: {
        style: {
            color: '#454545',
            font: '16px Lucida Grande, Lucida Sans Unicode,' +
                ' Verdana, Arial, Helvetica, sans-serif'
        }
    },
    subtitle: {
        style: {
            color: '#799f7e',
            font: '12px Lucida Grande, Lucida Sans Unicode,' +
                ' Verdana, Arial, Helvetica, sans-serif'
        }
    },
    xAxis: {
        gridLineWidth: 0,
        lineColor: '#C0D0E0',
        tickColor: '#C0D0E0',
        labels: {
            style: {
                color: '#666',
                fontWeight: 'bold'
            }
        },
        title: {
            style: {
                color: '#666',
                font: '12px Lucida Grande, Lucida Sans Unicode,' +
                ' Verdana, Arial, Helvetica, sans-serif'
            }
        }
    },
    yAxis: {
        alternateGridColor: '#beeac1',
        lineColor: '#C0D0E0',
        tickColor: '#C0D0E0',
        tickWidth: 1,
        labels: {
            style: {
                color: '#666',
                fontWeight: 'bold'
            }
        },
        title: {
            style: {
                color: '#666',
                font: '12px Lucida Grande, Lucida Sans Unicode,' +
                ' Verdana, Arial, Helvetica, sans-serif'
            }
        }
    },
    legend: {
        itemStyle: {
            font: '9pt Trebuchet MS, Verdana, sans-serif',
            color: '#000000'
        },
        itemHoverStyle: {
            color: 'black'
        },
        itemHiddenStyle: {
            color: 'silver'
        }
    },
    labels: {
        style: {
            color: '#496f40'
        }
    }
};

// Apply the theme
Highcharts.setOptions(Highcharts.theme);