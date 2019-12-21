class AppConfiguration:
    update_check_on_startup: bool = True
    http_proxy: str = ""
    https_proxy: str = ""
    tls_verification: bool = True
    timeout_in_secs: str = "10"
    print_server: str = "http://localhost:8080"
