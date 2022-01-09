from selenium import webdriver


def _create_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.headless = True
    return webdriver.Chrome(
        executable_path=r"D:\start\Aiogram\backend\chromedriver.exe",
        options=options
    )
