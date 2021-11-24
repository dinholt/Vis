function recv()
{
    $.getJSON("/query?type=all_shops",function(data){
        $.each(data,function(idx,item){
            option.series[0].data.append([ item[1],item[2][0],item[2][1] ]);
        });
    });
}

var chartDom = document.getElementById('view');
var myChart = echarts.init(chartDom);
var option;

option = {
    title: {
        text: '餐馆可视化',
        left: 'center'
      },
    bmap: {
        center: [104.741722, 31.46402],
        zoom: 12,
        roam: true
    },
    series: [
      {
        type: 'scatter',
        coordinateSystem: 'bmap',
        data: [],
        symbolSize: function (val) {
            return val[2] / 10;
        },
        encode: {
            value: 2
        },
        label: {
            formatter: '{b}',
            position: 'right',
            show: false
        },
        emphasis: {
            label: {
            show: true
        }
      }
    }]
  };

  recv()

myChart.setOption(option);