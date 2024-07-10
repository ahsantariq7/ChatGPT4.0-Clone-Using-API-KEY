import openai
from django.shortcuts import render
from django.http import JsonResponse
from chatgpt_project.settings import OPENAI_API_KEY
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Chat, Message
from django.views.decorators.csrf import csrf_exempt

openai.api_key = OPENAI_API_KEY


@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        chat_name = request.POST.get("chat_name")

        # Create or get the chat session
        chat, created = Chat.objects.get_or_create(name=chat_name)

        # Save user message
        user_message = Message.objects.create(
            chat=chat, sender="user", content=user_input
        )

        # Construct conversation history
        messages = chat.messages.all()
        conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        for msg in messages:
            conversation.append(
                {
                    "role": "user" if msg.sender == "user" else "assistant",
                    "content": msg.content,
                }
            )

        # Get response from GPT-4
        response = openai.ChatCompletion.create(model="gpt-4", messages=conversation)
        gpt_response = response["choices"][0]["message"]["content"]

        # Save GPT-4 response
        gpt_message = Message.objects.create(
            chat=chat, sender="assistant", content=gpt_response
        )

        return JsonResponse({"response": gpt_response})

    chats = Chat.objects.all()
    return render(request, "chat/chat.html", {"chats": chats})


@csrf_exempt
def chat_history(request, chat_name):
    chat = get_object_or_404(Chat, name=chat_name)
    messages = chat.messages.all()
    return JsonResponse(
        {
            "messages": [
                {"sender": msg.sender, "content": msg.content} for msg in messages
            ]
        }
    )
