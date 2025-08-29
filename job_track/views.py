from django.db.models import Q
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .models import Job, JobStatus
from .forms import JobAddForm, JobEditForm

def index(request):
    jobs = Job.objects.filter(user=request.user)
    return render(request, 'index.html', context={'jobs': jobs})

def help(request):
    return render(request, 'help.html')

@require_http_methods(["GET", "POST"])
@login_required(login_url=reverse_lazy('jobauth:login'))
def job_detail(request, job_id):
    job = Job.objects.get(pk=job_id)
    if request.method == 'GET':
        statuses = JobStatus.objects.all()
        form = JobEditForm(initial={'status': job.status.id, 'applied_at': job.applied_at})
        return render(request, 'job_detail.html', context={'job': job,
                                                           'statuses': statuses, 'form': form})
    else:
        form = JobEditForm(request.POST)
        if form.is_valid():
            status_id = form.cleaned_data['status']
            applied_at = form.cleaned_data['applied_at']
            job.status_id = status_id
            job.applied_at = applied_at
            job.save()
            return redirect(reverse('job_track:job_detail', kwargs={'job_id': job.id}))
        else:
            statuses = JobStatus.objects.all()
            return render(request, 'job_detail.html', context={'job': job, 'statuses': statuses,
                                                               'form': form, 'errors': form.errors})

@require_http_methods(["GET", "POST"])
@login_required(login_url=reverse_lazy('jobauth:login'))
# 限制要登入才能訪問，且會跳轉到登入頁面
# reverse_lazy表延遲執行
def add(request):
    if request.method == "GET":
        statuses = JobStatus.objects.all()
        return render(request, 'add.html', context={'statuses': statuses})
    else:
        form = JobAddForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            company = form.cleaned_data.get('company')
            status_id = form.cleaned_data.get('status')
            content = form.cleaned_data.get('content')
            applied_at = form.cleaned_data.get('applied_at')
            job_link = form.cleaned_data.get('job_link')
            company_link = form.cleaned_data.get('company_link')
            job = Job.objects.create(title=title, company=company, status_id=status_id, applied_at=applied_at,
                                     content=content, job_link=job_link, company_link=company_link, user=request.user)
            return JsonResponse({'code': 200, 'message': '應徵職位建立成功!', 'data': {'job_id': job.id}})
        else:
            print("表單驗證失敗，錯誤訊息如下：")
            print(form.errors.as_json())
            return JsonResponse({'code': 400, 'message': '參數錯誤!'})

@require_GET
def search(request):
    # /search?q=xxx
    q = request.GET.get('q')
    # 從部落格標題及內容搜尋是否有相關資料
    jobs = Job.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).all()
    return render(request, 'index.html', context={'jobs': jobs})
