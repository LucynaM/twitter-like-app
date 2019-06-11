from django.shortcuts import render, redirect
from django.http import Http404
from django import forms
from django.views import View
from django.views.generic import DeleteView
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Tweet, MyUser, Messages
from .forms import EntryForm, LoginForm, SigninForm, CommentsForm, MessagesForm

def check_author(obj, request):
    if obj.user != request.user:
        raise Http404

class SignUpUser(View):
    """Sign up new user"""
    def get(self, request):
        form = SigninForm()
        ctx = {
            'form': form,
        }
        return render(request, 'twitter/signup.html', ctx)

    def post(self, request):
        form = SigninForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop('password2')
            user = MyUser.objects.create_user(username=form.cleaned_data['email'], **form.cleaned_data)
            login(request, user)
            return redirect('twitter:entries')
        ctx = {
            'form': form,
        }
        return render(request, 'twitter/signup.html', ctx)


class LoginUser(View):
    """Log in user"""
    def get(self, request):
        form = LoginForm()
        ctx = {
            'form': form
        }
        return render(request, 'twitter/login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        msg = ""
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('twitter:entries')
            else:
                msg = "błędny użytkownik lub hasło"

        ctx = {
            'form': form,
            'msg': msg,
        }
        return render(request, 'homework/login.html', ctx)


def logout_user(request):
    logout(request)
    return redirect('twitter:login')


class EntriesView(LoginRequiredMixin, View):
    """Display all entries"""
    def get(self, request):
        entries = Tweet.objects.exclude(banned=True).order_by('-edited_at')
        ctx = {
            'entries': entries,
        }
        return render(request, 'twitter/entries.html', ctx)


class EntryView(LoginRequiredMixin, View):
    """Display single entry"""
    def get(self, request, id):
        entry = Tweet.objects.get(pk=id)
        comments = entry.comments.exclude(banned=True).order_by('-edited_at')
        form = CommentsForm()
        ctx = {
            'entry': entry,
            'comments': comments,
            'form': form,
        }
        return render(request, 'twitter/entry.html', ctx)

    def post(self, request, id):
        entry = Tweet.objects.get(pk=id)
        form = CommentsForm(request.POST)
        user = MyUser.objects.get(username=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.tweet = entry
            comment.save()
            form = CommentsForm()
        comments = entry.comments.exclude(banned=True).order_by('-edited_at')
        ctx = {
            'form': form,
            'comments': comments,
            'entry': entry,
        }
        return render(request, 'twitter/entry.html', ctx)


class AddEntry(LoginRequiredMixin, View):
    """Add new entry"""
    def get(self, request):
        form = EntryForm()
        ctx = {
            'form': form,
        }
        return render(request, 'twitter/add_entry.html', ctx)

    def post(self, request):
        form = EntryForm(request.POST)
        if form.is_valid():
            user = request.user
            Tweet.objects.create(user=user, **form.cleaned_data)
            return redirect('twitter:entries')
        ctx = {
            'form': form,
        }
        return render(request, 'twitter/add_entry.html', ctx)


class EditEntry(LoginRequiredMixin, View):
    """Edit new entry"""
    def get(self, request, id):
        entry = Tweet.objects.get(pk=id)
        check_author(entry, request)
        form = EntryForm(instance=entry)
        ctx = {
            'form': form,
        }
        return render(request, 'twitter/edit_entry.html', ctx)

    def post(self, request, id):
        entry = Tweet.objects.get(pk=id)
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.cleaned_data['user'] = request.user
            form.save()
            return redirect('twitter:entry', id=id)
        ctx = {
            'form': form,
        }
        return render(request, 'twitter/edit_entry.html', ctx)


class UsersView(LoginRequiredMixin, View):
    """Display all users"""
    def get(self, request):
        users = MyUser.objects.all()
        ctx = {
            'users': users
        }
        return render(request, 'twitter/users.html', ctx)


class UserView(LoginRequiredMixin, View):
    """Display user details"""
    def get(self, request, id):
        show_user = MyUser.objects.get(pk=id)
        entries = show_user.entries.all()

        ctx = {
            'entries': entries,
            'show_user': show_user,
        }
        return render(request, 'twitter/user.html', ctx)


class EditUser(LoginRequiredMixin, View):
    def get(self, request):
        user = MyUser.objects.get(username=request.user)
        form = SigninForm(instance=user)
        ctx = {
            'form': form,
        }
        return render(request, 'twitter/edit_user.html', ctx)

    def post(self, request):
        user = MyUser.objects.get(username=request.user)
        form = SigninForm(request.POST, instance=user)
        if form.is_valid():
            user.username = form.cleaned_data['email']
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('twitter:entries')
        ctx = {
            'form': form,
        }
        return render(request, 'twitter/edit_user.html', ctx)


class MessagesView(LoginRequiredMixin, View):
    """Display user messages"""

    def get(self, request):
        user = MyUser.objects.get(username=request.user)
        from_messages = user.from_messages.exclude(banned=True).order_by('-created_at')
        to_messages = user.to_messages.exclude(banned=True).order_by('-created_at')
        ctx = {
            'from_messages': from_messages,
            'to_messages': to_messages,
        }
        return render(request, 'twitter/messages.html', ctx)


class MessageView(LoginRequiredMixin, View):
    """Display single message"""

    def get(self, request, id):
        message = Messages.objects.get(pk=id)
        if message.to_user == request.user:
            message.is_read = True
            message.save()
        form = MessagesForm()
        ctx = {
            'message': message,
            'form': form,
        }
        return render(request, 'twitter/message.html', ctx)

    def post(self, request, id):
        message = Messages.objects.get(pk=id)
        to_user = message.from_user
        from_user = MyUser.objects.get(username=request.user)
        form = MessagesForm(request.POST)
        if form.is_valid():
            Messages.objects.create(from_user=from_user, to_user=to_user, **form.cleaned_data)
            return redirect('twitter:messages')
        ctx = {
            'message': message,
            'form': form,
        }
        return render(request, 'twitter/message.html', ctx)


class AddMessage(LoginRequiredMixin, View):
    """Add new message"""

    def get(self, request):
        form = MessagesForm()
        form.fields['to_user'] = forms.ModelChoiceField(queryset=MyUser.objects.exclude(username=request.user), label='Do')
        ctx = {
            'form': form,
        }
        return render(request, 'twitter/add_message.html', ctx)

    def post(self, request):
        from_user = MyUser.objects.get(username=request.user)
        form = MessagesForm(request.POST)
        if form.is_valid():
            Messages.objects.create(from_user=from_user, **form.cleaned_data)
            return redirect('twitter:messages')
        ctx = {
            'form': form,
        }
        return render(request, 'twitter/add_message.html', ctx)

class AddMessageToUser(LoginRequiredMixin, View):
    """Add new message"""

    def get(self, request, pk):
        form = MessagesForm()
        ctx = {
            'form': form,
        }
        return render(request, 'twitter/add_message.html', ctx)

    def post(self, request, pk):
        from_user = MyUser.objects.get(username=request.user)
        to_user = MyUser.objects.get(pk=pk)
        form = MessagesForm(request.POST)
        if form.is_valid():
            Messages.objects.create(from_user=from_user, to_user=to_user, **form.cleaned_data)
            return redirect('twitter:messages')
        ctx = {
            'form': form,
        }
        return render(request, 'twitter/add_message.html', ctx)


class DeleteView(LoginRequiredMixin, View):
    """Delete user or entry"""

    @staticmethod
    def get_obj(obj, id):
        if obj == 'entry':
            to_delete = Tweet.objects.get(id=id)
        elif obj == 'user':
            to_delete = MyUser.objects.get(id=id)
        return to_delete

    def get(self, request, obj, id):
        to_delete = DeleteView.get_obj(obj, id)
        ctx = {
            'to_delete': to_delete,
        }
        return render(request, 'twitter/delete.html', ctx)

    def post(self, request, obj, id):
        if request.POST['submit'] == 'tak':
            to_delete = DeleteView.get_obj(obj, id)
            to_delete.delete()
        return redirect('twitter:entries')




