# import requests
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponseRedirect, JsonResponse
# from django.urls import reverse
# from .forms import RegistrationForm, CommentForm
# import json
# from django.contrib.contenttypes.models import ContentType
# from .models import Article, Comment, LikeDislike
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
#
# def get_updates(request, slug):
#     article = get_object_or_404(Article, slug=slug)
#     comments = article.comments.all().values('id', 'username', 'content', 'created_at')
#     content_type = ContentType.objects.get_for_model(Article)
#     client_ip = request.META.get('REMOTE_ADDR')
#     likes = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, value='like').count()
#     dislikes = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, value='dislike').count()
#     user_liked = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, ip_address=client_ip, value='like').exists()
#     user_disliked = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, ip_address=client_ip, value='dislike').exists()
#
#     return JsonResponse({
#         'status': 'success',
#         'comments': list(comments),
#         'likes': likes,
#         'dislikes': dislikes,
#         'user_liked': user_liked,
#         'user_disliked': user_disliked,
#     })
#
# def enter(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             print(f"Пользователь {user.username} успешно создан")
#             return redirect('home')
#         else:
#             print("Форма не прошла валидацию. Ошибки:", form.errors)
#             article = get_object_or_404(Article, slug='is-3')  # Get ИС-3 article
#             return render(request, 'main/enter.html', {'form': form, 'form_errors': form.errors, 'article': article})
#     else:
#         form = RegistrationForm()
#     article = get_object_or_404(Article, slug='is-3')  # Get ИС-3 article
#     return render(request, 'main/enter.html', {'form': form, 'article': article})
#
# # def home(request):
# #     return render(request, 'main/home.html')
#
# def home(request):
#     article = get_object_or_404(Article, slug='is-3')  # Get ИС-3 article
#     return render(request, 'main/home.html', {'article': article})
#
# def T34(request):
#     article = get_object_or_404(Article, slug='is-3')  # Get ИС-3 article
#     return render(request, 'main/T34.html', {'article': article})
#
# TELEGRAM_BOT_TOKEN = "7177110452:AAEoDQ4JosXm86Pw77ZdxqRi2NeU8pwccG8"
# TELEGRAM_CHAT_ID = "1938946607"
#
# def send_telegram_message(message):
#     url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
#     payload = {
#         "chat_id": TELEGRAM_CHAT_ID,
#         "text": message,
#         "parse_mode": "HTML"
#     }
#     response = requests.post(url, json=payload)
#     return response.json()
#
# def feedback_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         message = request.POST.get('message')
#         errors = {}
#
#         if not name:
#             errors['name'] = 'Введите ваше имя'
#         if not email or '@' not in email:
#             errors['email'] = 'Введите корректный email'
#         if not message:
#             errors['message'] = 'Введите сообщение'
#
#         if errors:
#             article = get_object_or_404(Article, slug='is-3')  # Get ИС-3 article
#             return render(request, 'main/feedback.html', {'form_errors': errors, 'article': article})
#
#         telegram_message = (
#             f"<b>Новое сообщение обратной связи</b>\n"
#             f"Имя: {name}\n"
#             f"Email: {email}\n"
#             f"Сообщение: {message}"
#         )
#
#         telegram_response = send_telegram_message(telegram_message)
#         if telegram_response.get("ok"):
#             return HttpResponseRedirect(reverse('home'))
#         else:
#             errors['message'] = 'Ошибка отправки сообщения в Telegram'
#             article = get_object_or_404(Article, slug='is-3')  # Get ИС-3 article
#             return render(request, 'main/feedback.html', {'form_errors': errors, 'article': article})
#     article = get_object_or_404(Article, slug='is-3')  # Get ИС-3 article
#     return render(request, 'main/feedback.html', {'article': article})
#
# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip
#
# # main/views.py
# def article_detail(request, slug):
#     print(f"Processing slug: {slug}")
#     article = get_object_or_404(Article, slug=slug)
#     comments = article.comments.all()
#     comment_form = CommentForm()
#     content_type = ContentType.objects.get_for_model(Article)
#     client_ip = get_client_ip(request)
#     likes = LikeDislike.objects.filter(
#         content_type=content_type,
#         object_id=article.id,
#         value='like'
#     ).count()
#     dislikes = LikeDislike.objects.filter(
#         content_type=content_type,
#         object_id=article.id,
#         value='dislike'
#     ).count()
#     user_liked = LikeDislike.objects.filter(
#         content_type=content_type,
#         object_id=article.id,
#         ip_address=client_ip,
#         value='like'
#     ).exists()
#     user_disliked = LikeDislike.objects.filter(
#         content_type=content_type,
#         object_id=article.id,
#         ip_address=client_ip,
#         value='dislike'
#     ).exists()
#
#     context = {
#         'article': article,
#         'comments': comments,
#         'comment_form': comment_form,
#         'likes': likes,
#         'dislikes': dislikes,
#         'user_liked': user_liked,
#         'user_disliked': user_disliked,
#         'content_type_id': content_type.id,
#     }
#     print("Context:", context)
#     try:
#         return render(request, 'main/IS3.html', context)
#     except Exception as e:
#         print(f"Error rendering template: {str(e)}")
#         raise
#
# # main/views.py
# def add_comment(request):
#     if request.method != 'POST':
#         return JsonResponse({'status': 'error', 'message': 'Метод не разрешён'}, status=405)
#
#     try:
#         data = json.loads(request.body)
#         article_id = data.get('article_id')
#         username = data.get('username')
#         content = data.get('content')
#
#         if not article_id or not username or not content:
#             return JsonResponse({'status': 'error', 'message': 'Все поля обязательны'}, status=400)
#
#         article = get_object_or_404(Article, id=article_id)
#         comment = Comment.objects.create(
#             article=article,
#             username=username,
#             content=content
#         )
#
#         # Получаем полный список комментариев
#         comments = article.comments.all().values('id', 'username', 'content', 'created_at')
#         comments_data = [
#             {
#                 'id': c['id'],
#                 'username': c['username'],
#                 'content': c['content'],
#                 'created_at': str(c['created_at']),
#             } for c in comments
#         ]
#
#         # Отправка обновления через WebSocket
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             f'article_{article.slug}',
#             {
#                 'type': 'article_update',
#                 'data': {
#                     'comments': comments_data,
#                     'likes': LikeDislike.objects.filter(content_type=ContentType.objects.get_for_model(Article), object_id=article.id, value='like').count(),
#                     'dislikes': LikeDislike.objects.filter(content_type=ContentType.objects.get_for_model(Article), object_id=article.id, value='dislike').count(),
#                 }
#             }
#         )
#
#         return JsonResponse({
#             'status': 'success',
#             'comment': {
#                 'id': comment.id,
#                 'username': comment.username,
#                 'content': comment.content,
#                 'created_at': str(comment.created_at),
#             }
#         })
#     except Exception as e:
#         return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
#
# def toggle_like_dislike(request):
#     if request.method != 'POST':
#         return JsonResponse({'status': 'error', 'message': 'Метод не разрешён'}, status=405)
#
#     try:
#         data = json.loads(request.body)
#         content_type_id = data.get('content_type_id')
#         object_id = data.get('object_id')
#         action = data.get('action')
#
#         print('Received data:', data)
#
#         if not content_type_id or not object_id or not action:
#             missing_fields = []
#             if not content_type_id:
#                 missing_fields.append('content_type_id')
#             if not object_id:
#                 missing_fields.append('object_id')
#             if not action:
#                 missing_fields.append('action')
#             return JsonResponse({
#                 'status': 'error',
#                 'message': f'Отсутствуют обязательные поля: {", ".join(missing_fields)}'
#             }, status=400)
#
#         content_type_id = int(content_type_id)
#         object_id = int(object_id)
#
#         content_type = get_object_or_404(ContentType, id=content_type_id)
#         if content_type.model_class() != Article:
#             return JsonResponse({
#                 'status': 'error',
#                 'message': 'content_type не соответствует модели Article'
#             }, status=400)
#
#         obj = get_object_or_404(Article, id=object_id)
#         client_ip = get_client_ip(request)
#
#         existing = LikeDislike.objects.filter(
#             content_type=content_type,
#             object_id=object_id,
#             ip_address=client_ip
#         ).first()
#
#         if existing:
#             if existing.value == action:
#                 existing.delete()
#                 action_taken = 'removed'
#             else:
#                 existing.value = action
#                 existing.save()
#                 action_taken = 'updated'
#         else:
#             LikeDislike.objects.create(
#                 content_type=content_type,
#                 object_id=object_id,
#                 ip_address=client_ip,
#                 value=action
#             )
#             action_taken = 'added'
#
#         likes = LikeDislike.objects.filter(
#             content_type=content_type,
#             object_id=object_id,
#             value='like'
#         ).count()
#         dislikes = LikeDislike.objects.filter(
#             content_type=content_type,
#             object_id=object_id,
#             value='dislike'
#         ).count()
#
#         user_liked = LikeDislike.objects.filter(
#             content_type=content_type,
#             object_id=object_id,
#             ip_address=client_ip,
#             value='like'
#         ).exists()
#         user_disliked = LikeDislike.objects.filter(
#             content_type=content_type,
#             object_id=object_id,
#             ip_address=client_ip,
#             value='dislike'
#         ).exists()
#
#         print(f"Sending to group: article_{obj.slug}")
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             f'article_{obj.slug}',
#             {
#                 'type': 'article_update',
#                 'data': {
#                     'comments': [
#                         {
#                             'id': c['id'],
#                             'username': c['username'],
#                             'content': c['content'],
#                             'created_at': str(c['created_at']),
#                         } for c in obj.comments.all().values('id', 'username', 'content', 'created_at')
#                     ],
#                     'likes': likes,
#                     'dislikes': dislikes,
#                     'user_liked': user_liked,
#                     'user_disliked': user_disliked,
#                 }
#             }
#         )
#
#         return JsonResponse({
#             'status': 'success',
#             'action': action_taken,
#             'likes': likes,
#             'dislikes': dislikes,
#             'user_liked': user_liked,
#             'user_disliked': user_disliked,
#         })
#     except ValueError as e:
#         print(f"ValueError in toggle_like_dislike: {str(e)}")
#         return JsonResponse({'status': 'error', 'message': f'ValueError: {str(e)}'}, status=400)
#     except Exception as e:
#         print(f"Error in toggle_like_dislike: {str(e)}")
#         return JsonResponse({'status': 'error', 'message': f'Internal Server Error: {str(e)}'}, status=500)


