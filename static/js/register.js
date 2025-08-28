$(function(){
	function bindCaptchaBynClick(){
		$("#captcha-btn").click(function(event){
			let $this = $(this);
			let email = $("input[name='email']").val();
			if(!email){
				alert("請先輸入電子郵件帳號");
				return;
			}
			// 取消按鈕的點擊事件(限時)
			$this.off('click');

			//發送ajax請求
			$.ajax('/auth/captcha?email='+email, {
				method: 'GET',
				success: function (result){
					if(result['code'] == 200){
						alert("驗證碼發送成功!");
					}else{
						alert(result['message']);
					}
				},
				fail: function (error) {
					console.log(error);
				}
			})

			let countdown = 180; // 倒數60秒
			setInterval(function(){
				if(countdown <= 0){
					$this.text('獲取驗證碼');
					// 清除計時器
					clearInterval(timer);
					// 重新綁定點及事件
					bindCaptchaBynClick();
				}else{
					countdown--;
					$this.text(countdown+'s');
				}
			},1000);
		})
	}

	bindCaptchaBynClick();
})