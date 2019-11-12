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

document.getElementById("Redirect").onclick = function () {
    console.log(urlCon)
    var curentUrl = document.URL

    var res = curentUrl.match(/(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)?/g);
    if (res) {
        console.log(res)
        hi = String(res)
        var cache_url = hi.replace(key, '');
    } else {
        alert('WhOOPS ! Some err, sorry, pls refrest your page')
    }

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