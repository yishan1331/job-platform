<?php
//https://blog.csdn.net/leedaning/article/details/72781734
if (filter_var($_SERVER['HTTP_HOST'], FILTER_VALIDATE_IP)) {
    $publicIP = $_SERVER['HTTP_HOST'];
} else {
    # for dev testing
    $publicIP = "localhost";
}

$publicSystemName = "CDCP";
$publicUID = "@CDCP@PaaS";

$publicURLConfig = new stdClass();
$publicURLConfig->url = $publicIP.":3687";
$publicURLConfig->systemname = $publicSystemName;
$publicURLConfig->uid = $publicUID;

if (!empty($_SERVER["HTTP_CLIENT_IP"])){
    $clientIP = $_SERVER["HTTP_CLIENT_IP"];
}elseif(!empty($_SERVER["HTTP_X_FORWARDED_FOR"])){
    $clientIP = $_SERVER["HTTP_X_FORWARDED_FOR"];
}else{
    $clientIP = $_SERVER["REMOTE_ADDR"];
}
$clientPort = $_SERVER['REMOTE_PORT'];
