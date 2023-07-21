const form = document.querySelector('form');
const chatBox = document.getElementById('chat_box');

const scrollToBottom = () => {
    chatBox.scrollTop = chatBox.scrollHeight;
}

form.addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(form);
    fetch('/send_message', {
        method: 'POST',
        body: formData
    })
        .then(response => response.text())
        .then(data => {
            // Adicionando a mensagem do usuário
            const userMessageDiv = document.createElement('div');
            userMessageDiv.innerHTML = `<p class="user-message">${formData.get('human_input')}</p>`;
            chatBox.appendChild(userMessageDiv);
            // Adicionando a resposta do bot
            const botMessageDiv = document.createElement('div');
            botMessageDiv.innerHTML = `<p class="chat-response">${data}</p>`;
            chatBox.appendChild(botMessageDiv);
            scrollToBottom();
        });
    form.reset();
});
