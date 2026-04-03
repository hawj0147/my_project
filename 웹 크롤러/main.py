import requests
from bs4 import BeautifulSoup

def get_movie_data(keyword):
    url = f"https://search.naver.com/search.naver?where=nexearch&query={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 1. 영화 정보들을 담고 있는 리스트 아이템을 찾습니다. 
    # (최신 네이버 영화 검색 결과의 공통 클래스인 ._au_movie_list_content 등을 타겟팅)
    movie_cards = soup.select('.item_list .item') or soup.select('._au_movie_list_content .item') or soup.select('.card_item')
    
    movie_results = []
    
    # 디버깅용: 검색된 카드 개수를 터미널에 출력합니다.
    print(f"검색어: {keyword} / 발견된 영화 개수: {len(movie_cards)}")

    for card in movie_cards:
        try:
            # 제목 추출
            title_el = card.select_one('.title') or card.select_one('.name')
            if not title_el: continue
            title = title_el.text.strip()
            
            # 상세 정보 (평점, 개봉일, 출연진 등)
            # 네이버는 .info_txt 클래스 안에 <span>이나 <dl>로 정보를 넣습니다.
            info_text = card.select_one('.info_txt') or card.select_one('.info_box')
            full_info = info_text.get_text(separator="|").strip() if info_text else ""
            
            rating_el = card.select_one('.num') or card.select_one('.rating')
            rating = rating_el.text.strip() if rating_el else "0.0"

            # 링크 및 이미지
            link = card.select_one('a')['href'] if card.select_one('a') else "#"
            img_el = card.select_one('img')
            img_url = img_el['src'] if img_el else ""

            # HTML(search.html)에서 사용하는 변수명과 100% 일치시킵니다.
            card_data = {
                "title": title,
                "rating": rating,
                "open_date": "상세정보 확인", # 정보 위치가 유동적이라 기본값 설정
                "cast": "상세정보 확인",
                "link": link,
                "img": img_url
            }
            
            # 정보 텍스트 분석해서 개봉일과 출연진 추출 시도
            info_parts = full_info.split('|')
            for part in info_parts:
                if "개봉" in part:
                    card_data["open_date"] = part.replace("개봉", "").strip()
                if "출연" in part:
                    card_data["cast"] = part.replace("출연", "").strip()

            movie_results.append(card_data)
            
        except Exception as e:
            print(f"개별 카드 파싱 에러: {e}")
            continue
            
    return movie_results