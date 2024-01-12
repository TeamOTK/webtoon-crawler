from naver.info import Info

class Run():
    def __init__(self):
        pass

    def run(self):
        info = Info('data/webtoon/', 'info.csv')
        info.get_webtoon_info()
        

if __name__ == '__main__':
    run = Run()
    run.run()