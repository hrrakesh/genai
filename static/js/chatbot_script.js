const chatDiv = document.getElementById('chat');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');



sendButton.addEventListener('click', async () => {
    const userMessage = userInput.value;
    if (!userMessage) return;

    chatDiv.innerHTML += `<div class="message user-message"><span class="message-label">User:</span> ${userMessage}</div>`;

    const response = await fetch('/chat_with_bot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
    });

    const data = await response.json();

    chatDiv.innerHTML += `<div class="message ai-message"><span class="message-label">AI:</span> ${data.message}</div>`;

    userInput.value = '';

    chatDiv.scrollTop = chatDiv.scrollHeight;
});

