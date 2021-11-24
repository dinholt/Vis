function recv()
{
    $.getJSON(
        "/query?type=all_shops",
        function(data)
        {
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
    },
    series: [
      {
        type: 'scatter',
        coordinateSystem: 'bmap',
        itemStyle: {
            color: 'rgba(251, 118, 123, 0.6)',
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

recv()

myChart.on('click',  function(param) {
    click_on_shop(param.data)
});

function setOption()
{
    myChart.setOption(option);
}

function click_on_shop(data)
{
    console.log(data);
    show_shop_detail(data['name'],data['poiid'])
    wc_img = document.getElementById("wc_img")
    wc_img.setAttribute("src",'/wordcloud?id='+data['poiid']+"&seed="+Math.random())
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