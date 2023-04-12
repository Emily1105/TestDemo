import allure
import pytest
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestCeshiren:
    #冒烟测试，测试搜索功能
    #测试高级别的异常场景
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def teardown(self):
        self.driver.quit()

    @pytest.mark.parametrize('name',yaml.safe_load(open("./test.yml")))
    #通过yaml文件实现参数化，yaml文件包含6组数据,分别实现正向测试，搜索最小长度1，搜索不存在的数据，搜索特殊字符，搜索内容为空，搜索内容为空格
    def test_ceshiren(self,name):
        """
        测试步骤：
        1.打开网页https://ceshiren.com/
        2.点击首页搜索框
        3.点击高级搜索按钮
        4.搜索框输入内容
        5.点击搜索按钮
        6.断言搜索信息和预期结果一致
        :return:
        """
        #异常处理
        try:
           # 1.打开网页https://ceshiren.com/
            self.driver.get("https://ceshiren.com/")
           # 2.点击首页搜索框
            self.driver.find_element(By.ID,"search-button").click()
           # 3.点击高级搜索按钮
            self.driver.find_element(By.CSS_SELECTOR,".searching").click()
           # 4.搜索框输入内容
            self.driver.find_element(By.CSS_SELECTOR,".full-page-search").send_keys(name)
           # 5.点击搜索按钮
            self.driver.find_element(By.CSS_SELECTOR,".search-cta").click()
           # 6.断言搜索信息和预期结果一致
            ele = self.driver.find_element(By.CSS_SELECTOR,".topic-title")
            assert name in ele.text
        #发生异常执行截图
        except:
            pic = self.driver.save_screenshot(f"{name}.jpg")
            allure.attach(self.driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)

