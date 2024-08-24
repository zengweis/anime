<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>反馈页面</title>
</head>
<body>
    <form action="send_feedback.php" method="post">
        <label for="name">您的昵称:</label><br>
        <input type="text" id="name" name="name" required><br><br>
        <label for="email">您的邮箱:</label><br>
        <input type="email" id="email" name="email" required><br><br>
        <label for="message">反馈内容:</label><br>
        <textarea id="message" name="message" required></textarea><br><br>
        <button type="submit">提交反馈</button>
    </form>
</body>
</html>