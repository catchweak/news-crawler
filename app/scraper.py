from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.orm import sessionmaker
from .database import SessionLocal
from .models import Article
from . import site_repo, category_repo
from datetime import datetime
import requests
import urllib.request
from bs4 import BeautifulSoup

def scrap_url():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    sites = site_repo.get_sites()
    
    for site in sites:
        categories = category_repo.get_categories(site.id)

        for category in categories:
            if category.code == '250':
                target_url = site.base_url + '/'+ category.parent_code +'/'+ category.code # str(264) -> category.code
                print(target_url)

                try:
                    driver.get(target_url)
                    more_news_click(driver, category.id, site.id) # section이 category.id가 되면됨
                    print("All tasks completed. The browser will remain open.")
                except Exception as e:
                    print(f'An error occurred during the main execution: {e}')
            

def more_news_click(driver, category_id, site_id):
    """
    뉴스 더보기 클릭
    """
    while True:
        try:
            # 요소가 로드될 때까지 대기
            headline_tag = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='section_more']/a[not(contains(@style, 'display: none;'))]"))
            )

            # a 태그를 찾음
            a_tag = headline_tag.find_element(By.XPATH, "//div[@class='section_more']/a[not(contains(@style, 'display: none;'))]")

            # 요소가 상호작용 가능할 때까지 대기
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='section_more']/a[not(contains(@style, 'display: none;'))]"))
            )

            # 스크롤해서 요소가 화면에 표시되도록 함
            driver.execute_script("arguments[0].scrollIntoView(true);", a_tag)
            
            # JavaScript를 사용하여 클릭
            driver.execute_script("arguments[0].click();", a_tag)
            print("Clicked 'more news' button.")
        except Exception as e:
            get_detail_url(driver, category_id)
            print(f'Exception occurred: {e}')
            break

def get_detail_url(driver, category_id):
    """
    상세페이지 url 조사
    """

    news_url_tag = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="newsct"]/div[2]/div/div[1]/div/ul/li/div/div/div/a'))
    )
    news_url_tags = news_url_tag.find_elements(By.XPATH, '//*[@id="newsct"]/div[2]/div/div[1]/div/ul/li/div/div/div/a')

    # 각 링크 요소의 href 속성 값 가져와 출력
    for news_url_tag in news_url_tags:
        news_url = news_url_tag.get_attribute("href")
        save_to_db(news_url, category_id)

def save_to_db(news_url, category_id):
    """
    DB에 기사 데이터 저장
    """
    db = SessionLocal()
    try:
        article = Article(url=news_url, category_id=category_id)
        db.add(article)
        db.commit()
    except Exception as e:
        print(f"An error occurred while saving data to the database: {e}")
        db.rollback()
    finally:
        db.close()

def scrap_single_page(request_url):
    """
    한개의 url에 대하여 단일 크롤링
    """
    db = SessionLocal()
    try:
        articles = db.query(Article).filter(Article.url==request_url).all()

        for article in articles:
            update_article_content(article, db)
    finally:
        db.close()

def scrap_detail_page():
    """
    기사 상세 정보 크롤링
    """
    db = SessionLocal()
    try:
        # articles = db.query(Article).all()
        # articles = db.query(Article).limit(1).all()
        # articles = db.query(Article).filter(Article.headline.is_(None)).all()
        articles = db.query(Article).filter(Article.author.is_(None)).all()

        for article in articles:
            update_article_content(article, db)
    finally:
        db.close()

