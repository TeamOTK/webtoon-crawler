import warnings
from selenium.webdriver.chrome.options import Options

from naver.info import Info
from common.driver import Driver

warnings.filterwarnings('ignore')
options = Options()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("headless") ## 크롤링 창 보이게 하려면 주석 처리
options.add_argument('--window-size=1920, 1080')
options.add_argument('--no-sandbox')
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--start-maximized') 
options.add_argument('--start-fullscreen') ## 전체 화면 없애려면 주석 처리
options.add_argument('--disable-blink-features=AutomationControlled')

class Run():
    def __init__(self):
        # Driver 하나로 사용
        self.driver = Driver().set_driver(options)

    def run(self):
        info = Info(self.driver, 'data/webtoon/', 'info.csv')
        info.get_webtoon_info()
        

if __name__ == '__main__':
    run = Run()
    run.run()