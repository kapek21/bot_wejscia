// Proxy configuration for orange1 device (SOCKS5)
var config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "socks5",
            host: "x428.fxdx.in",
            port: parseInt(13350)
          },
          bypassList: ["localhost"]
        }
      };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "karol1234567",
            password: "Karol1234567"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
