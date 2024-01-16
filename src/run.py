import warnings
from selenium.webdriver.chrome.options import Options

from naver.info import Info
from namu.namu import NamuCrawler
from common.driver import Driver

warnings.filterwarnings('ignore')
options = Options()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
# options.add_argument("headless") ## 크롤링 창 보이게 하려면 주석 처리
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
        # info = Info(self.driver, 'data/webtoon/', 'info.csv')
        # info.get_webtoon_info()

        ## 화산귀환, 신의탑, 외모지상주의, 나이트런, 전지적 독자 시점, 재혼황후, 가비지타임, 내일, 삼국지톡, 놓지마 정신줄
        namu = NamuCrawler(self.driver, 'data/webtoon/', 'namu.csv')
        title_list = ["화산귀환", "신의 탑", "외모지상주의", "나이트런", "전지적 독자 시점", "재혼 황후", "가비지타임", "내일", "삼국지톡", "놓지마 정신줄 시즌3"]
        namu_list = [
            "https://namu.wiki/w/%ED%99%94%EC%82%B0%EA%B7%80%ED%99%98(%EC%9B%B9%ED%88%B0)",
            "https://namu.wiki/w/%EC%8B%A0%EC%9D%98%20%ED%83%91",
            "https://namu.wiki/w/%EC%99%B8%EB%AA%A8%EC%A7%80%EC%83%81%EC%A3%BC%EC%9D%98(%EC%9B%B9%ED%88%B0)",
            "https://namu.wiki/w/%EB%82%98%EC%9D%B4%ED%8A%B8%EB%9F%B0",
            "https://namu.wiki/w/%EC%A0%84%EC%A7%80%EC%A0%81%20%EB%8F%85%EC%9E%90%20%EC%8B%9C%EC%A0%90(%EC%9B%B9%ED%88%B0)",
            "https://namu.wiki/w/%EC%9E%AC%ED%98%BC%20%ED%99%A9%ED%9B%84(%EC%9B%B9%ED%88%B0)",
            "https://namu.wiki/w/%EA%B0%80%EB%B9%84%EC%A7%80%ED%83%80%EC%9E%84",
            "https://namu.wiki/w/%EB%82%B4%EC%9D%BC(%EC%9B%B9%ED%88%B0)",
            "https://namu.wiki/w/%EC%82%BC%EA%B5%AD%EC%A7%80%ED%86%A1",
            "https://namu.wiki/w/%EB%86%93%EC%A7%80%EB%A7%88%20%EC%A0%95%EC%8B%A0%EC%A4%84"
        ]
        namu.save_csv(title_list, namu_list)

if __name__ == '__main__':
    run = Run()
    run.run()