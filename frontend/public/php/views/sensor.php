<?php
function GetSensorLastData($params, $publicURLConfig)
{
    $url = "https://" . $publicURLConfig->url . "/api/" . $publicURLConfig->systemname . "/2.0/Sensor/SingleRow/Last/" . $params->sensorRawTable . "?uid=" . $publicURLConfig->uid . "&userNo=" . $params->userNo;
    return array($url);
}

function GetAllEnergyMeterSensorLastData($params, $publicURLConfig)
{
    $url = "https://" . $publicURLConfig->url . "/api/" . $publicURLConfig->systemname . "/1.0/Sensor/LastSingleRows/AllEnergyMeter?uid=" . $publicURLConfig->uid . "&userNo=" . $params->userNo;
    return array($url);
}
