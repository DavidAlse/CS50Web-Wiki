from django.urls import path, include


from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("newPage", views.newPage, name="newPage"),
    path("randomPage", views.randomPage, name="randomPage"),
    
]
