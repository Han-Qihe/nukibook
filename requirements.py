import os
import platform
import requests
import zipfile
import subprocess
import sys
import shutil

def install_dependencies():
    print("安装 Python 依赖...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])

def install_wget():
    print("安装 wget 工具...")
    os_type = platform.system().lower()
    if os_type == "windows":
        # Windows 上安装 wget
        wget_url = "https://eternallybored.org/misc/wget/releases/wget-1.21.3-win64.zip"
        wget_zip = "wget.zip"
        wget_dir = "wget"
        
        # 下载 wget
        response = requests.get(wget_url)
        with open(wget_zip, 'wb') as f:
            f.write(response.content)
        
        # 解压
        with zipfile.ZipFile(wget_zip, 'r') as zip_ref:
            zip_ref.extractall(wget_dir)
        
        # 将 wget 添加到系统 PATH 中
        wget_path = os.path.abspath(os.path.join(wget_dir, "wget.exe"))
        os.environ["PATH"] += os.pathsep + wget_path
        
        print(f"wget 已安装并配置为：{wget_path}")
    elif os_type == "linux" or os_type == "darwin":
        if os_type == "linux":
            subprocess.check_call(["sudo", "apt-get", "install", "-y", "wget"])
        elif os_type == "darwin":
            subprocess.check_call(["brew", "install", "wget"])
    else:
        print(f"未知的操作系统：{os_type}")

def get_latest_stable_version():
    print("获取最新的稳定版 Chrome 和 ChromeDriver...")
    url = "https://googlechromelabs.github.io/chrome-for-testing/latest-stable.json"
    response = requests.get(url)
    version_data = response.json()
    return version_data['version']

def download_and_install_chrome(chrome_version):
    print(f"安装 Chrome 版本：{chrome_version}")
    os_type = platform.system().lower()
    download_url = None

    if os_type == "windows":
        download_url = f"https://edgedl.me.gvt1.com/edgedl/chrome-for-testing/{chrome_version}/win64/chrome-win64.zip"
    elif os_type == "linux":
        download_url = f"https://edgedl.me.gvt1.com/edgedl/chrome-for-testing/{chrome_version}/linux64/chrome-linux64.zip"
    elif os_type == "darwin":
        download_url = f"https://edgedl.me.gvt1.com/edgedl/chrome-for-testing/{chrome_version}/mac-arm64/chrome-mac-arm64.zip"

    if download_url:
        chrome_zip = "chrome_stable.zip"
        response = requests.get(download_url)
        with open(chrome_zip, 'wb') as f:
            f.write(response.content)

        # 解压缩并安装 Chrome
        with zipfile.ZipFile(chrome_zip, 'r') as zip_ref:
            zip_ref.extractall("chrome_stable")

        # 配置路径
        chrome_path = os.path.abspath("chrome_stable")
        os.environ["PATH"] += os.pathsep + chrome_path
        print(f"Chrome 已安装到：{chrome_path}")
    else:
        print("不支持的操作系统。")

def download_and_install_chromedriver(chrome_version):
    print(f"安装 ChromeDriver 版本：{chrome_version}")
    os_type = platform.system().lower()
    download_url = None

    if os_type == "windows":
        download_url = f"https://edgedl.me.gvt1.com/edgedl/chrome-for-testing/{chrome_version}/win64/chromedriver-win64.zip"
    elif os_type == "linux":
        download_url = f"https://edgedl.me.gvt1.com/edgedl/chrome-for-testing/{chrome_version}/linux64/chromedriver-linux64.zip"
    elif os_type == "darwin":
        download_url = f"https://edgedl.me.gvt1.com/edgedl/chrome-for-testing/{chrome_version}/mac-arm64/chromedriver-mac-arm64.zip"

    if download_url:
        chromedriver_zip = "chromedriver_stable.zip"
        response = requests.get(download_url)
        with open(chromedriver_zip, 'wb') as f:
            f.write(response.content)

        # 解压缩并安装 ChromeDriver
        with zipfile.ZipFile(chromedriver_zip, 'r') as zip_ref:
            zip_ref.extractall("chromedriver_stable")

        # 配置路径
        chromedriver_path = os.path.abspath("chromedriver_stable")
        os.environ["PATH"] += os.pathsep + chromedriver_path
        print(f"ChromeDriver 已安装到：{chromedriver_path}")
    else:
        print("不支持的操作系统。")

if __name__ == "__main__":
    install_dependencies()
    install_wget()
    chrome_version = get_latest_stable_version()
    download_and_install_chrome(chrome_version)
    download_and_install_chromedriver(chrome_version)
    print("所有依赖、Chrome 和 ChromeDriver 已成功安装。")
