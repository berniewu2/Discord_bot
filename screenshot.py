from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.chrome.options import Options


options = Options()
options.headless = True


def screenshot(champion, role):

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(f'https://www.op.gg/champions/{champion}/{role}/build?region=global&tier=platinum_plus')

    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.execute_script("window.scrollTo(0,200)")
    driver.set_window_size(1200,1500) # May need manual adjustment(w,h)                                                                                                                
    driver.save_screenshot("screenshot.png")
    driver.quit()
    print("end...")
    return
