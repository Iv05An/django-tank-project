# from django.urls import path
# from .views import home, T34, IS3, enter, feedback_view
# from . import views
#
# urlpatterns = [
#     path('', home, name='home'),        # Главная страница
#     path('T34/', T34, name='T34'),      # Страница T34
#     path('IS3/', IS3, name='IS3'),      # Страница IS3
#     # path('login/', enter, name='login'),  # Добавляем маршрут для формы входа
#     path('feedback/', feedback_view, name='feedback'),
#     path('register/', enter, name='register'),
#
#     path('article/<slug:slug>/', views.article_detail, name='article_detail'),
#     path('add_comment/', views.add_comment, name='add_comment'),
#     path('toggle_like_dislike/', views.toggle_like_dislike, name='toggle_like_dislike')
# ]

from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    # path('T34/', views.T34, name='T34'),  # Страница Т-34 (заглушка)
    #path('IS3/', views.article_detail, {'slug': '3'}, name='IS3'),
    path('article/<str:slug>/', views.article_detail, name='article_detail'),
    path('feedback/', views.feedback_view, name='feedback'),  # Страница обратной связи
    path('register/', views.enter, name='register'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('toggle_like_dislike/', views.toggle_like_dislike, name='toggle_like_dislike'),
    path('test/<str:slug>/', views.test_route, name='test_route'),
    path('get_updates/<slug:slug>/', views.get_updates, name='get_updates'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)