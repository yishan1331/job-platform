<?php
function CommonPaginationQuery($params, $publicURLConfig)
{
    $baseUrl = "https://" . $publicURLConfig->url . "/api/" . $publicURLConfig->systemname . "/1.0/CommonUse/TableData/Pagination/" . $params->table;

    $queryParams = [
        'uid' => $publicURLConfig->uid,
        'page' => isset($params->page) ? (int)$params->page : 1,
        'perPage' => isset($params->perPage) ? (int)$params->perPage : 20,
        'userNo' => isset($params->userNo) ? $params->userNo : ''
    ];
    if (isset($params->getAll)) {
        $queryParams['getAll'] = $params->getAll;
    }
    if (isset($params->sortBy)) {
        $queryParams['sortBy'] = $params->sortBy;
    }
    if (isset($params->sortingOrder)) {
        $queryParams['sortingOrder'] = $params->sortingOrder;
    }

    if (!empty($params->attr)) {
        $queryParams['attr'] = $params->attr;
        $queryParams['attrValue'] = isset($params->attrValue) ? $params->attrValue : '';
        $queryParams['fuzzy'] = !empty($params->fuzzy) ? 'yes' : 'no';
    }

    $url = $baseUrl . '?' . http_build_query($queryParams, '', '&', PHP_QUERY_RFC3986);

    $url = str_replace(' ', '', $url);
    // echo($url . "\n");
    return array($url);
}

function CommonQueryAllData($params, $publicURLConfig)
{
    $url = "https://" . $publicURLConfig->url . "/api/" . $publicURLConfig->systemname . "/1.0/CommonUse/TableData?uid=" . $publicURLConfig->uid . "&table=" . $params->table;
    return array($url);
}
