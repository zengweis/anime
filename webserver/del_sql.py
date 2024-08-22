import pymysql
import os

# 数据库配置
db = pymysql.connect(
    host="localhost",
    user="animelist",
    password="animelist",
    database="animelist"
)
cursor = db.cursor()

# 文件系统路径（根据实际情况修改）
FOLDER_PATH = '/www/wwwroot/anime/animelist'

# 查询数据库中的所有视频记录
query = "SELECT id, filename FROM videos"
cursor.execute(query)
records = cursor.fetchall()

# 列出文件系统中的所有文件
file_paths = set()
for root, dirs, files in os.walk(FOLDER_PATH):
    for file in files:
        file_paths.add(file)

# 找到失效的记录
ids_to_delete = []
for record_id, filename in records:
    if filename not in file_paths:
        ids_to_delete.append(record_id)

# 删除失效的记录
if ids_to_delete:
    delete_query = "DELETE FROM videos WHERE id IN (%s)" % ','.join(['%s'] * len(ids_to_delete))
    cursor.execute(delete_query, tuple(ids_to_delete))
    db.commit()
    print(f"Deleted {len(ids_to_delete)} invalid records.")
else:
    print("No invalid records found.")

# 关闭数据库连接
db.close()