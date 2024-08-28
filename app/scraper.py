from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .database import SessionLocal
from .models import Article, Channel, ShortsVideo
from . import site_repo, category_repo
from datetime import datetime
import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import time
from googleapiclient.discovery import build
import json
import os
from .crud import create_channel, create_shorts_video
from .utils import iso_to_datetime
import yt_dlp as ytdlp
from pymongo import MongoClient
import gridfs

SETTINGS_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'settings.json')

with open(SETTINGS_FILE_PATH, 'r') as file:
    settings = json.load(file)
    
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

def update_article_content(article: Article, db, division='plain'):
    """
    기사 상세 정보 업데이트
    """
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    if division == 'plain':
        article_url = article.url
    else:
        article_url = article.redirected_url

    print("--------------")
    print("id : " + str(article.id))
    print("category_id : " + str(article.categories))
    print("url : " + str(article_url))
    print("--------------")

    # BeautifulSoup를 사용하여 기사의 내용을 스크랩
    try:
        response = requests.get(article_url, allow_redirects=False)
        print("response code : " + str(response.status_code))
        if response.status_code == 200:

            if division == 'plain':
                soup = BeautifulSoup(response.content, 'html.parser')
                # headline
                headline_tag = soup.find('h2', {'id':'title_area'})
                if headline_tag is not None:
                    print('==========headline==========')
                    headline = headline_tag.find('span').text
                    print(headline)
                    article.headline = headline

                # body
                dic_area_tag = soup.find('article', {'id':'dic_area'})
                if dic_area_tag is not None:
                    print('==========body==========')
                    content = []
                    for element in dic_area_tag.descendants:
                        if element.name == 'img':
                            img_src = element.get('data-src', '')
                            img_alt = element.get('alt', '')
                            if img_src:  # data-src가 존재하는 경우에만 커스텀 태그로 감싸기
                                custom_tagged_img = f'<catch-weak-img>{img_src}?alt={img_alt}</catch-weak-img>'
                                content.append(custom_tagged_img)
                        elif element.name not in ['script', 'style'] and element.string and element.parent.name != 'em':
                            text = element.string.strip() # 스크립트와 스타일 태그를 제외하고, em 태그의 부모가 아닌 경우만 텍스트를 추가
                            if text:
                                content.append(text)

                    article_body = '\n'.join(content)
                    print(article_body)
                    article.body = article_body

                    # summary
                    media_end_summary_tag_list = dic_area_tag.findAll('strong')
                    if media_end_summary_tag_list is not None and media_end_summary_tag_list != []:
                        media_end_summary_tag = dic_area_tag.findAll('strong')[0]
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
            elif division == 'entertain':
                driver.get(article_url)
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                # headline
                pattern = re.compile(r'^NewsEndMain_article_title__')
                headline_tag = soup.find('h2', class_=pattern)
                if headline_tag is not None:
                    print('==========headline==========')
                    headline = headline_tag.text
                    print(headline)
                    article.headline = headline
                
                # body
                body_tag = soup.find('div', {'class':'_article_content'})
                if body_tag is not None:
                    print('==========body==========')
                    print(body_tag.text)
                    article.body = body_tag.text
                
                # TODO : summary

                # image url
                image_span_tag = soup.find('span', {'class':'NewsEndMain_image_wrap__djL-o'})
                if image_span_tag is not None:
                    img_tag = image_span_tag.find('img')
                    if img_tag and 'src' in img_tag.attrs:
                        print('==========image url==========')
                        print(img_tag['src'])
                        article.img_url = img_tag['src']
                
                # origin url
                origin_article_url_tag = soup.find('a', {'class', 'NewsEndMain_link_origin_article__7igDs'})
                if origin_article_url_tag is not None:
                    print('==========origin_article_url_tag==========')
                    print(origin_article_url_tag['href'])
                    article.origin_url = origin_article_url_tag['href']

                # TODO : author
                # author가 존재하는 기사를 연예, 스포츠에서는 보지 못함.
                
                # create date
                date_tag_list = soup.findAll('em', {'class', 'date'})
                if date_tag_list is not None:
                    print('==========created_at_tag==========')
                    print(date_tag_list[0].text)
                    article.article_created_at = date_tag_list[0].text

                    if len(date_tag_list) > 1:
                        print('==========updated_at_tag==========')
                        print(date_tag_list[1].text)
                        article.article_updated_at = date_tag_list[1].text

            elif division == 'sports':
                driver.get(article_url)
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                # headline
                pattern = re.compile(r'^NewsEndMain_article_title__')
                headline_tag = soup.find('h2', class_=pattern)
                if headline_tag is not None:
                    print('==========headline==========')
                    headline = headline_tag.text
                    print(headline)
                    article.headline = headline
                
                # body
                body_tag = soup.find('div', {'class':'_article_content'})
                if body_tag is not None:
                    print('==========body==========')
                    print(body_tag.text)
                    article.body = body_tag.text
                
                # TODO : summary

                # image url
                image_span_tag = soup.find('span', {'class':'NewsEndMain_image_wrap__djL-o'})
                if image_span_tag is not None:
                    img_tag = image_span_tag.find('img')
                    if img_tag and 'src' in img_tag.attrs:
                        print('==========image url==========')
                        print(img_tag['src'])
                        article.img_url = img_tag['src']
                
                # origin url
                origin_article_url_tag = soup.find('a', {'class', 'NewsEndMain_link_origin_article__7igDs'})
                if origin_article_url_tag is not None:
                    print('==========origin_article_url_tag==========')
                    print(origin_article_url_tag['href'])
                    article.origin_url = origin_article_url_tag['href']

                # TODO : author
                # author가 존재하는 기사를 연예, 스포츠에서는 보지 못함.
                
                # create date
                date_tag_list = soup.findAll('em', {'class', 'NewsEndMain_date__xjtsQ'})
                if date_tag_list is not None:
                    print('==========created_at_tag==========')
                    print(date_tag_list[0].text)
                    article.article_created_at = date_tag_list[0].text

                    if len(date_tag_list) > 1:
                        print('==========updated_at_tag==========')
                        print(date_tag_list[1].text)
                        article.article_updated_at = date_tag_list[1].text

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
            new_url = response.headers.get('Location')
            if not new_url:
                break
            
            if not new_url.startswith('http'):
                from urllib.parse import urljoin
                new_url = urljoin(current_url, new_url)
            
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
    
