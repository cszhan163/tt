
wx.ready(function () {
  // 1 判断当前版本是否支持指定 JS 接口，支持批量判断
  document.querySelector('#checkJsApi').onclick = function () {
    wx.checkJsApi({
      jsApiList: [
        'getNetworkType',
        'configWXDeviceWiFi'
      ],
      success: function (res) {
        alert(JSON.stringify(res));
      }
    });
  };
document.querySelector('#airkissConfig').onclick = function () {
    wx.invoke('configWXDeviceWiFi', {}, function(res){
                        var err_msg = res.err_msg;
                        if(err_msg == 'configWXDeviceWiFi:ok') {
                            $('#message').html("配置 WIFI成功，<span id='second'>5</span>秒后跳转到首页。");
                            setInterval(count,1000);
                            return;
                        } else {
                            $('#message').html("配置 WIFI失败，是否<a href=\"/wechat/printer/airkiss" + window.location.search +  "\">再次扫描</a>。");
                        }
                    });

}

document.querySelector('#airkissScan').onclick = function () {

    wx.invoke('startScanWXDevice', {}, function(res){
                        var err_msg = res.err_msg;
                        if(err_msg == 'configWXDeviceWiFi:ok') {
                            $('#message').html("配置 WIFI成功，<span id='second'>5</span>秒后跳转到首页。");
                            setInterval(count,1000);
                            return;
                        } else {
                            $('#message').html("配置 WIFI失败，是否<a href=\"/wechat/printer/airkiss" + window.location.search +  "\">再次扫描</a>。");
                        }
                    });
}

wx.onWXDeviceBindStateChange(function(){

});
wx.onScanWXDevicesResult(function(devices,isCompleted,contentType,){

});

});

wx.error(function (res) {
alert(res.errMsg);
});
