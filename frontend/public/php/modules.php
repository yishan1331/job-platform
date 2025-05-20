<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
date_default_timezone_set("Asia/Taipei");
$postBody = file_get_contents("php://input");
$postBody = json_decode($postBody);
$methods = $postBody->methods;
$token = $_SERVER['HTTP_AUTHORIZATION'];
$whichFunction = $postBody->whichFunction;

include("./globalvar.php");
include("./views/accountAction.php");
include("./views/common.php");
include("./views/product.php");
include("./views/sensor.php");

$useCURL = true;
$DEBUG = isset($postBody->DEBUG) ? $postBody->DEBUG : false;

$postdata = $whichFunction($postBody, $publicURLConfig);
$response = array(
    "status"=> 200,
    "data"=>array(
        "Response"=> "ok"
    ),
);
if ($methods == "NOAPI") {
    // echo json_encode($postdata);
} else {
    if ($useCURL) {
        $ch = curl_init();

        if ($DEBUG) {
            // 打印 URL 进行检查
            echo "请求 URL: " . $postdata[0] . "\n";
        }

        // 设置 cURL 选项
        curl_setopt($ch, CURLOPT_URL, $postdata[0]); // 设置请求的 URL
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $methods); // 设置请求方法
        if ($methods != "GET"){
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($postdata[1])); // 设置请求体内容
        }

        curl_setopt($ch, CURLOPT_HTTPHEADER, array(
            'Content-Type: application/json',
            'Accept: application/json',
            'Authorization: '. $token,
            'X-Client-IP: '. $clientIP,
            'X-Client-PORT: '. $clientPort
        )); // 设置请求头

        // 忽略 SSL 验证（不推荐在生产环境中使用）
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);

        // 设置返回结果以字符串形式返回，而不是直接输出
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        if ($DEBUG) {
            // 启用详细输出
            curl_setopt($ch, CURLOPT_VERBOSE, true);
            $verbose = fopen('php://temp', 'w+');
            curl_setopt($ch, CURLOPT_STDERR, $verbose);
        }

        // 执行 cURL 请求并获取响应
        $result = curl_exec($ch);

        // 检查是否有错误发生
        if ($result === false) {
            $response['status'] = curl_errno($ch);
            $response['data'] = curl_error($ch);
            echo "cURL 錯誤: " . curl_error($ch) . "\n";
        } else {
            // 获取响应的 HTTP 状态码
            $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
            $response['status'] = $http_code;
            $response['data'] = json_decode($result, true);
        }

        if ($DEBUG) {
            // 输出详细信息
            rewind($verbose);
            $verboseLog = stream_get_contents($verbose);
            echo "详细日志:\n", htmlspecialchars($verboseLog), "\n";
        }

        // 关闭 cURL 资源
        curl_close($ch);

        echo json_encode($response);
    } else {
        if ($methods == "GET") {
            // $getfunction = new FunctionGetClass;
            // $postdata = $getfunction->$whichFunction($postBody,$returnData);
            $options = array(
                "ssl" => array(
                    "verify_peer" => false,
                    "verify_peer_name" => false,
                ),
            );
        } else {
            // $postfunction = new FunctionPostClass;
            // $postdata = $postfunction->$whichFunction($postBody,$returnData);
            $options = array(
                'http' => array(
                    'method' => $methods,
                    'content' => json_encode($postdata[1]),
                    'header' => "Content-Type: application/json\r\n" .
                        "Accept: application/json\r\n"
                ),
                "ssl" => array(
                    "verify_peer" => false,
                    "verify_peer_name" => false,
                ),
            );
        }
        try {
            $context = stream_context_create($options);
            $result = file_get_contents($postdata[0], false, $context);

            preg_match('/([0-9])\d+/',$http_response_header[0],$matches);
            $responsecode = intval($matches[0]);

            // 這樣會抓不到api回傳的錯誤訊息，只知道status_code
            // 檢查資料是否獲取成功
            if ($result === false) {
                $http_code = $http_response_header[0];
                // 取得失敗，檢查是否是 HTTP 錯誤
                if (strpos($http_code, '403') !== false) {
                    // 处理 403 Forbidden 错误
                    $response['status'] = 403;
                    throw new Exception('HTTP 403 Forbidden 錯誤：無法存取遠端伺服器。');
                } else {
                    // 其他类型的 HTTP 错误，或者网络连接错误
                    throw new Exception('發生了其他類型的錯誤。');
                }
            }
            $Arr = json_decode($result, true);
            $response['status'] = $responsecode;
            $response['data'] = $Arr;
        } catch (Exception | HttpException $e) {
            $response['data']['Response'] = $e->getMessage();
        } finally {
            echo json_encode($response);
        }
    }
}
