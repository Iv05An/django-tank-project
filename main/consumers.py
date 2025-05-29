# # main/consumers.py
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from django.contrib.contenttypes.models import ContentType
# from .models import Article, Comment, LikeDislike
#
# # class ArticleConsumer(AsyncWebsocketConsumer):
# #     async def connect(self):
# #         self.slug = self.scope['url_route']['kwargs']['slug']
# #         self.room_group_name = f'article_{self.slug}'
# #
# #         await self.channel_layer.group_add(
# #             self.room_group_name,
# #             self.channel_name
# #         )
# #         await self.accept()
# #
# #     async def disconnect(self, close_code):
# #         await self.channel_layer.group_discard(
# #             self.room_group_name,
# #             self.channel_name
# #         )
# #
# #     async def article_update(self, event):
# #         # Отправляем обновление клиентам
# #         await self.send(text_data=json.dumps({
# #             'type': event['type'],
# #             'data': event['data']
# #         }, default=str))  # Добавляем default=str для корректной сериализации дат
# class ArticleConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.slug = self.scope['url_route']['kwargs']['slug']
#         self.group_name = f'article_{self.slug}'
#         print(f"WebSocket connected: group={self.group_name}")
#
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )
#         print(f"WebSocket disconnected: group={self.group_name}")
#
#     async def article_update(self, event):
#         data = event['data']
#         await self.send(text_data=json.dumps({
#             'type': 'article_update',
#             'data': data
#         }))
#     @database_sync_to_async
#     def get_article_data(self):
#         article = Article.objects.get(slug=self.slug)
#         comments = article.comments.all().values('id', 'username', 'content', 'created_at')
#         content_type = ContentType.objects.get_for_model(Article)
#         likes = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, value='like').count()
#         dislikes = LikeDislike.objects.filter(content_type=content_type, object_id=article.id, value='dislike').count()
#         # Предполагаем, что клиент передаёт IP через заголовки WebSocket
#         client_ip = self.scope['client'][0] if self.scope['client'] else None
#         user_liked = LikeDislike.objects.filter(
#             content_type=content_type,
#             object_id=article.id,
#             ip_address=client_ip,
#             value='like'
#         ).exists() if client_ip else False
#         user_disliked = LikeDislike.objects.filter(
#             content_type=content_type,
#             object_id=article.id,
#             ip_address=client_ip,
#             value='dislike'
#         ).exists() if client_ip else False
#         return {
#             'comments': [
#                 {
#                     'id': comment['id'],
#                     'username': comment['username'],
#                     'content': comment['content'],
#                     'created_at': str(comment['created_at']),
#                 } for comment in comments
#             ],
#             'likes': likes,
#             'dislikes': dislikes,
#             'user_liked': user_liked,
#             'user_disliked': user_disliked,
#         }


# main/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ArticleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.slug = self.scope['url_route']['kwargs']['slug']
        self.group_name = f'article_{self.slug}'
        print(f"WebSocket connected: group={self.group_name}")

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected: group={self.group_name}")

    async def article_update(self, event):
        data = event['data']
        await self.send(text_data=json.dumps({
            'type': 'article_update',
            'data': data
        }))