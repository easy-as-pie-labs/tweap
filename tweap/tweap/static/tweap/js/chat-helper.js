(function() {
    localStorage.removeItem('chat-raw-credentials');
    localStorage.removeItem('chat-credentials');
    localStorage.removeItem('chat-conversations');
    localStorage.removeItem('chatToggleStatus');
    localStorage.removeItem('overView');
    $( document ).ready(function() {
        $('form').submit(function () {
            var chatRawCredentials = {};
            chatRawCredentials.username = $("[name='username']").val();
            chatRawCredentials.password = $("[name='password']").val();
            localStorage.setItem('chat-raw-credentials', JSON.stringify(chatRawCredentials));
        });
    });
})();

