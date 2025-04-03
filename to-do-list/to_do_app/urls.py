from django.urls import path, include


urlpatterns = [
   path('auth/', include('to_do_app.views.auth_views.urls')),
   path('users/', include('to_do_app.views.user_views.urls')),
   path('tasks/', include('to_do_app.views.task_views.urls')),
   path('categories/', include('to_do_app.views.category_views.urls')),
   path('reports/', include('to_do_app.views.report_views.urls')),
]
