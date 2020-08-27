<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Cache-Control" content="no-siteapp" />
<meta http-equiv="Cache-Control" content="no-transform" />
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="applicable-device" content="pc,mobile">
<meta name="viewport" content="initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no" />
<meta name="renderer" content="webkit" />
<title>正在播放</title>
<meta name="keywords" content="" />
<meta name="description" content="" />
<link rel="stylesheet" href="langapp.css" type="text/css" />
<script type="text/javascript" src="jquery-3.3.1.min.js"></script>
<script src="jquery.js"></script>
<script>var maccms={"path":"","mid":"1","aid":"15","mob_status":"0"};</script>
<script src="home.js"></script>
	<!--[if lt IE 9]>
	<script src="https://cdn.bootcss.com/html5shiv/3.7.2/html5shiv.min.js"></script>
	<script src="https://cdn.bootcss.com/respond.js/1.4.2/respond.min.js"></script>
	<![endif]-->
</head>
<body>
     
<table width="95%" border="1" cellpadding="2" cellspacing="1">
    <tr>
<?php
//遍历子文件夹和文件夹的内容 并且计算出文件的多少
//一个demo  引号替换下
function scan($dir){
   $dirArr = scandir($dir);
   $i = 0;
    foreach($dirArr as $v){
     if(is_file("videos/".$v) && $v!="." && $v!=".."){
        if($i%6==1){
            echo '<tr>';
        }
        $str = "http://127.0.0.1/videos/".$v;
        echo "<td width='16.7%' nowrap><a href='http://127.0.0.1/videos_list.php?url=".base64_encode($str)."'>".$v."</a></td>";
        if($i%6==0){
            echo '</tr>';
        }
        $videos[$i] = $str;
        $i++;
      }
    }
}
if(empty($_GET['url'])){
  scan("./videos");
}
function next_video($dir){
    $dirArr = scandir($dir);
    $i = 0;
    foreach($dirArr as $v){
        if(is_file("videos/".$v) && $v!="." && $v!=".."){
            $str = "http://127.0.0.1/videos/".$v;
            $videos[$i] = $str;
            $i++;
        }
    }
    for($i=0;$i<count($videos);$i++){
        if($_GET['url']==base64_encode($videos[$i])){
            return base64_encode($videos[$i+1]);
        }
    }
    return '';
}
$next = next_video('./videos');
?>
    </tr>
</table>
    <div class="container">
<div class="pl-box">
<script type="text/javascript">var player_data={"flag":"play","encrypt":2,"trysee":0,"points":0,"link":"\/wmjpvod\/123727play-1-1.html","link_next":"","link_pre":"","url":"<?=$_GET['url']?>","url_next":"","from":"videojs","server":"","note":""}</script>
<script type="text/javascript" src="playerconfig.js"></script>
<script type="text/javascript" src="player.js"></script>
</div>
            <div class="stui-pannel clearfix">
                <div class="stui-player col-pd">
                    <div class="stui-player__detail detail">
                       <div class="video-title">
                          <h1 class="title">TEST</h1>
                       </div>
                       <div class="video-title">
                          <h1 class="title"><a href="http://127.0.0.1/videos_list.php?url=<?=$next?>">NEXT</a></h1>
                       </div>
                    </div>
                </div>                                                                                              
            </div>  
</div>

</div>
</div>

</div>

<script type="text/javascript">
    // 二级导航 伸缩性
    $(".nav li").click(function(){
        if($(this).hasClass("nav-parent")){
            var liThis = $(".nav .nav-parent").index($(this));
            console.log(liThis);
            $(this).addClass('active').siblings().removeClass('active')
            var navChildThis = $(".nav-child-box .nav-child").eq(liThis);
            $(".nav-child-box .nav-child").css({'opacity':'0','height':'0','padding':'0'});
            navChildThis.css({'opacity':'1','height':'36px'});
            $(".v-type").addClass("v-type-down");
        }
        else{
            $(".nav-child-box .nav-child").css({'opacity':'0','height':'0','padding':'0'});
            $(".v-type").removeClass("v-type-down");

        };
    });
</script>
<div class="toolbar"><a href="javascript:scroll(0,0)" class="toolbar-item toolbar-item-top"></a></div>
<div style="display:none">

</div>
</body>
</html>
