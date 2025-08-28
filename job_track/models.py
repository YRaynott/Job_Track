from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class JobStatus(models.Model):
    name = models.CharField(max_length=10, verbose_name="狀態名稱")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "狀態名稱" #單數
        verbose_name_plural = verbose_name  #複數

class Job(models.Model):
    title = models.CharField(max_length=20, verbose_name='職位名稱')
    company = models.CharField(max_length=20, verbose_name='公司名稱')
    status = models.ForeignKey(JobStatus, on_delete=models.CASCADE, verbose_name='狀態')
    content = models.TextField(verbose_name='內容')
    job_link = models.URLField(verbose_name='職位頁面')
    company_link = models.URLField(verbose_name='公司官網')
    applied_at = models.DateField(null=True, blank=True, verbose_name='投遞時間')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='使用者')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '求職紀錄'
        verbose_name_plural = '求職紀錄'
        ordering = ['-applied_at']

