document.addEventListener("DOMContentLoaded", function () {
    const input = document.querySelector("input[name='applied_at']");
    if (input && !input.value) {
        const now = new Date();
        const yyyy = now.getFullYear();
        const mm = String(now.getMonth() + 1).padStart(2, '0');
        const dd = String(now.getDate()).padStart(2, '0');
        const today = `${yyyy}-${mm}-${dd}`;
        input.value = today;
    }
});

$(function () {
    $('#submit-btn').click(function (e) {
        e.preventDefault();

        $.ajax({
            url: '',  // 或 /track/add/
            method: 'POST',
            data: $('form').serialize(),
            success: function (result) {
                if (result.code === 200) {
                    alert(result.message);
                    window.location.href = '/track/';  // ✅ 成功跳轉
                } else {
                    alert(result.message);
                }
            },
            error: function (err) {
                console.log(err);
                alert("新增失敗，請稍後再試！");
            }
        });
    });
});
