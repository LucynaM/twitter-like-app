from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Tweet, Messages, Comments, MyUser

# Register your models here.
# admin.site.register(MyUser)


def change_to_banned(model_admin, request, query_set):
    query_set.update(banned=True)
change_to_banned.short_description = "Ustaw ban"


def unban(model_admin, request, query_set):
    query_set.update(banned=False)
unban.short_description = "Usuń ban"


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'from_user', 'to_user', 'banned')
    actions = (change_to_banned, unban, )


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name')


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'get_comments_nr', 'banned')
    actions = (change_to_banned, unban, )

    def get_comments_nr(self, obj):
        return obj.comments.count()

    get_comments_nr.short_description = 'liczba komentarzy'


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'tweet', 'banned')
    actions = (change_to_banned, unban, )