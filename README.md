# anime
#### upload_systeam
###### 部署于anime下载机，基于python环境，请提前安装pip install boto3 tqdm

    --r2_test.py  用于测试链接
    --upload_to_r2.py  上传指定目录下的文件，需要获取key与指定目录
#### webserver
###### 部署于云服务器，提供网页查询服务，安装LNMP python（bot3 tdmp）
    --beindex.py  用于创建animelist文件夹下的单独网页与index网页
    --del_sql.py  用于清理sql语句，防止重复查询
    --search.php  提供查询功能
## 配置 
本系统在下载机采用windowsserver2019，利用qbittorrent的rss订阅实现自动下载，需要在qbittorrent中设置下载完后自动执行upload_to_r2.py 示例语句 --python "C:\your_path\upload_to_r2.py" "%F"
网页端server需设置定时任务 参考语句 --sudo -u root bash -c 'python3 /www/wwwroot/anime/del_sql.py
python3 /www/wwwroot/anime/beindex.py'

sql数据库配置
登陆
--mysql -u animelist -p 

建表
--
USE animelist;
CREATE TABLE videos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    pagelink VARCHAR(255) NOT NULL
);
