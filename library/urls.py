from django.conf.urls import url
from . import views

app_name = 'library'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^book/(?P<pk>[0-9]+)/$', views.BookDetailView.as_view(), name='detail'),
    url(r'^alltags/', views.alltags, name='alltags'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    url(r'^mybook/(?P<pk>[0-9]+)/$',views.MyBookView.as_view(),name='mybook'),
    url(r'^search/$', views.search, name='search'),
    url(r'^borrow/',views.borrow,name="borrow"),
]