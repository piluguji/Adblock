// Define the URL list globally
var url_list = [];

// Fetch and parse the URL list when the extension is installed
chrome.runtime.onInstalled.addListener(async () => {
    const res = await fetch("https://easylist.to/easylist/easylist.txt");
    const record = await res.text();
    
    var lines = record.split('\n');
    for (var i = 1; i < lines.length; i++) {
        var line = lines[i];

        if ('||' == line.substring(0, 2) && line.indexOf('^') != -1 && line.indexOf('*') == -1) {
            var last_index = line.indexOf('^');
            var url = '*://*.' + line.substring(2, last_index) + '/*';
            url_list.push(url);
        }
    }
});

if (url_list.length === 0) {
    await setupWebRequestListener();
}else{
    chrome.webRequest.onBeforeRequest.addListener(
        function (details) {
            console.log("on");
            if (extension_status == "on") {
                return { cancel: true };
            } else {
                return { cancel: false };
            }
        },
        { urls: url_list },
        ["blocking"]
    );
}