def update_article_content(article: Article, db):
    """
    기사 상세 정보 업데이트
    """
    article_url = article.url
    print("--------------")
    print("id : " + str(article.id))
    print("category_id : " + str(article.category_id))
    print("url : " + str(article.url))
    print("--------------")

    # BeautifulSoup를 사용하여 기사의 내용을 스크랩
    try:
        response = requests.get(article_url, allow_redirects=False)
        print("response code : " + str(response.status_code))
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # headline
            headline_tag = soup.find('h2', {'id':'title_area'})
            if headline_tag is not None:
                headline = headline_tag.find('span').text
                print('==========headline==========')
                print(headline)
                article.headline = headline

            # body
            dic_area_tag = soup.find('article', {'id':'dic_area'})
            if dic_area_tag is not None:
                print('==========body==========')
                print(dic_area_tag.text)
                article.body = dic_area_tag.text

                # summary
                media_end_summary_tag_list = dic_area_tag.findAll('strong')
                if media_end_summary_tag_list is not None and media_end_summary_tag_list != []:
                    media_end_summary_tag = dic_area_tag.findAll('strong')[0]
                    print(media_end_summary_tag)
                    print('==========summary==========')
                    print(media_end_summary_tag.text)
                    article.summary = media_end_summary_tag.text
                
                # image url
                image_url_tag = dic_area_tag.find('img', {'id': 'img1'})
                if image_url_tag is not None:
                    print('==========image url==========')
                    print(image_url_tag['data-src'])
                    article.img_url = image_url_tag['data-src']

            # origin url
            origin_article_url_tag = soup.find('a', {'class', 'media_end_head_origin_link'})
            if origin_article_url_tag is not None:
                print('==========origin_article_url_tag==========')
                print(origin_article_url_tag['href'])
                article.origin_url = origin_article_url_tag['href']

            # author
            author_tag = soup.find('em', {'class', 'media_end_head_journalist_name'})
            if author_tag is not None:
                print('==========author_tag==========')
                print(author_tag)
                print(author_tag.text)
                article.author = author_tag.text

            # create date
            created_at_tag = soup.find('span', {'class', 'media_end_head_info_datestamp_time _ARTICLE_DATE_TIME'})
            if created_at_tag is not None:
                print('==========created_at_tag==========')
                print(created_at_tag.text)
                article.article_created_at = created_at_tag.text

            # update date
            updated_at_tag = soup.find('span', {'class', 'media_end_head_info_datestamp_time _ARTICLE_MODIFY_DATE_TIME'})
            if updated_at_tag is not None:
                print('==========created_at_tag==========')
                print(created_at_tag.text)
                article.article_created_at = created_at_tag.text

            if updated_at_tag != None:
                print('==========updated_at_tag==========')
                article.article_updated_at = updated_at_tag.text

            # like count
            # like_count_tag = soup.find('span', {'class', 'u_likeit_text _count num'})
            # print('==========like_count_tag==========')
            # try:
            #     print(like_count_tag.text)
            # except:
            #     pass

            # comment count bs4로는 불가능

        elif response.status_code == 302:
            article.redirected_url = get_moved_page_url(article_url)

        # 기사 내용 업데이트 후 DB에 저장
        try:
            db.add(article)
            db.commit()
        except Exception as e:
            print(f"An error occurred while committing changes to the database: {e}")
            db.rollback()
    except Exception as e:
        print(f"An error occurred while updating article content: {e}")


def get_bsobj(url):
    """
    bs_obj를 리턴
    """
    html = urllib.request.urlopen(url)
    bs_obj = BeautifulSoup(html, "html.parser") # url에 해당하는 html이 bsObj에 들어감

    return bs_obj

def get_moved_page_url(start_url, max_redirects=10):
    """
    302응답을 내려주는 url들에 대하여 최종적으로 마지막 url을 return
    """
    current_url = start_url
    redirect_count = 0

    while redirect_count < max_redirects:
        response = requests.get(current_url, allow_redirects=False)
        if response.status_code in (301, 302):
            # Extract the Location header to get the new URL
            new_url = response.headers.get('Location')
            if not new_url:
                break
            
            # Handle relative URLs by joining with the current URL
            if not new_url.startswith('http'):
                from urllib.parse import urljoin
                new_url = urljoin(current_url, new_url)
            
            # Update current URL to the new URL and increment redirect count
            current_url = new_url
            redirect_count += 1
        else:
            # If no more redirects, return the final URL
            return current_url

    # If max redirects reached, return None or raise an exception
    if redirect_count == max_redirects:
        raise Exception("Max redirects reached. Possible infinite loop.")
    else:
        return current_url