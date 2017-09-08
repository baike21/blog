/*
 * loadmore.js
*/

$(function () {
    /*  初始化  */
    var counter = 0;   /*计数器*/
    var pageStart = 0; /*偏置*/
    var pageSize = 3;  /*每次大小*/
    /*首次加载*/
    getData(pageStart, pageSize);
    /*监听点击加载更多*/
    $('input[type="button"]').click(function () {
        counter ++;
        pageStart = counter * pageSize;
        getData(pageStart, pageSize);
        });
});
/*       业务逻辑代码，负责从服务端拉去数据      */
function getData(offset,size){
    $.ajax({
        type: 'GET',
        url: 'movie.html',  /* 向backends要数据的url地址 */
        dataType: 'json',          /* 数据类型 */
        data:{},                   /* 发送什么数据给服务器 */
        success: function(response){  /* response是ajax请求成功后返回的参数,json字符串，需要先解码成字典 */
            //alert(JSON.parse(response).bloglist);
            //console.log(response);
            var json_data = JSON.parse(response);
            var data = json_data.bloglist;
            var sum = json_data.bloglist.length;
            var result = '';
            /* 不够加载满的情况 部署在SQL上时不需要*/
            if(sum - offset < size ){
                size = sum - offset;
            }
            for(var i=offset; i<(offset+size); i++){
                result +='<ul class="arrow-box"><div class="leaf-shape">'+'<img src="/static/images/02.jpg">'+
                        '<p><a class="review-title" href="#" target="_blank">'+ data[i].title +'</a></p>'+
                        '<span class="dateview">'+ data[i].pub_time +'</span></div></ul>';
            }

            $('.blog-list-fluid').append(result);

            /*隐藏more*/
            if ( (offset + size) >= sum){
                $(".load-more").hide();
            }else{
                $(".load-more").show();
            }
        },
        error: function(xhr, errorCode, errorInfo){
            alert('Ajax error!');
        }
    });
}

