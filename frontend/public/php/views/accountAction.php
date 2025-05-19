<?php
//登入
function Login($params, $publicURLConfig)
{
    $url = "https://" . $publicURLConfig->url . "/api/" . $publicURLConfig->systemname . "/1.0/user/login?uid=" . $publicURLConfig->uid . "&userID=" . $params->userID . "&pwd=" . $params->pwd;
    return array($url);
}
function Logout($params, $publicURLConfig)
{
    $url = "https://" . $publicURLConfig->url . "/api/" . $publicURLConfig->systemname . "/1.0/user/logout?uid=" . $publicURLConfig->uid . "&userNo=" . $params->userNo . "&userID=" . $params->userID;
    return array($url);
}

function AddUser($params, $publicURLConfig)
{
    $url = "https://" . $publicURLConfig->url . "/api/" . $publicURLConfig->systemname . "/1.0/user?uid=" . $publicURLConfig->uid . "&userNo=" . $params->modifierUserNo;
    //The JSON data.
    $data = array(
        'userID' => $params->userID,
        'userName' => $params->userName,
        'pwd' => $params->pwd,
        'email' => $params->email,
        'levelNo' => $params->levelNo,
        'remark' => $params->remark
    );
    return array($url, $data);
}

function PatchUser($params, $publicURLConfig)
{
    $url = "https://" . $publicURLConfig->url . "/api/" . $publicURLConfig->systemname . "/1.0/user/" . $params->userNo . "?uid=" . $publicURLConfig->uid . "&userNo=" . $params->modifierUserNo;
    //The JSON data.
    $data = array(
        'userID' => $params->userID,
        'userName' => $params->userName,
        'pwd' => $params->pwd,
        'email' => $params->email,
        'levelNo' => $params->levelNo,
        'remark' => $params->remark
    );
    return array($url, $data);
}

function DeleteUser($params, $publicURLConfig)
{
    $url = "https://" . $publicURLConfig->url . "/api/" . $publicURLConfig->systemname . "/1.0/user/" . $params->userNo . "?uid=" . $publicURLConfig->uid . "&userNo=" . $params->modifierUserNo;
    return array($url, $data);
}

function AddPermission($params, $publicURLConfig)
{
    $url = "https://" . $publicURLConfig->url . "/api/" . $publicURLConfig->systemname . "/1.0/accessPermission?uid=" . $publicURLConfig->uid . "&userNo=" . $params->modifierUserNo;
    //The JSON data.
    $data = array(
        'levelName' => $params->levelName,
        'levelInfo' => $params->levelInfo,
        'remark' => $params->remark,
        'accessList' => $params->accessList
    );
    return array($url, $data);
}

function PatchPermission($params, $publicURLConfig)
{
    $url = "https://" . $publicURLConfig->url . "/api/" . $publicURLConfig->systemname . "/1.0/accessPermission/" . $params->levelNo . "?uid=" . $publicURLConfig->uid . "&userNo=" . $params->modifierUserNo;
    //The JSON data.
    $data = array(
        'levelName' => $params->levelName,
        'levelInfo' => $params->levelInfo,
        'remark' => $params->remark,
        'accessList' => $params->accessList
    );
    return array($url, $data);
}

function DeletePermission($params, $publicURLConfig)
{
    $url = "https://" . $publicURLConfig->url . "/api/" . $publicURLConfig->systemname . "/1.0/accessPermission/" . $params->levelNo . "?uid=" . $publicURLConfig->uid . "&userNo=" . $params->modifierUserNo;
    return array($url, $data);
}
