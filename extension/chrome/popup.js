let OnAction = document.getElementById('OnAction');
let webCurrent = document.getElementById("urlCurrent");
// let webStatus = document.getElementById("webStatus");
let excludeUrl = document.getElementById("excludeUrl");
let reportUrl = document.getElementById("reportUrl");
let detectUrlBy = document.getElementById("detectBy");
let url = ""
let deleteUrlExclude = document.getElementById("DeleteUrlExclude");

const SERVER_IP_C = "203.162.10.102"
const api_endpoint_C = `http://${SERVER_IP_C}/api/`

chrome.tabs.query({
    'active': true,
    'lastFocusedWindow': true
}, function (tabs) {
    tab = tabs[0];
    url = new URL(tab.url)
    domain = url.hostname
});

chrome.storage.sync.get(["current_url", "statkeyus"], function (items) {
    var default_content = "(loading...)"
    webCurrent.innerHTML = "     " + (domain || default_content);
    detectUrlBy.innerHTML = "     " + (items["AI"] || "Database");
    // show dectec by ...
});

// Save and send data
document.getElementById("OnActionReport2").onclick = function () {
    chrome.tabs.reload(tab.id);
}

document.getElementById("OnActionExclude").addEventListener("click", (event) => {

    var userExcludeUrl = excludeUrl.value;
    if (userExcludeUrl == "") {
        return;
    }

    chrome.storage.sync.get(['storagekey'], function (result) {
        if (result === null) {
            result = [];
        }
        var array = result['storagekey'] ? result['storagekey'] : [];
        array.unshift(userExcludeUrl);

        var jsonObj = {};
        jsonObj['storagekey'] = array;
        chrome.storage.sync.set(jsonObj, function () {
            alert("thanh cong")
        });
    });

    response = $.post(api_endpoint_C + "exclude", {
        user_id: "192.168.0.0",
        url_exclude: userExcludeUrl,
        label: "1"
    }).done(o => {
        console.log(o);
        excludeUrl.value = ""
    });
})

document.getElementById("OnActionReport").addEventListener("click", (event) => {
    if (reportUrl.value !== '') {
        chrome.tabs.update({
            url: chrome.extension.getURL('confirmReport.html') + '?url=' + reportUrl.value
        });
    } else {
        alert('Nhap URL report !!!')
    }
})

document.getElementById("OnActionDelete").addEventListener("click", (event) => {
    var userDeleteUrlExclude = deleteUrlExclude.value;
    if (userDeleteUrlExclude == "") {
        return;
    }

    chrome.storage.sync.get(['storagekey'], function (result) {
        if (result === null) {
            result = [];
        }
        var theList = result['storagekey'] ? result['storagekey'] : [];
        console.log("deleteUrlExclude " + userDeleteUrlExclude)
        // Checks if the url that will be deleted is in the array:
        console.log(theList.includes(userDeleteUrlExclude))
        if (theList.includes(userDeleteUrlExclude)) {
            console.log("HHHHHH")
            // create a new array without url
            var newUrlList = theList.filter(function (item) {
                return item !== userDeleteUrlExclude;
            });
            console.log("delete  " + newUrlList)
            var jsonObj = {};
            jsonObj['storagekey'] = newUrlList;
            // set new url list to the storage
            chrome.storage.sync.set(jsonObj, function () {
                // alert("Delete url exclude thanh cong")
            });
            deleteUrlExclude.value = ""
            alert("Delete url exclude thanh cong")
            chrome.runtime.reload();
        } else {
            deleteUrlExclude.value = ""
            alert("The url not exclude")
        }
    });
})


var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-91844630-4']);
_gaq.push(['_trackPageview']);

(function() {
  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
  ga.src = 'https://ssl.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();