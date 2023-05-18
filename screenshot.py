from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


options = Options()
options.headless = True


def screenshot_name(name:str):

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get(f'https://www.op.gg/summoners/na/{name}')

    driver.execute_script("window.scrollTo(0,200)")

    driver.set_window_size(1200,1500) # May need manual adjustment(w,h)                                                                                                                
    driver.save_screenshot("screenshot.png")
    driver.quit()
    print("end...")
    return


def screenshot(champion:str, role:str):

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get(f'https://www.op.gg/champions/{champion}/{role}/build?region=global&tier=platinum_plus')


    driver.execute_script("window.scrollTo(0,200)")

    driver.set_window_size(1200,1500) # May need manual adjustment(w,h)                                                                                                                
    driver.save_screenshot("screenshot.png")
    driver.quit()
    print("end...")
    return

def screenshot_pro(champion:str, role:str, lpl):

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


def screenshot_anime(name:str):

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    anime = '%20'.join(name)
    driver.get(f'https://animecountdown.com/search?q={anime}')
    driver.set_window_size(1200,1500) # May need manual adjustment(w,h)	

    action = ActionChains(driver)
    action.move_by_offset(95,760)

    action.click().perform()                
    driver.execute_script("window.scrollTo(0,400)")                                                                                                
    driver.save_screenshot("screenshot.png")
    driver.quit()

    print("end...")
    return