def scrap_detail_page_redirected_url(division):
    """
    스포츠,연예 기사 상세 정보 크롤링
    """
    db = SessionLocal()
    try:
        # 연예 뉴스
        if division == 'entertain':
            articles = db.query(Article).filter(Article.redirected_url.startswith('https://m.entertain.naver.com')).all()
        elif division == 'sports':
            articles = db.query(Article).filter(Article.redirected_url.startswith('https://m.sports.naver.com')).all()

        for article in articles:
            update_article_content(article, db, division)
    finally:
        db.close()

def scrap_shorts(keyword, request_cnt):
    """
    쇼츠 정보 가져오기
    """
    db = SessionLocal()

    api_key = settings['apiKey']

    youtube = build('youtube', 'v3', developerKey=api_key)
    channel_id = 'UCcQTRi69dsVYHN3exePtZ1A'  # KBS World TV 채널 ID
    try:
        results = []
        next_page_token = None
        keyword_query = (keyword + ' #Shorts') if keyword else '#Shorts'

        # 검색 요청을 반복하면서 비디오 ID를 청크로 나눔
        while True:
            request = youtube.search().list(
                part='snippet',
                channelId=channel_id,
                order='date',
                q=keyword_query,
                type='video',
                maxResults=min(request_cnt, 50),  # 한 번에 최대 50개
                pageToken=next_page_token
            )
            response = request.execute()

            video_ids = [item['id']['videoId'] for item in response['items']]
            if not video_ids:
                break

            video_request = youtube.videos().list(
                part='snippet,statistics',
                id=','.join(video_ids)
            )
            video_response = video_request.execute()

            # 조회수 기준으로 정렬
            videos = sorted(video_response['items'], key=lambda x: int(x['statistics']['viewCount']), reverse=True)
            results.extend(videos)

            next_page_token = response.get('nextPageToken')
            if not next_page_token or len(results) >= request_cnt:
                break

        # DB 저장 작업 등 처리
        for item in results:
            snippet = item.get('snippet', {})
            statistics = item.get('statistics', {})

            tags = ', '.join(snippet.get('tags', []))
            channel_title = snippet.get('channelTitle', 'Unknown Channel')
            existing_channel = db.query(Channel).filter(Channel.channel_id == channel_id).first()
            if not existing_channel:
                create_channel(db, channel_id, channel_title)

            create_shorts_video(db, 
                video_id=item['id'],
                title=snippet.get('title', 'No title available'),
                description=snippet.get('description', 'No description available'),
                published_at=iso_to_datetime(snippet.get('publishedAt')),
                view_count=int(statistics.get('viewCount', 0)),
                like_count=int(statistics.get('likeCount', 0)),
                comment_count=int(statistics.get('commentCount', 0)),
                thumbnail_url=snippet.get('thumbnails', {}).get('maxres', {}).get('url', 'No thumbnail available'),
                channel_id=channel_id,
                tags=tags
            )
    finally:
        db.close()


