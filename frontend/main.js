document.addEventListener("DOMContentLoaded", function () {
    const chatInput = document.querySelector(".chat-input");
    const sendButton = document.querySelector(".chat-button");
    const chatMessages = document.querySelector(".chat-messages");
    const suggestedMessages = document.querySelectorAll(".suggested-message");
    const suggestionButtons = document.querySelectorAll('.suggestion-button');
    const suggestionContainer = document.querySelector('.suggestion-container');

    // Gửi tin nhắn khi nhấn nút gửi hoặc Enter
    sendButton.addEventListener("click", handleSendMessage);
    chatInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            handleSendMessage();
        }
    });

    // Xử lý khi nhấn vào gợi ý tin nhắn
    suggestedMessages.forEach((msg) => {
        msg.addEventListener("click", function () {
            chatInput.value = msg.textContent;
            handleSendMessage();
        });
    });

    suggestionButtons.forEach(button => {
        button.addEventListener('click', function() {
            document.getElementById('user-input').value = this.textContent;
            document.getElementById('send-button').click();
        });
    });

    let chatHistory = [];

    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function updateSuggestions(questions) {
        // Xóa các suggestion cũ
        suggestionContainer.innerHTML = '';
        
        // Thêm các câu hỏi liên quan mới
        questions.forEach(question => {
            const button = document.createElement('button');
            button.className = 'suggestion-button';
            button.textContent = question;
            button.addEventListener('click', () => {
                chatInput.value = question;
                handleSendMessage();
            });
            suggestionContainer.appendChild(button);
        });
    }

    async function handleSendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        // Hiển thị tin nhắn người dùng
        addMessage(message, true);
        chatInput.value = '';

        // Thêm loading
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message bot-message loading';
        loadingDiv.textContent = 'Đang trả lời...';
        chatMessages.appendChild(loadingDiv);

        try {
            const response = await fetch('http://localhost:8001/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_message: message
                })
            });

            chatMessages.removeChild(loadingDiv);

            if (response.ok) {
                const data = await response.json();
                // Hiển thị câu trả lời
                addMessage(data.answer, false);
                // Cập nhật các câu hỏi gợi ý
                if (data.related_questions && data.related_questions.length > 0) {
                    updateSuggestions(data.related_questions);
                }
            } else {
                addMessage('Xin lỗi, có lỗi xảy ra. Vui lòng thử lại.', false);
            }
        } catch (error) {
            chatMessages.removeChild(loadingDiv);
            addMessage('Lỗi kết nối đến server. Vui lòng thử lại.', false);
            console.error('Error:', error);
        }
    }

    // Khởi tạo các câu hỏi gợi ý ban đầu
    const initialQuestions = [
        "Kinh nghiệm với AI của bạn?",
        "Các dự án tiêu biểu?",
        "Tech stack chính?"
    ];
    updateSuggestions(initialQuestions);
});
