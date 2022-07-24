class AppConfiguration:
    update_check_on_startup: bool = True
    http_proxy: str = ""
    https_proxy: str = ""
    no_proxy: str = ""
    tls_verification: bool = True
    allow_redirects: bool = False
    timeout_in_secs: str = "10"
    print_server: str = "https://printrider.bettercallbots.com"
