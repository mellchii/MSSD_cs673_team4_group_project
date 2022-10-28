from django.urls import path
from . import views
from .views import updatePost, deletePost
from django.conf import settings
from django.conf.urls.static import static
 
# app_name = 'post'
urlpatterns = [
    path('project/<pk>/comment/<id>/delete', views.deleteComment, name='deleteComment'), 
    path('project/<pk>/comment/<id>/edit', views.editComment, name='editComment'), 
    path("", views.index, name="home"),
    path("tag/<slug:slug>", views.tagged, name='tagged'),
    path('vote/', views.vote, name='vote'),
    path('addProject/', views.addProjectToPSC, name='addProject'),
    path('project/<pk>',views.postDetailComment,name='postDetail'),
    path('project/edit/<pk>', updatePost.as_view(), name='editPost'), 
    path('project/<pk>/delete', views.deletePost, name='deletePost'), 
    path('project/<pk>/favorite', views.favoritePost, name='favoritePost'), 
    path('search', views.search, name="search")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
