from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required

def index(request):
    '''学习笔记的主页'''
    return render(request, 'learning_logs/index.html')
@login_required
def topics(request):
    '''显示所有主题。'''
    topics = Topic.objects.order_by('data_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    '''显示单个主题及其所有的条目'''
    topic = Topic.objects.get(id=topic_id)
    # 将获取到的与主题相关的条目，并根据data_added进行排序，减号表示按照降序排列
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    '''添加新的主题'''
    if request.method != 'POST':
        # 当请求不是post，那么就是get,所以给一个新的表单
        form = TopicForm()
    else:
        # 当是post请求的时候，对提交的post表单进行处理
        form = TopicForm(data=request.POST)
        #  方法is_valid核实用户填写了所有必不可少的字段，且输入的数据与要求的字段类型一致
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')
    # 将form表单的内容赋值给context
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    '''编辑现有条目'''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # 初次请求使用现有条目填充表单
        form = EntryForm(instance=entry)
    else:
        # 如果要是post的话，用原先的内容先填充表单，对后面post提交的内容进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
# Create your views here.
