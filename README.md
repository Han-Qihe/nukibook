### 项目名称：Nukibooks.com 爬虫脚本

#### 项目概述：
本项目是一个基于 Selenium 的爬虫脚本，用于从 Nukibooks.com 网站上爬取指定作者的所有文章及所有图片或指定文章下的所有图片，并将其保存到本地。用户可以选择按作者 ID 爬取该作者的所有文章及所有图片，或通过文章 ID 爬取单篇文章内容。

---

### 目录结构：
```bash
.
├── README.md                # 项目说明文件
├── nukibooks.py                  # 核心爬虫脚本
└── E:/tools/  # (示例) 爬取数据的默认保存目录
    └── nukibook/
        ├── {author_name}_{author_id}/    # 每个作者的文件夹
            ├── author_name.txt           # 保存作者名称
            ├── article_id.txt            # 该作者所有文章 ID
            ├── article_url.txt           # 该作者所有文章 URL
            └── articles/
                ├── {article_id}/
                    ├── img_url.txt       # 每篇文章的图片 URL
                    └── imgs/             # 下载的图片文件
```

### 环境依赖：

- Python 3.x
- Selenium 库
- Chrome 浏览器及其对应的 ChromeDriver
- `wget` 工具（用于下载图片）
  
### 安装步骤：

1. **安装 Selenium：**
   打开终端/命令行，运行以下命令：
   ```bash
   pip install selenium
   ```

2. **下载 ChromeDriver：**
   根据你的 Chrome 浏览器版本，下载对应的 ChromeDriver，并将其路径添加到系统环境变量中。可以从以下网址下载 ChromeDriver：
   [ChromeDriver下载地址](https://sites.google.com/a/chromium.org/chromedriver/downloads)

3. **安装 wget：**
   - 在 Linux 系统上，`wget` 通常是预装的。
   - 在 Windows 上，可以从 [GNU wget for Windows](https://eternallybored.org/misc/wget/) 下载并安装。安装后，确保 `wget` 在系统路径中。

---

### 使用说明：

#### 运行步骤：

1. 打开终端或命令行，进入脚本所在目录。

2. 运行以下命令启动脚本：
   ```bash
   python nukibooks.py
   ```

3. 根据提示选择操作：
   - **选项1**：输入 `1` 以爬取指定作者的所有文章及这些文章下的所有图片。
   - **选项2**：输入 `2` 以爬取指定文章下的所有图片。

4. **输入 ID：**
   - 如果选择 **选项1**，请输入作者的 ID（从 Nukibook 网站获取），程序将爬取该作者的所有文章及这些文章下的所有图片。
   - 如果选择 **选项2**，请输入文章的 ID，程序将爬取该文章下的所有图片。

5. **路径选择：**
   - 脚本默认将数据保存到 `E:/tools` 路径下。你可以根据提示选择修改保存路径，输入自定义路径，或者按回车保留默认路径。

6. 程序将自动进行爬取，保存数据包括：
   - **作者名称**
   - **文章 ID 和 URL**
   - **图片的 URL 和图片文件**

7. **文件结构：**
   - 数据将以 `{author_name}_{author_id}` 的形式创建文件夹。
   - 每篇文章都会有独立的文件夹，保存图片及其 URL。

---

### 函数说明：

#### `fetch_author_data(author_id, output_dir)`
- **功能**：获取指定作者的名称及其所有文章的 ID 和 URL，并将这些信息保存到本地。
- **参数**：
  - `author_id`: 作者的 ID，用于生成 URL 爬取数据。
  - `output_dir`: 用户指定的保存路径。
- **返回值**：`author_name`（作者名称），`author_output_dir`（保存路径）。

#### `fetch_img_urls(author_name, author_id, output_dir, article_id=None)`
- **功能**：爬取作者所有文章或指定文章下的所有图片 URL。
- **参数**：
  - `author_name`: 作者名称，用于路径生成。
  - `author_id`: 作者的 ID，用于文件夹命名。
  - `output_dir`: 保存数据的路径。
  - `article_id`: 如果指定，则只爬取此文章的图片。

#### `download_images(author_name, author_id, output_dir)`
- **功能**：从每篇文章的图片 URL 下载图片并保存到本地。
- **参数**：
  - `author_name`: 作者名称。
  - `author_id`: 作者 ID。
  - `output_dir`: 图片保存的路径。

---

### 注意事项：

1. **爬取限制**：
   - 确保遵守 Nukibook 网站的使用政策，不要进行过度频繁的爬取。
   - 在爬取时脚本会设置延迟 (`time.sleep`) 来避免被网站封禁。

2. **异常处理**：
   - 脚本已经处理了常见的异常情况，如找不到页面、按钮等。如果遇到其他问题，可以查看终端输出的错误信息。

3. **多次中断与继续**：
   - 如果由于网络或其他原因导致中断，你可以重新运行脚本，脚本会根据已有的文件跳过已经处理的数据，继续进行未完成的下载任务。

---

### 常见问题：

1. **如何获取作者 ID 或文章 ID？**
   - 你可以在 Nukibooks.com 网站的作者页面或文章 URL 中找到 `author_id` 或 `article_id`，例如：
     ```
     https://nukibooks.com/artists/{author_id}
     https://nukibooks.com/articles/{article_id}
     ```
例：
https://nukibooks.com/artists/15906
{author_id}为：15906

https://nukibooks.com/articles/2673553
{article_id}为：2673553

2. **如何修改保存路径？**
   - 运行脚本时，系统会提示当前的保存路径。你可以输入新的路径来自定义保存位置，或者按回车键使用默认路径。
   - **注意路径中斜杠使用“/”，而不是“\”，“//”，“\\”等。**

3. **如何增加下载速度？**
   - 你可以调整脚本中的 `time.sleep()` 时间，但是过快的爬取可能会导致被网站限制访问。

---

### 未来改进：

- 增加对并发下载的支持，以提升大批量爬取的效率。
- 增加对错误下载图片的自动重试功能。
- 提供 GUI 界面，方便不熟悉命令行的用户操作。

---

## 免责声明

- 本项目仅供学习和研究使用，请勿用于任何商业用途或侵犯版权的行为。
- 爬取数据前请遵守目标网站的 `robots.txt` 协议和相关法律规定。
- 未经许可，禁止对本项目的核心代码和逻辑进行修改或重新分发。

---

## 禁止修改声明

本项目提供的爬虫程序旨在展示网络爬取的基础方法，任何对本程序的修改与重新分发均需获得原作者的授权。请勿在未经允许的情况下将代码用于商业用途或进行核心逻辑修改，如有任何问题或需求，请联系项目维护者。
