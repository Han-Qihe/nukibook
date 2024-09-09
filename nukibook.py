from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

def fetch_author_data(author_id, output_dir):
    # 设置 Chrome 配置
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式
    service = Service()  # 根据需要设置 ChromeDriver 的路径
    driver = webdriver.Chrome(service=service, options=chrome_options)

    base_url = f"https://nukibooks.com/artists/{author_id}"
    driver.get(base_url)

    author_name = None
    try:
        # 获取作者名称
        author_name = driver.find_element(By.CSS_SELECTOR, "div.home-gallery h1.gallery-ttl").text
        print("作者名称:", author_name)

        # 创建目录
        author_output_dir = f"{output_dir}/nukibook/{author_name}_{author_id}"
        os.makedirs(author_output_dir, exist_ok=True)

        # 保存作者名称
        with open(f"{author_output_dir}/author_name.txt", "w", encoding="utf-8") as file:
            file.write(author_name)

        # 存储所有文章的 article_id
        article_ids = set()
        while True:
            articles = driver.find_elements(By.CSS_SELECTOR, "div.gallery-item-figure img")
            for img in articles:
                src = img.get_attribute("src")
                article_id = src.split('/')[3]  # 提取 article_id
                article_ids.add(article_id)

            # 检查是否有下一页
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "a.next")
                if "disabled" in next_button.get_attribute("class"):
                    break
                else:
                    next_button.click()
                    time.sleep(3)
            except Exception as e:
                print(f"无法找到下一页按钮: {e}")
                break

        # 保存 article_ids
        with open(f"{author_output_dir}/article_id.txt", "w", encoding="utf-8") as file:
            for article_id in article_ids:
                file.write(article_id + "\n")
        
        print("所有文章ID已保存")
        
        # 生成文章URL
        with open(f"{author_output_dir}/article_id.txt", "r", encoding="utf-8") as file:
            article_ids = file.readlines()
        
        with open(f"{author_output_dir}/article_url.txt", "w", encoding="utf-8") as file:
            for article_id in article_ids:
                article_id = article_id.strip()
                article_url = f"https://nukibooks.com/articles/{article_id}"
                file.write(article_url + "\n")
        
        print("所有文章URL已保存")

    except Exception as e:
        print(f"爬取数据时出错: {e}")

    finally:
        driver.quit()

    return author_name, author_output_dir

def fetch_img_urls(author_name, author_id, output_dir, article_id=None):
    driver = webdriver.Chrome()
    author_output_dir = f"{output_dir}/nukibook/{author_name}_{author_id}"

    if article_id:
        article_urls = [f"https://nukibooks.com/articles/{article_id}"]
    else:
        with open(f"{author_output_dir}/article_url.txt", "r", encoding="utf-8") as file:
            article_urls = file.readlines()
    
    for url in article_urls:
        url = url.strip()
        article_id = url.split('/')[-1]
        article_img_dir = os.path.join(author_output_dir, f"articles/{article_id}/imgs")
        os.makedirs(article_img_dir, exist_ok=True)
        
        with open(f"{author_output_dir}/articles/{article_id}/img_url.txt", "w", encoding="utf-8") as file:
            driver.get(url)
            try:
                image_elements = driver.find_elements(By.CSS_SELECTOR, "div.article-page-list img")
                for index, img in enumerate(image_elements):
                    img_src = img.get_attribute("src")
                    file.write(img_src + "\n")
            except Exception as e:
                print(f"无法获取图片 URL: {e}")

    driver.quit()

def download_images(author_name, author_id, output_dir):
    author_output_dir = f"{output_dir}/nukibook/{author_name}_{author_id}/articles"
    img_dirs = [d for d in os.listdir(author_output_dir) if os.path.isdir(os.path.join(author_output_dir, d))]

    for img_dir in img_dirs:
        url_file = os.path.join(author_output_dir, img_dir, "img_url.txt")
        download_dir = os.path.join(author_output_dir, img_dir, "imgs")
        os.makedirs(download_dir, exist_ok=True)

        with open(url_file, 'r', encoding='utf-8') as file:
            urls = file.readlines()
            for url in urls:
                url = url.strip()
                if url:
                    file_name = os.path.basename(url)
                    download_path = os.path.join(download_dir, file_name)
                    wget_command = f'wget -O "{download_path}" "{url}"'
                    print(f'执行命令: {wget_command}')
                    os.system(wget_command)

    print('所有图片下载完成')

if __name__ == "__main__":
    print("请选择:")
    print("1. 请输入作者ID，这将爬取该作者的所有文章及作品")
    print("2. 请输入文章ID，这将爬取该文章下的所有作品")
    choice = input("请选择 (1 或 2): ").strip()

    if choice == '1':
        author_id = input("请输入作者ID: ").strip()
        article_id = None
    elif choice == '2':
        article_id = input("请输入文章ID: ").strip()
        author_id = "unknown_author"
    else:
        print("无效的选择")
        exit()

    # 询问用户是否需要修改保存路径
    default_output_dir = "E:/tools"
    output_dir = input(f"当前路径为 {default_output_dir}，是否修改？按回车保留当前路径或输入新路径，注意路径中斜杠使用/，而不是\，//，\\: ")
    output_dir = output_dir.strip() or default_output_dir

    if choice == '1':
        author_name, author_output_dir = fetch_author_data(author_id, output_dir)
        fetch_img_urls(author_name, author_id, output_dir)
    elif choice == '2':
        author_name = "未知作者"
        fetch_img_urls(author_name, author_id, output_dir, article_id)

    download_images(author_name, author_id, output_dir)
