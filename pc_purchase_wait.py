from selenium.webdriver import ActionChains
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def get_track(distance):      # distance为传入的总距离
    # 移动轨迹
    track=[]
    # 当前位移
    current=0
    # 减速阈值
    mid=distance*4/5
    # 计算间隔
    t=0.2
    # 初速度
    v=170

    while current<distance:
        if current<mid:
            # 加速度为2
            a=4
        else:
            # 加速度为-2
            a=-3
        v0=v
        # 当前速度
        v=v0+a*t
        # 移动距离
        move=v0*t+1/2*a*t*t
        # 当前位移
        current+=move
        # 加入轨迹
        track.append(round(move))
    return track
def move_to_gap(slider,tracks):     # slider是要移动的滑块,tracks是要传入的移动轨迹
    ActionChains(driver).click_and_hold(slider).perform()
    for x in tracks:
        ActionChains(driver).move_by_offset(xoffset=x,yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(driver).release().perform()

# pc端购买流程ui自动化


if __name__ == '__main__':
    driver = webdriver.Chrome()
    # 不可删除，设置浏览器window.navigator.webdriver=undefined
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""",
    })
    driver.get("https://newmall-uat-site.ejoy365hk.com/pc/login")
    driver.implicitly_wait(20)
    driver.maximize_window()
    driver.find_element_by_xpath('//*[@id="pane-first"]/div/form/div[1]/div/div[1]/input').send_keys("18818229142")
    driver.find_element_by_xpath('//*[@id="pane-first"]/div/form/div[2]/div/div[1]/input').send_keys("mc123456")
    driver.find_element_by_xpath('//button//span[text()="登录"]').click()
    huakuai = driver.find_element_by_class_name('button')
    sleep(2)
    move_to_gap(huakuai,get_track(332))
    for i in range(1):
        i+=1
        driver.get("https://newmall-uat-site.ejoy365hk.com/pc/#/")
        driver.find_element_by_xpath('//input[@placeholder="雅诗兰黛"]').send_keys("直邮")
        driver.find_element_by_xpath('//button[text()="搜索"]').click()
        driver.find_element_by_xpath('//div//span[text()="大图"]').click()
        wait = WebDriverWait(driver,5)
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div/div/div/div[2]/div/div/div[4]/div[1]/div/div/div[1]'))).click()
        # driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[2]/div/div/div[4]/div[1]/div/div/div[1]').click()
        # driver.find_element_by_xpath('//button[contains(text(),"立即购买")]').click()
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH,'//button[contains(text(),"立即购买")]'))).click()
        driver.find_element_by_xpath('//button//span[contains(text(),"稍后上传")]').click()
        driver.find_element_by_xpath('//button[text()="提交订单"]').click()
    driver.quit()
