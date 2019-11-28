function parseUri (str) {
	var	o   = parseUri.options,
		m   = o.parser[o.strictMode ? "strict" : "loose"].exec(str),
		uri = {},
		i   = 14;

	while (i--) uri[o.key[i]] = m[i] || "";

	uri[o.q.name] = {};
	uri[o.key[12]].replace(o.q.parser, function ($0, $1, $2) {
		if ($1) uri[o.q.name][$1] = $2;
	});

	return uri;
};

parseUri.options = {
	strictMode: false,
	key: ["source","protocol","authority","userInfo","user","password","host","port","relative","path","directory","file","query","anchor"],
	q:   {
		name:   "queryKey",
		parser: /(?:^|&)([^&=]*)=?([^&]*)/g
	},
	parser: {
		strict: /^(?:([^:\/?#]+):)?(?:\/\/((?:(([^:@]*)(?::([^:@]*))?)?@)?([^:\/?#]*)(?::(\d*))?))?((((?:[^?#\/]*\/)*)([^?#]*))(?:\?([^#]*))?(?:#(.*))?)/,
		loose:  /^(?:(?![^:@]+:[^:@\/]*@)([^:\/?#.]+):)?(?:\/\/)?((?:(([^:@]*)(?::([^:@]*))?)?@)?([^:\/?#]*)(?::(\d*))?)(((\/(?:[^?#](?![^?#\/]*\.[^?#\/.]+(?:[?#]|$)))*\/?)?([^?#\/]*))(?:\?([^#]*))?(?:#(.*))?)/
	}
};

// MAIN PROCESS HERE

window.onload = function () {
    chrome.storage.sync.get(['storagekey'], function (result) {
        if(!result) return;
        result.storagekey.forEach((url, id) => {
            domain = parseUri(url).host
            add_new_HTML_row(id, url, domain)
        });
    })
}

function add_new_HTML_row(id, url, domain) {
    $('.main-table').append(`
    <div class="row">
        <div class="cell no">${id+1}</div>
        <div class="cell url">${url}</div>
        <div class="cell domain">${domain}</div>
        <div class="cell remove" id="bt-${id}" value="${id}">Remove</div>
    </div>
    `)

    $(`#bt-${id}`).click(function(e) {
        var id = e.target.id.substring(3)
        id =  parseInt(id)
        remove_url(id)
    })
}

function remove_url(id) {
    chrome.storage.sync.get(['storagekey'], function (result) {
        if(!result) return;
        var url_list = result.storagekey;
        url_list = url_list.filter((value, idx) => {
            if(idx !== id) return value
        })
        var jsonObj = {};
        jsonObj['storagekey'] = url_list;
        chrome.storage.sync.set(jsonObj, function () {
            location.reload();
        });
    })
}





