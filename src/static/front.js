function recv()
{
    $.getJSON("/query?type=all_shops",function(data){
        $.each(data,function(idx,item){
            //console.log(option.series[0].data,"sdkfj");
            option.series[0].data.push( {name:item[1],value:[item[3][0],item[3][1]], poiid:item[0]} );
        ;});
        setOption();
    })
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
        roam: true,
    },
    series: [
      {
        type: 'scatter',
        coordinateSystem: 'bmap',
        itemStyle: {
            color: 'rgba(251, 118, 123, 0.3)',
        },
        large:true,
        data: [],
        symbolSize: 8,
        encode: {
            value: 2
        },
        label: {
            formatter: '<font class="label_text">{b}</font>',
            position: 'right',
            show: false
        },
        emphasis: {
            label: {
            show: true
        },
      }
    }]
  };

recv()

myChart.on('click',  function(param) {
    console.log(param.name);
    console.log(param.data)
});

function setOption()
{
    myChart.setOption(option);
}