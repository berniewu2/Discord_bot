from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


options = Options()
options.headless = True


def screenshot_name(name):

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get(f'https://www.op.gg/summoners/na/{name}')

    driver.execute_script("window.scrollTo(0,200)")

    driver.set_window_size(1200,1500) # May need manual adjustment(w,h)                                                                                                                
    driver.save_screenshot("screenshot.png")
    driver.quit()
    print("end...")
    return


def screenshot(champion, role):

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get(f'https://www.op.gg/champions/{champion}/{role}/build?region=global&tier=platinum_plus')


    driver.execute_script("window.scrollTo(0,200)")

    driver.set_window_size(1200,1500) # May need manual adjustment(w,h)                                                                                                                
    driver.save_screenshot("screenshot.png")
    driver.quit()
    print("end...")
    return

def screenshot_pro(champion, role, lpl):

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    if lpl:
        driver.get(f'https://probuildstats.com/champion/{champion}?league=lpl&role={role}')
    else:
        driver.get(f'https://probuildstats.com/champion/{champion}?role={role}')

    driver.set_window_size(1200,1500) # May need manual adjustment(w,h)                                                                                                                
    driver.save_screenshot("screenshot.png")
    driver.quit()
    print("end...")
    return