def download_shorts(batch_size=100):
    """
    DB에서 비디오 ID를 100개씩 조회하여 다운로드하고 MongoDB에 저장
    """
    db = SessionLocal()
    mongo_settings = settings['mongodb']

    client = MongoClient(f"mongodb+srv://{mongo_settings['username']}:{mongo_settings['password']}@{mongo_settings['host']}/?retryWrites=true&w=majority&appName={mongo_settings['options']['appName']}")
    # local
    # client = MongoClient(
    #     f"mongodb://{mongo_settings['username']}:{mongo_settings['password']}@"
    #     f"{mongo_settings['host']}:{mongo_settings['port']}/"
    # )
    mongodb = client[mongo_settings['dbname']]
    fs = gridfs.GridFS(mongodb)
    files_collection = mongodb['fs.files']
    chunks_collection = mongodb['fs.chunks']

    download_path = settings['downloadPath']
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',  # 비디오 제목을 파일명으로 사용합니다.
        'quiet': False,  # console log
    }

    try:
        offset = 0
        while True:
            shorts_videos = db.query(ShortsVideo).offset(offset).limit(batch_size).all()
            
            if not shorts_videos:
                break
            
            for video in shorts_videos:
                url = 'https://www.youtube.com/shorts/' + video.video_id
                try:
                    with ytdlp.YoutubeDL(ydl_opts) as ydl:
                        info_dict = ydl.extract_info(url, download=True)
                        file_path = ydl.prepare_filename(info_dict)
                        print(f"Video downloaded successfully: {video.title} ({url})")

                    existing_file = files_collection.find_one({'metadata.video_id': video.video_id})

                    if existing_file:
                        print(f"Video already exists in MongoDB: {video.title}")
                        # 로컬 파일 삭제
                        os.remove(file_path)
                        continue

                    with open(file_path, 'rb') as video_file:
                        file_id = fs.put(
                            video_file,
                            filename=os.path.basename(file_path),
                            video_id=video.video_id,
                            metadata={
                                'title': video.title,
                                'description': video.description,
                                'published_at': video.published_at,
                                'view_count': video.view_count,
                                'like_count': video.like_count,
                                'comment_count': video.comment_count,
                                'thumbnail_url': video.thumbnail_url,
                                'tags': video.tags,
                                'channel_id': video.channel_id
                            }
                        )
                        print(f"Video stored in MongoDB: {video.title}")
                    os.remove(file_path)

                except Exception as e:
                    print(f"An error occurred while downloading {video.title}: {e}")

            offset += batch_size

    except SQLAlchemyError as e:
        print(f"An error occurred during the database operation: {e}")
    finally:
        db.close()