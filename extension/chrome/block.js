const SERVER_IP = "203.162.10.102"
const api_endpoint = `http://${SERVER_IP}/api/add`

var urlCon = ""
const key = 'blocked.html?url='
chrome.storage.sync.get(['saveCache'], function (result) {
    data = result.saveCache
    if (result === null) {
        console.log("VL")
        result = [];
    } else {
        console.log("Client   " + data[0])
        urlCon = data[0]
    }
});

document.getElementById("WhiteList").onclick = function () {
    var params = new URLSearchParams(window.location.href);
    const current_url = params.get('url');
    response = $.post(api_endpoint, {
        url: current_url,
        label: 0
    }).done(o => {
        console.log(o.result)
    });
    window.location.href = current_url
}

document.getElementById("Redirect").onclick = function () {
    var params = new URLSearchParams(window.location.href);
    const cache_url = params.get('url');

    chrome.storage.sync.get(['storagekey'], function (result) {
        if (result === null) {
            result = [];
        }
        var array = result['storagekey'] ? result['storagekey'] : [];
        array.push(cache_url);

        var jsonObj = {};
        jsonObj['storagekey'] = array;
        chrome.storage.sync.set(jsonObj, function () {
            alert("Exclude Url thanh cong")
            window.location.href = cache_url;
        });
    });
}

document.getElementById("CloseTab").onclick = function () {
    window.close();
}
window.onload = function () {
    console.log('Processing detect type')
    var params = new URLSearchParams(window.location.href);
    const type = params.get('type');
    console.log(type)
    if (type == 'database') {
        console.log('inner database')
        document.getElementById('type').innerHTML = 'database';
    }
    else {
        document.getElementById('type').innerHTML = 'machine learning';
    }
}