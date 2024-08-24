<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require 'vendor/autoload.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST['name'];
    $email = $_POST['email'];
    $message = $_POST['message'];

    $mail = new PHPMailer(true);

    try {
        // 邮件服务器设置
        $mail->isSMTP();
        $mail->Host = 'smtp.qq.com'; 
        $mail->SMTPAuth = true;
        $mail->Username = '3428641781@qq.com'; 
        $mail->Password = 'vcxcxcloibmxdaij'; 
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_SMTPS;
        $mail->Port = 465;

        // 发件人设置
        $mail->setFrom('3428641781@qq.com', '反馈者');
        
        // 收件人设置
        $mail->addAddress('2195556927@qq.com');

        // 内容设置
        $mail->isHTML(false);
        $mail->Subject = '用户反馈';
        $mail->CharSet = 'UTF-8';
        $mail->Body = "姓名: $name\n邮箱: $email\n反馈内容:\n$message";

        $mail->send();
        
        // 自动跳转到主页
        echo '<script type="text/javascript">
                alert("反馈已成功发送！");
                window.location.href = "index.html";
              </script>';
        
        // 如果自动跳转失败，提供手动跳转链接
        echo '<noscript>
                <p>反馈已成功发送！</p>
                <p>如果没有自动跳转，请<a href="index.html">点击这里</a>返回主页。</p>
              </noscript>';
        
    } catch (Exception $e) {
        echo "反馈发送失败: {$mail->ErrorInfo}";
    }
}
?>