# from django.shortcuts import get_object_or_404, render, redirect
# from django.views.generic import FormView, DetailView
# from ..models.message import Message
# from ..models.chat import Chat
# from ..forms.message import MessageCreateForm
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse_lazy
# from django.http import JsonResponse


# class MessageCreateView(LoginRequiredMixin, FormView):
#     form_class = MessageCreateForm
#     template_name = "chats/chat_detail.html"

#     def form_valid(self, form):
#         chat = get_object_or_404(Chat, pk=self.kwargs["pk"])
#         message = form.save(commit=False)
#         message.sender = self.request.user
#         message.chat = chat
#         message.save()

#         return JsonResponse({"success": True})


# def create_message(request, chat_pk):
#     chat = get_object_or_404(Chat, pk=chat_pk)

#     if request.method == "POST":
#         form = MessageCreateForm(request.POST, request.FILES)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             message.chat = chat
#             message.save()
#             return JsonResponse({"success": True})
#         else:
#             return JsonResponse({"success": False, "errors": form.errors}, status=400)
#     else:
#         form = MessageCreateForm()

#     return render(request, "your_template.html", {"form": form, "chat": chat})
