import boto3
import os
import pymysql

# 配置 Cloudflare R2 端点和凭证
s3_client = boto3.client('s3',
                         endpoint_url='https://.r2.cloudflarestorage.com',
                         aws_access_key_id='',
                         aws_secret_access_key='')

bucket_name = 'anime-web-aliyun'
output_dir = '/www/wwwroot/anime/animelist'  # 视频页面保存的目录
index_file_path = '/www/wwwroot/anime/index.html'  # index.html 保存的文件路径

# MySQL 数据库配置
db = pymysql.connect(
    host="127.0.0.1",
    user="animelist",
    password="animelist",
    database="animelist"
)
cursor = db.cursor()

# 确保输出目录存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 删除目录中的 .DS_Store 文件
def delete_ds_store_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == '.DS_Store':
                os.remove(os.path.join(root, file))

# 删除旧的 .DS_Store 文件（如果存在）
delete_ds_store_files(output_dir)

# 生成index.html和播放页面
def generate_html_files():
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    files = [obj['Key'] for obj in response.get('Contents', [])]

    # 生成index.html
    index_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Video Index</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                background-color: #f5f5f7;
                color: #333;
                margin: 0;
                padding: 20px;
                line-height: 1.6;
            }
            h1 {
                text-align: center;
                margin-bottom: 40px;
            }
            ul {
                list-style: none;
                padding: 0;
            }
            li {
                margin: 10px 0;
            }
            a {
                text-decoration: none;
                color: #007aff;
                font-size: 18px;
            }
            a:hover {
                text-decoration: underline;
            }
            .search-button {
                text-align: center;
                margin-bottom: 20px;
            }
            button {
                padding: 10px 20px;
                font-size: 16px;
                background-color: #007aff;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }
            button:hover {
                background-color: #005bb5;
            }
            
        </style>
        
    
    
    </head>
    <body>
            
            <h4>想看的番不在？⬇️⬇️⬇️问题反馈</h4>
   
            <a href="feedback_form.php"><button>问题反馈</button></a>
     
     
        <h1>Video Index</h1>
        <div class="search-button">
            <a href="search.php"><button>Search</button></a>
        </div>
        <ul>
    '''

    for file in files:
        file_name = os.path.basename(file)
        file_link = f"animelist/{file_name}.html"  # 更新链接路径以指向正确的目录
        
        # 在插入之前删除可能存在的重复记录
        cursor.execute("DELETE FROM videos WHERE filename = %s", (file_name,))
        
        # 插入文件名和页面链接到数据库
        cursor.execute("INSERT INTO videos (filename, pagelink) VALUES (%s, %s)", (file_name, file_link))
        
        # 生成单个视频播放页面
        video_page_content = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{file_name}</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/dplayer@1.25.0/dist/DPlayer.min.css">
            <script src="https://cdn.jsdelivr.net/npm/dplayer@1.25.0/dist/DPlayer.min.js"></script>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                    background-color: #f5f5f7;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                    text-align: center;
                }}
                #dplayer {{
                    width: 80%;
                    max-width: 1000px;
                    margin: 20px auto;
                    border-radius: 8px;
                    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.1);
                }}
                a {{
                    text-decoration: none;
                    color: #007aff;
                    font-size: 18px;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <h1>{file_name}</h1>
            <div id="dplayer"></div>
            <p><a href="http://www.1a.wiki">Back to Index</a></p>

            <script>
                const dp = new DPlayer({{
                    container: document.getElementById('dplayer'),
                    video: {{
                        url: 'https://anime.1a.wiki/{file}',
                        type: 'auto',
                    }},
                    danmaku: {{
                        id: '{file_name}',
                        api: 'https://www.1a.wiki/www/wwwroot/anime/DPlayer-node-master/',
                    }},
                    contextmenu: [
                        {{
                            text: 'DPlayer',
                            link: 'https://github.com/DIYgod/DPlayer',
                        }},
                    ],
                }});
            </script>
        </body>
        </html>
        '''

        # 将视频页面写入文件
        with open(os.path.join(output_dir, f"{file_name}.html"), 'w', encoding='utf-8') as f:
            f.write(video_page_content)

        # 在index.html中添加链接
        index_content += f'<li><a href="{file_link}">{file_name}</a></li>\n'

    index_content += '''
        </ul>
    </body>
    </html>
    '''

    # 将index.html写入文件
    with open(index_file_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    # 提交数据库更改
    db.commit()
    

# 运行脚本生成HTML文件
generate_html_files()
delete_ds_store_files(output_dir)
# 关闭数据库连接
db.close()
