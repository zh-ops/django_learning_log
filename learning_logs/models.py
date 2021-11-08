from django.db import models

class Topic(models.Model):
    '''用户学习的主题'''
    text = models.CharField(max_length=200)
    data_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.text

class Entry(models.Model):
    '''学到的有关某个主题的具体知识。'''
    # .foreignkey是一个数据库术语，将每个条目关联到Topic，on_delete让删除主题时同时删除所有与之相关的条目。
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    # meta类用于存储用于管理模型的额外信息
    class meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return f"{self.text}"


# Create your models here.