import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import RegistrationForm, CommentForm
import json
from django.contrib.contenttypes.models import ContentType
from .models import Article, Comment, LikeDislike
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
from django.views.decorators.csrf import csrf_exempt

def get_updates(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comments = article.comments.all().values('id', 'username', 'content', 'created_at')
    content_type = ContentType.objects.get_for_model(Article)
    client_ip = request.META.get('REMOTE_ADDR')
    likes = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, value='like').count()
    dislikes = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, value='dislike').count()
    user_liked = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, ip_address=client_ip, value='like').exists()
    user_disliked = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, ip_address=client_ip, value='dislike').exists()

    return JsonResponse({
        'status': 'success',
        'comments': list(comments),
        'likes': likes,
        'dislikes': dislikes,
        'user_liked': user_liked,
        'user_disliked': user_disliked,
    })

def enter(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"Пользователь {user.username} успешно создан")
            return redirect('home')
        else:
            print("Форма не прошла валидацию. Ошибки:", form.errors)
            return render(request, 'main/enter.html', {'form': form, 'form_errors': form.errors})
    else:
        form = RegistrationForm()
    return render(request, 'main/enter.html', {'form': form})

def home(request):
    return render(request, 'main/home.html')  # Без статьи

# def T34(request):
#     article = get_object_or_404(Article, slug='is-3')  # Get ИС-3 article
#     return render(request, 'main/T34.html', {'article': article})

