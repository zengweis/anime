<?php
// 数据库配置
$host = 'localhost';
$dbname = 'animelist';
$user = 'animelist';
$pass = 'animelist';

try {
    // 创建数据库连接
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // 获取搜索查询
    $query = isset($_GET['query']) ? $_GET['query'] : '';

    if ($query) {
        // 搜索数据库中的视频文件名
        $stmt = $pdo->prepare("SELECT filename, pagelink FROM videos WHERE filename LIKE ?");
        $stmt->execute(['%' . $query . '%']);
        $results = $stmt->fetchAll(PDO::FETCH_ASSOC);
    } else {
        $results = [];
    }
} catch (PDOException $e) {
    echo "Database error: " . $e->getMessage();
    die();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Results</title>
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
        .search-box {
            text-align: center;
            margin-bottom: 20px;
        }
        input[type="text"] {
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 8px;
            width: 80%;
            max-width: 500px;
        }
        input[type="submit"] {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #007aff;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <h1>Search Results</h1>
    <div class="search-box">
        <form action="search.php" method="get">
            <input type="text" name="query" value="<?php echo htmlspecialchars($query); ?>" placeholder="Search for a video...">
            <input type="submit" value="Search">
        </form>
    </div>

    <ul>
        <?php if ($results): ?>
            <?php foreach ($results as $result): ?>
                <li><a href="<?php echo htmlspecialchars($result['pagelink']); ?>"><?php echo htmlspecialchars($result['filename']); ?></a></li>
            <?php endforeach; ?>
        <?php else: ?>
            <li>No results found for "<?php echo htmlspecialchars($query); ?>"</li>
        <?php endif; ?>
    </ul>
</body>
</html>