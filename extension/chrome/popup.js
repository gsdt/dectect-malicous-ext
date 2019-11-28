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

document.getElementById("OnActionReport").addEventListener("click", (event) => {
    if (reportUrl.value !== '') {
        chrome.tabs.update({
            url: chrome.extension.getURL('reportUrlPage/reportPage.html') + '?url=' + reportUrl.value
        });
    } else {
        alert('Nhap URL report !!!')
    }
})

document.getElementById("OnActionDelete").addEventListener("click", (event) => {
    chrome.tabs.update({
        url: chrome.extension.getURL('exclude.html')
    });
})