# def T34(request):
#     article = get_object_or_404(Article, slug='t-34')  # Статья t-34
#     comments = article.comments.all()
#     comment_form = CommentForm()
#     content_type = ContentType.objects.get_for_model(Article)
#     client_ip = get_client_ip(request)
#     likes = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, value='like').count()
#     dislikes = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, value='dislike').count()
#     user_liked = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, ip_address=client_ip, value='like').exists()
#     user_disliked = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, ip_address=client_ip, value='dislike').exists()
#
#     context = {
#         'article': article,
#         'comments': comments,
#         'comment_form': comment_form,
#         'likes': likes,
#         'dislikes': dislikes,
#         'user_liked': user_liked,
#         'user_disliked': user_disliked,
#         'content_type_id': content_type.id,
#     }
#     return render(request, 'main/T34.html', context)

TELEGRAM_BOT_TOKEN = "7177110452:AAEoDQ4JosXm86Pw77ZdxqRi2NeU8pwccG8"
TELEGRAM_CHAT_ID = "1938946607"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    return response.json()

def feedback_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        errors = {}

        if not name:
            errors['name'] = 'Введите ваше имя'
        if not email or '@' not in email:
            errors['email'] = 'Введите корректный email'
        if not message:
            errors['message'] = 'Введите сообщение'

        if errors:
            return render(request, 'main/feedback.html', {'form_errors': errors})

        telegram_message = (
            f"<b>Новое сообщение обратной связи</b>\n"
            f"Имя: {name}\n"
            f"Email: {email}\n"
            f"Сообщение: {message}"
        )

        telegram_response = send_telegram_message(telegram_message)
        if telegram_response.get("ok"):
            return HttpResponseRedirect(reverse('home'))
        else:
            errors['message'] = 'Ошибка отправки сообщения в Telegram'
            return render(request, 'main/feedback.html', {'form_errors': errors})
    return render(request, 'main/feedback.html')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

