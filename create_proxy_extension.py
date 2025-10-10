"""
Tworzy rozszerzenie Chrome dla proxy z autentykacją
Chrome nie wspiera proxy auth w URL, więc musimy użyć rozszerzenia
"""

import os
import zipfile
import string
import random

def create_proxy_extension(proxy_host, proxy_port, proxy_user, proxy_pass, extension_dir='proxy_extension'):
    """Tworzy rozszerzenie Chrome dla proxy z autentykacją"""
    
    manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

    background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
          },
          bypassList: ["localhost"]
        }
      };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (proxy_host, proxy_port, proxy_user, proxy_pass)

    # Utwórz katalog
    if not os.path.exists(extension_dir):
        os.makedirs(extension_dir)
    
    # Zapisz pliki
    manifest_path = os.path.join(extension_dir, 'manifest.json')
    background_path = os.path.join(extension_dir, 'background.js')
    
    with open(manifest_path, 'w') as f:
        f.write(manifest_json)
    
    with open(background_path, 'w') as f:
        f.write(background_js)
    
    return extension_dir


if __name__ == "__main__":
    # Test
    ext_dir = create_proxy_extension(
        "x340.fxdx.in",
        "13206",
        "softedgedtrailhead104154",
        "jIhUckJtAOt9"
    )
    print(f"Proxy extension created in: {ext_dir}")

