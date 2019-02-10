from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(UserInfo)
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
#admin.site.register(ArticleDetail)
admin.site.register(ArticleUpDown)
admin.site.register(Comment)
admin.site.register(ArticleTag)

@admin.register(ArticleDetail)
class ContentAdmin(admin.ModelAdmin):
    class Media:
        js=(
            '/static/kindeditor/kindeditor-all.js',
            '/static/kindeditor/config.js',
            '/static/kindeditor/lang/zh-CN.js',
        )