logger = logging.getLogger(__name__)

def test_route(request, slug):
    logger.info(f"Test route hit for slug: {slug}")
    return JsonResponse({'status': 'success', 'message': f'Test route for {slug}'})
    
def article_detail(request, slug):
    logger.info(f"Processing slug: {slug}")
    article = get_object_or_404(Article, slug=slug)
    comments = article.comments.all()
    comment_form = CommentForm()
    content_type = ContentType.objects.get_for_model(Article)
    client_ip = get_client_ip(request)
    likes = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, value='like').count()
    dislikes = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, value='dislike').count()
    user_liked = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, ip_address=client_ip, value='like').exists()
    user_disliked = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, ip_address=client_ip, value='dislike').exists()

    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'likes': likes,
        'dislikes': dislikes,
        'user_liked': user_liked,
        'user_disliked': user_disliked,
        'content_type_id': content_type.id,
    }
    logger.info(f"Context: {context}")
    try:
        if slug == 't-34':
            template = 'main/T34.html'
        elif slug == 'is-3':
            template = 'main/IS3.html'
        else:
            template = 'main/IS3.html'
        logger.info(f"Using template: {template}")
        return render(request, template, context)
    except Exception as e:
        logger.error(f"Ошибка при рендеринге шаблона: {str(e)}")
        raise
