const SERVER_IP = "203.162.10.102"
const api_endpoint = `http://${SERVER_IP}/api/check`

const webRequestFlags = [
  'blocking',
];

function checkStorage(current_url) {
  console.log("================================= 2")
  return new Promise(resolve => {
    setTimeout(() => {
      chrome.storage.sync.get(['storagekey'], function (result) {
        console.log("================================= 2 - 1")
        data = result.storagekey
        if (data) {
          console.log("================================= 2 - 2")
          console.log(data)
          if (data.includes(current_url)) {
            console.log("================================= 2 - 3")
            resolve('false');
          } else {
            console.log("================================= 2 - 4 - 1")
            resolve('true');
          }
        } else {
          console.log("================================= 2 - 4 - 2")
          resolve('true');
        }
      });
    }, 200);
  });
}

function checkDB(tabId, current_url, tab) {
  if (current_url) {
    if (current_url.indexOf("chrome-extension://") === 0) {
      return
    }
    if (current_url.indexOf(SERVER_IP) >= 0) {
      console.log("fire up localhost")
      return
    }
    response = $.post(api_endpoint, {
      url: current_url
    }).done(o => {
      console.log(o.result)
      if (o.result.label == "1") {
        chrome.tabs.update({
          url: chrome.extension.getURL('blocked.html') + '?a=b&url=' + current_url + '&type=' + o.result.source
        });
      }
    });
  }
}

function checkCon(current_url) {
  return new Promise(resolve => {
    setTimeout(() => {
      chrome.storage.sync.get(['saveCache'], function (result) {

        if (result === null) {
          result = [];
        }

        var array = result['saveCache'] ? result['saveCache'] : [];
        array.unshift(current_url);

        var jsonObj = {};
        jsonObj['saveCache'] = array;
        console.log(array)
        chrome.storage.sync.set(jsonObj, function () {
          console.log("DA THEM")
          resolve('true');
        });
      });
    }, 200);
  });
}


async function process(tabId, changeInfo, tab) {
  var current_url = changeInfo.url;

  var array = []
  if (current_url) {

    var msg0 = await checkCon(current_url);
    console.log("================================= 1")
    var msg1 = await checkStorage(current_url);
    if (msg1 === 'true') {
      console.log("================================= 3")
      var msg = await checkDB(tabId, current_url, tab);
    }
  }
  console.log(tab)
}

chrome.tabs.onUpdated.addListener(process);
