<?php
function AddProduct($params, $publicURLConfig)
{
    $url = "https://" . $publicURLConfig->url . "/api/" . $publicURLConfig->systemname . "/1.5/CommonUse/product?uid=" . $publicURLConfig->uid . "&userNo=" . $params->modifierUserNo;

    //The JSON data.
    $data = array(
        'prodID' => array($params->prodID),
        'prodName' => array($params->prodName),
        'unit' => array($params->unit),
        'remark' => array($params->remark),
        'creatorNo' => array($params->modifierUserNo),
        'modifierNo' => array($params->modifierUserNo)
    );
    return array($url, $data);
}

function PatchProduct($params, $publicURLConfig)
{
    $url = "https://" . $publicURLConfig->url . "/api/" . $publicURLConfig->systemname . "/1.5/CommonUse/product?uid=" . $publicURLConfig->uid . "&userNo=" . $params->modifierUserNo;

    //The JSON data.
    $data = array(
        'old_prodID' => array($params->prodID),
        'prodName' => array($params->prodName),
        'unit' => array($params->unit),
        'remark' => array($params->remark),
        'modifierNo' => array($params->modifierUserNo)
    );
    return array($url, $data);
}

function DeleteProduct($params, $publicURLConfig)
{
    $url = "https://" . $publicURLConfig->url . "/api/" . $publicURLConfig->systemname . "/1.5/CommonUse/product?uid=" . $publicURLConfig->uid . "&userNo=" . $params->modifierUserNo;

    //The JSON data.
    $data = array(
        'prodID' => array($params->prodID)
    );
    return array($url, $data);
}
