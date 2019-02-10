from django.db import models
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import AbstractUser
class UserInfo(AbstractUser):
    nid = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=25,verbose_name='昵称')
    telephone = models.CharField(max_length=11,verbose_name="电话",unique=True,null=True)
    avatar = models.FileField(upload_to='avatars/',default='/avatars/default.png')
    create_time = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    blog = models.OneToOneField(to='Blog',to_field='nid',null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.username

class Blog(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题',max_length=64)
    site = models.CharField(verbose_name='个人博客后缀',max_length=32,unique=True)
    theme = models.CharField(verbose_name='博客主题',max_length=32)

    def __str__(self):
        return self.title

class Category(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题',max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid',on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称',max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid',on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题',max_length=50)
    desc = models.CharField(verbose_name='文章描述',max_length=300)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name="创建时间",default=timezone.now)
    homeCategory = models.ForeignKey(to='Category',to_field="nid",null=True,on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="作者",to='UserInfo',to_field='nid',on_delete=models.CASCADE)
    tags = models.ManyToManyField(to='Tag',through='ArticleTag',through_fields=('article','tag'))

    def __str__(self):
        return self.title


class ArticleDetail(models.Model):
    nid = models.AutoField(primary_key=True)
    content = models.TextField()
    article = models.OneToOneField(to="Article",to_field='nid',on_delete=models.CASCADE)

class Comment(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='评论文章',to='Article',to_field='nid',on_delete=models.CASCADE)
    user  = models.ForeignKey(verbose_name='评论者',to='UserInfo',to_field='nid',on_delete=models.CASCADE)
    content = models.CharField(verbose_name='评论内容',max_length=255)
    create_time = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    parent_conment = models.ForeignKey('self',null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.content

class ArticleUpDown(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo',null=True,on_delete=models.CASCADE)
    article = models.ForeignKey('Article',null=True,on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = [('article','user'),]


class ArticleTag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章',to='Article',to_field='nid',on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name='标签',to='Tag',to_field='nid',on_delete=models.CASCADE)

    class Meta:
        unique_together = [('article','tag'),]
    def __str__(self):
        v = self.article.title+"———"+self.tag.title
        return v