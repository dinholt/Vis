function recv(type="scatter")
{
    console.log(type)
    if(type=="scatter")
    {
        $.getJSON(
            "/query?type=all_shops&sff="+score_filter_from+"&sft="+score_filter_to+"&pff="+price_filter_from+"&pft="+price_filter_to,
            function(data)
            {
                option.series[0].data = []
                $.each(
                    data,function(idx,item)
                    {
                    //console.log(option.series[0].data,"sdkfj");
                        option.series[0].data.push( { name:item[1],value:[item[3][0],item[3][1]], poiid:item[0] } );
                    }
                );
                setOption();
                }
        )
    }
    if(type=="heatmap")
    {
        $.getJSON(
            "/query?type=all_shops&sff="+score_filter_from+"&sft="+score_filter_to+"&pff="+price_filter_from+"&pft="+price_filter_to,
            function(data)
            {
                option.series[0].data = []
                $.each(
                    data,function(idx,item)
                    {
                    //console.log(option.series[0].data,"sdkfj");
                        option.series[0].data.push( [item[3][0],item[3][1],1] );
                    }
                );
                setOption();
                }
            )
    }
    
}

var score_filter_from = 1
var score_filter_to = 5
var price_filter_from = 10
var price_filter_to = 40
var current_type = "scatter"

var chartDom = document.getElementById('map_view');
var myChart = echarts.init(chartDom);
var option;

option = {
    title: {
        text: '',
        left: 'center'
      },
    bmap: {
        center: [104.741722, 31.46402],
        zoom: 12,
        roam: true,
        enableMapClick: false
    },
    visualMap: {
        show: false,
        top: 'top',
        min: 0,
        max: 20,
        seriesIndex: 0,
        calculable: true,
        inRange: {
          color: [ 'green', 'yellow', 'rgba(218, 68, 83, 0.8)'],
        },
    },
    series: [
      {
        type: 'scatter',
        coordinateSystem: 'bmap',
        itemStyle: {
            color: 'rgba(218, 68, 83, 0.8)',
        },
        large:true,
        data: [],
        symbolSize: 10,
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
        },
      }
    }]
  };

var first_run = true
function setOption()
{
    if(!first_run)
    {
        option.bmap = null
        option.visualMap = null
    }
    myChart.setOption(option);
    first_run = false
}

function switch_to_heat()
{
    $("#select_shops_analysis").attr("class","select")
    $("#select_users_analysis").attr("class","select")
    $("#select_shops_heat").attr("class","select select_selected")
    option.series[0].type = "heatmap"
    current_type = "heatmap"
    recv("heatmap")
}

function switch_to_scatter()
{
    $("#select_shops_analysis").attr("class","select select_selected")
    $("#select_users_analysis").attr("class","select")
    $("#select_shops_heat").attr("class","select")
    option.series[0].type = "scatter"
    current_type = "scatter"
    recv("scatter")
}

function click_on_shop(data)
{
    console.log(data);
    show_shop_detail(data['name'],data['poiid'])
    wc_img = document.getElementById("wc_img")
    wc_img.setAttribute("src",'/wordcloud?id='+data['poiid']+"&seed="+Math.random()+"&type=shop" )
}

function show_shop_detail(name,poiid)
{
    $.getJSON(
        "/query?type=shop_detail&poiid="+poiid,
        function(data)
        {
            detail_view = document.getElementById("detail_view")

            detail_view.getElementsByClassName("text_title")[0].textContent = name;
            detail_view.getElementsByClassName("text_sub")[0].textContent = "SID:"+poiid

            if(parseFloat( data['avgScore'])<1e-6)
            {
                detail_view.getElementsByClassName("stars_cutter")[0].style.setProperty("width",0)
                detail_view.getElementsByClassName("score")[0].textContent = "无评分"
                detail_view.getElementsByClassName("score")[0].style.setProperty("width",'140px')
            }else
            {
                detail_view.getElementsByClassName("stars_cutter")[0].style.setProperty("width", ( parseFloat( data['avgScore'])/5 * 100 ) + 'px' )
                detail_view.getElementsByClassName("score")[0].textContent = data['avgScore']
                detail_view.getElementsByClassName("score")[0].style.setProperty("width",'50px')
            }

        }
    )

    document.getElementById("detail_view_border").style.setProperty("right","50px")
}
function close_shop_detail()
{
    document.getElementById("detail_view_border").style.setProperty("right","-550px")
}

$("#slider_score").ionRangeSlider({
    type: "double",
    min: 1,
    max: 5,
    from: 3.5,
    to: 5,
    step: 0.5,
    grid: true,
    onFinish: function(data)
    {
        console.log(data.from,data.to)
        score_filter_from = data.from
        score_filter_to = data.to
        recv(current_type)
    }
});

$("#slider_price").ionRangeSlider({
    type: "double",
    min: 5,
    max: 100,
    from: 10,
    to: 40,
    step: 1,
    grid: true,
    onFinish: function(data)
    {
        console.log(data.from,data.to)
        price_filter_from = data.from
        price_filter_to = data.to
        recv(current_type)
    }
});

switch_to_scatter()
myChart.on('click',  function(param) {
    click_on_shop(param.data)
});