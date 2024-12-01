# from rest_framework import serializers
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from aiogram import Bot, Dispatcher, types
# import asyncio
#
# from bot.dispatcher import bot_2
#
#
# class MessageSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     phone_number = serializers.CharField(max_length=15)
#     message = serializers.CharField(max_length=500)
#
#
# async def send_telegram_message(name, phone_number, message):
#     try:
#         await bot_2.send_message(
#             chat_id=-1002296752741,
#             text=f"""
# Ism: {name}
# Telefon raqam: {phone_number}
#
# Xabar: {message}"""
#         )
#     except Exception as e:
#         await bot_2.send_message(
#             chat_id=1974800905,
#             text=f"""
# Ism: {name}
# Telefon raqam: {phone_number}
#
# Xabar: {message}
#
# Exception: {e}"""
#         )
#
#
# class MessageAPIView(APIView):
#     permission_classes = [AllowAny]
#
#     def get(self, request):
#         serializer = MessageSerializer(data=request.query_params)
#         if serializer.is_valid():
#             name = serializer.validated_data['name']
#             phone_number = serializer.validated_data['phone_number']
#             message = serializer.validated_data['message']
#
#             asyncio.run(send_telegram_message(name, phone_number, message))
#
#             return Response({
#                 "status": "success",
#                 "data": serializer.validated_data
#             })
#         return Response({"status": "error", "errors": serializer.errors})
#
#
# from django.shortcuts import render
#
#
# def index(request):
#     return render(request, 'alabaratory-main/index.html')
