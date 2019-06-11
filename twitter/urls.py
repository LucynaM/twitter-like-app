
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import EntriesView, AddEntry, LoginUser, SignUpUser, logout_user, UserView, EditUser, UsersView, EntryView, \
    MessagesView, AddMessage, AddMessageToUser, MessageView, EditEntry, DeleteView

urlpatterns = [
    url(r'^$', EntriesView.as_view(), name="entries"),
    url(r'^add_entry/$', AddEntry.as_view(), name="add_entry"),
    url(r'^edit_entry/(?P<id>(\d)+)/$', EditEntry.as_view(), name="edit_entry"),
    url(r'^login/$', LoginUser.as_view(), name="login"),
    url(r'^logout/$', logout_user, name="logout"),
    url(r'^sign_up/$', SignUpUser.as_view(), name="sign_up"),
    url(r'^user_details/(?P<id>(\d)+)/$', UserView.as_view(), name="user_details"),
    url(r'^users/$', UsersView.as_view(), name="users"),
    url(r'^edit_user/$', EditUser.as_view(), name="edit_user"),
    url(r'^entry/(?P<id>(\d)+)/$', EntryView.as_view(), name="entry"),
    url(r'^messages/$', MessagesView.as_view(), name="messages"),
    url(r'^add_message/$', AddMessage.as_view(), name="add_message"),
    url(r'^add_message/(?P<pk>(\d)+)$', AddMessageToUser.as_view(), name="add_message_to_user"),
    url(r'^message/(?P<id>(\d)+)/$', MessageView.as_view(), name="message"),
    url(r'^delete/(?P<obj>([a-zA-z0-9\-])+)/(?P<id>(\d)+)/$', DeleteView.as_view(), name="delete"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
