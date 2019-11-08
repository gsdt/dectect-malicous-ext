const SERVER_IP_C = "203.162.10.102"
const api_endpoint_C = `http://${SERVER_IP_C}/api/`

let userName = document.getElementById('username');
let userEmail = document.getElementById('email');

let userComment = document.getElementById('comment');
let urlReport = document.getElementById('urlReport');

var urlCon = ""
const key = 'confirmReport.html?url='

chrome.storage.sync.get(["current_url", "statkeyus"], function (items) {
    var curentUrl = document.URL

    var res = curentUrl.match(/(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)?/g);
    if (res) {
        console.log(res)
        hi = String(res)
        var cache_url = hi.replace(key, '');
    } else {
        alert('WhOOPS ! Some err, sorry, pls refrest your page')
    }
    urlCon = cache_url
    var default_content = "(loading...)"
    urlReport.innerHTML = "     " + (cache_url || default_content);
});

document.getElementById("submit").addEventListener("click", (event) => {
    let userChoice = document.getElementsByName('choice');
    console.log(userChoice)
    let flag = 2
    if (userName.value === '') {
        flag = 1
        document.getElementById("aler1").style.visibility = "visible";
    } else {
        document.getElementById("aler1").style.visibility = "hidden";
    }
    if (userEmail.value === '') {
        flag = 1
        document.getElementById("aler2").style.visibility = "visible";
    } else {
        document.getElementById("aler2").style.visibility = "hidden";
    }

    if (flag === 2) {
        let cf = 0
        for (var i = 0; i < userChoice.length; i++) {
            if (userChoice[i].checked) {
                cf = userChoice[i].value
                break;
            }
        }
        data = {
            user_email: userEmail.value,
            url_report: urlCon,
            label: cf,
            user_name: userName.value,
            content_report: userComment.value,
        }

        response = $.post( api_endpoint_C + "report", data).done(o => {
            alert(o.result.status);
        });
    }
    urlReport.value = ""
})