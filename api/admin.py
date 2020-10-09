from django.contrib import admin

from .models import Review, Comment


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("text", "pub_date", "author", "title", "score")
    search_fields = ("author",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "pub_date", "author", "review")
    search_fields = ("author",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
