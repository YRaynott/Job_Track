// detail.js
$(document).ready(function () {
    $("form").on("submit", function (e) {
        e.preventDefault();  // 阻止預設提交（避免頁面刷新）

        const form = $(this);
        const url = form.attr("action") || window.location.href; // 保持目前頁面
        const formData = form.serialize(); // 把表單資料序列化成 URL 編碼格式

        $.post(url, formData)
            .done(function (data) {
                showAlert("更新成功！", "success");
            })
            .fail(function (xhr) {
                showAlert("更新失敗，請檢查輸入內容。", "danger");
            });
    });

    function showAlert(message, type) {
        const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`;
        $("#liveAlertPlaceholder").html(alertHtml);
    }
});
