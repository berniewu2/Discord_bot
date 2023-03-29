from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


options = Options()
options.headless = True


def screenshot(champion, role, probuild = False):

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(f'https://www.op.gg/champions/{champion}/{role}/build?region=global&tier=platinum_plus')
    sleep(1)
    
    if probuild:
        driver.get(f'https://probuildstats.com/champion/{champion}?league=lpl&role={role}')
        sleep(1)

    if not probuild:
        driver.execute_script("window.scrollTo(0,200)")

    driver.set_window_size(1200,1500) # May need manual adjustment(w,h)                                                                                                                
    driver.save_screenshot("screenshot.png")
    driver.quit()
    print("end...")
    return
