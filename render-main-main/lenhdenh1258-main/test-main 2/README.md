# Ứng dụng đăng ký trường học

## Kết nối Telegram

Server sẽ gửi thông báo đến Telegram sau mỗi lượt đăng ký mới. Không ghi token bot vào mã nguồn; tạo file `.env` ở thư mục dự án với nội dung:

```bash
TELEGRAM_BOT_TOKEN=token-cua-bot
TELEGRAM_CHAT_ID=chat-id-nhan-thong-bao
```

Sau đó khởi động lại server:

```bash
python3 server.py
```

Để lấy `TELEGRAM_BOT_TOKEN`, tạo bot qua `@BotFather`. Để lấy `TELEGRAM_CHAT_ID`, nhắn một tin cho bot rồi đọc `chat.id` từ API `getUpdates` của Telegram.

Nếu chưa cấu hình hai biến trên, ứng dụng vẫn lưu dữ liệu SQLite và hoạt động bình thường nhưng không gửi thông báo.