import requests
from bs4 import BeautifulSoup

def get_movie_data(keyword):
    url = f"https://search.naver.com/search.naver?where=nexearch&query={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    movie_cards = soup.select('.item_list .item') or soup.select('._au_movie_list_content .item') or soup.select('.card_item')
    
    movie_results = []
    
    # print(f"검색어: {keyword} / 발견된 영화 개수: {len(movie_cards)}")

    for card in movie_cards:
        try:
            
            title_el = card.select_one('.title') or card.select_one('.name')
            if not title_el: continue
            title = title_el.text.strip()
            
            
            info_text = card.select_one('.info_txt') or card.select_one('.info_box')
            full_info = info_text.get_text(separator="|").strip() if info_text else ""
            
            rating_el = card.select_one('.num') or card.select_one('.rating')
            rating = rating_el.text.strip() if rating_el else "0.0"

            genre = card.find("div", class_="info").find_all("dd")[0].text

            cast = card.find("div", class_="data_box").find("div", class_="info").find_all("span")[0].text

            link = card.select_one('a')['href'] if card.select_one('a') else "#"
            img_el = card.select_one('img')
            img_url = img_el['src'] if img_el else ""


            
            card_data = {
                "title": title,
                "rating": rating,
                "cast": cast,
                "link": link,
                "img": img_url,
                "genre" : genre
            }
            
            
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