# def add_comment(request):
#     if request.method != 'POST':
#         return JsonResponse({'status': 'error', 'message': 'Метод не разрешён'}, status=405)
#
#     try:
#         data = json.loads(request.body)
#         article_id = data.get('article_id')
#         username = data.get('username')
#         content = data.get('content')
#
#         if not article_id or not username or not content:
#             return JsonResponse({'status': 'error', 'message': 'Все поля обязательны'}, status=400)
#
#         article = get_object_or_404(Article, id=article_id)
#         comment = Comment.objects.create(
#             article=article,
#             username=username,
#             content=content
#         )
#
#         comments = article.comments.all().values('id', 'username', 'content', 'created_at')
#         comments_data = [
#             {
#                 'id': c['id'],
#                 'username': c['username'],
#                 'content': c['content'],
#                 'created_at': str(c['created_at']),
#             } for c in comments
#         ]
#
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             f'article_{article.slug}',
#             {
#                 'type': 'article_update',
#                 'data': {
#                     'comments': comments_data,
#                     'likes': LikeDislike.objects.filter(content_type=ContentType.objects.get_for_model(Article), object_id=article.id, value='like').count(),
#                     'dislikes': LikeDislike.objects.filter(content_type=ContentType.objects.get_for_model(Article), object_id=article.id, value='dislike').count(),
#                 }
#             }
#         )
#
#         return JsonResponse({
#             'status': 'success',
#             'comment': {
#                 'id': comment.id,
#                 'username': comment.username,
#                 'content': comment.content,
#                 'created_at': str(comment.created_at),
#             }
#         })
#     except Exception as e:
#         return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
#
# def toggle_like_dislike(request):
#     if request.method != 'POST':
#         return JsonResponse({'status': 'error', 'message': 'Метод не разрешён'}, status=405)
#
#     try:
#         data = json.loads(request.body)
#         content_type_id = data.get('content_type_id')
#         object_id = data.get('object_id')
#         action = data.get('action')
#
#         print('Received data:', data)
#
#         if not content_type_id or not object_id or not action:
#             missing_fields = []
#             if not content_type_id:
#                 missing_fields.append('content_type_id')
#             if not object_id:
#                 missing_fields.append('object_id')
#             if not action:
#                 missing_fields.append('action')
#             return JsonResponse({
#                 'status': 'error',
#                 'message': f'Отсутствуют обязательные поля: {", ".join(missing_fields)}'
#             }, status=400)
#
#         content_type_id = int(content_type_id)
#         object_id = int(object_id)
#
#         content_type = get_object_or_404(ContentType, id=content_type_id)
#         if content_type.model_class() != Article:
#             return JsonResponse({
#                 'status': 'error',
#                 'message': 'content_type не соответствует модели Article'
#             }, status=400)
#
#         obj = get_object_or_404(Article, id=object_id)
#         client_ip = get_client_ip(request)
#
#         existing = LikeDislike.objects.filter(
#             content_type=content_type,
#             object_id=object_id,
#             ip_address=client_ip
#         ).first()
#
#         if existing:
#             if existing.value == action:
#                 existing.delete()
#                 action_taken = 'removed'
#             else:
#                 existing.value = action
#                 existing.save()
#                 action_taken = 'updated'
#         else:
#             LikeDislike.objects.create(
#                 content_type=content_type,
#                 object_id=object_id,
#                 ip_address=client_ip,
#                 value=action
#             )
#             action_taken = 'added'
#
#         likes = LikeDislike.objects.filter(
#             content_type=content_type,
#             object_id=object_id,
#             value='like'
#         ).count()
#         dislikes = LikeDislike.objects.filter(
#             content_type=content_type,
#             object_id=object_id,
#             value='dislike'
#         ).count()
#
#         user_liked = LikeDislike.objects.filter(
#             content_type=content_type,
#             object_id=object_id,
#             ip_address=client_ip,
#             value='like'
#         ).exists()
#         user_disliked = LikeDislike.objects.filter(
#             content_type=content_type,
#             object_id=object_id,
#             ip_address=client_ip,
#             value='dislike'
#         ).exists()
#
#         print(f"Sending to group: article_{obj.slug}")
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             f'article_{obj.slug}',
#             {
#                 'type': 'article_update',
#                 'data': {
#                     'comments': [
#                         {
#                             'id': c['id'],
#                             'username': c['username'],
#                             'content': c['content'],
#                             'created_at': str(c['created_at']),
#                         } for c in obj.comments.all().values('id', 'username', 'content', 'created_at')
#                     ],
#                     'likes': likes,
#                     'dislikes': dislikes,
#                     'user_liked': user_liked,
#                     'user_disliked': user_disliked,
#                 }
#             }
#         )
#
#         return JsonResponse({
#             'status': 'success',
#             'action': action_taken,
#             'likes': likes,
#             'dislikes': dislikes,
#             'user_liked': user_liked,
#             'user_disliked': user_disliked,
#         })
#     except ValueError as e:
#         print(f"ValueError in toggle_like_dislike: {str(e)}")
#         return JsonResponse({'status': 'error', 'message': f'ValueError: {str(e)}'}, status=400)
#     except Exception as e:
#         print(f"Error in toggle_like_dislike: {str(e)}")
#         return JsonResponse({'status': 'error', 'message': f'Internal Server Error: {str(e)}'}, status=500)

@csrf_exempt  # Замени на CSRF-проверку в продакшене
def toggle_like_dislike(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        content_type_id = data.get('content_type_id')
        object_id = data.get('object_id')
        action = data.get('action')
        # Логика лайков/дизлайков (замени на свою)
        return JsonResponse({
            'status': 'success',
            'likes': 1,  # Пример
            'dislikes': 0,
            'user_liked': action == 'like',
            'user_disliked': action == 'dislike',
        })
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt  # Замени на CSRF-проверку в продакшене
def add_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        article_id = data.get('article_id')
        username = data.get('username')
        content = data.get('content')
        # Логика добавления комментария (замени на свою)
        return JsonResponse({'status': 'success', 'message': 'Комментарий добавлен'})
    return JsonResponse({'status': 'error'}, status=400)