import requests
from bs4 import BeautifulSoup
import copy

class Express_bus_list(object):

    '''
    출발지 코드와 도착지 코드, 조회 날짜 세가지 인자를 받아 고속버스 데이터를 수집
    사용 방법 : Bus_list 객체를 생성하면 해당 날짜의 버스 데이터를 자동으로 담아줌
    데이터 확인 : show 함수 이용

    주요 코드
    '010' : '서울경부'
    '020' : '센트럴시티(서울)'
    '500' : '광주(유·스퀘어)'
    '700' : '부산'
    '703' : '부산사상'
    '032' : '동서울'
    '300' : '대전복합'
    '602' : '전주'
    '360' : '유성'
    '310' : '천안'
    '801' : '동대구'
    '''

    def __init__(self, date='20200125', depcode='032', arvcode='300'):
        self.bus_list = []  # 버스 정보를 담을 리스트
        self.bus = self.Bus()  # 버스 객체
        self.search_date = date  # 조회 날짜
        self.depcode = depcode  # 출발지 코드
        self.arvcode = arvcode  # 도착지 코드

        self.data()  # 크롤링 및 파싱 수행

    def data(self):  # 파싱된 데이터를 이용해 버스 객체에 담은 뒤 배열에 넣어주는 함수
        bus_info = self.search_bus()  # 파싱을 마친 데이터

        for index, value in enumerate(bus_info):  # 데이터를 객체에 담아주는 반복문
            if index < 3:  # 필요없는 데이터는 건너뜀
                continue

            if index % 4 == 3:
                self.bus.dep_time = str(value.text)
            elif index % 4 == 0:
                self.bus.pride = str(value.text)
            elif index % 4 == 1:
                self.bus.company = str(value.text)
            elif index % 4 == 2:
                self.bus.seats = str(value.text)
                self.bus_list.append(copy.copy(self.bus))  # 주소값을 바꿔주기위해 얕은 복사를 함

    def show(self):  # 담긴 정보를 확인하기 위한 함수
        for i in self.bus_list:
            print(i.__dict__)


    def search_bus(self):  # 출발지와 도착지로 크롤링을 해주는 함수
        try:
            with requests.Session() as s:
                URL = 'https://www.kobus.co.kr/mrs/alcnSrch.do'

                data = {'deprCd': self.depcode,  # 출발치 코드
                        'arvlCd': self.arvcode,  # 도착지 코드
                        'pathDvs': 'sngl',
                        'pathStep': '1',
                        'pathStepRtn': '1',
                        'deprDtm': self.search_date,  # 서치 날짜
                        'busClsCd': '0',
                        }

                response = s.post(URL, data)  # 크롤링해온 통짜 데이터
                bus_info = self.parser(response.text)  # 통짜 데이터를 파싱하기위해 넘긴다

                return bus_info  # 파싱이 완료된 최종 데이터를 리턴한다
        except:
            raise ('fail')

    def parser(self, response):  # 크롤링한 통짜 데이터를 받아와서 필요한 정보만 파싱하는 함수
        parser = BeautifulSoup(response, 'html.parser')  # 뷰티풀숲을 이용해 파싱
        bus_info = parser.findAll('span', {'class': {'start_time',
                                                     'bus_com',
                                                     'grade_mo',
                                                     'remain'}})  # 버스의 유효한 정보만 가져온다
        return bus_info  # 파싱한 데이터를 넘겨준다

    class Bus(object):  # 리스트에 저장할 버스 객체
        def __init__(self):  # 초기 버스 상태
            self.dep_time = None  # 버스 출발 시간
            self.company = None  # 버스 회사명
            self.pride = None  # 버스 프라이드(우등같은거)
            self.seats = None  # 잔여좌석


if __name__ == '__main__':
    express_bus_list = Express_bus_list('20191230', '032', '300')  # 버스 조회
    print(express_bus_list.__doc__)  # 사용법
    express_bus_list.show()  # 확인