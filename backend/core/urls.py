from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # módulos
    path('auth/', include('users.urls')),
    path('atividades/', include('atividades.urls')),
    path('respostas/', include('respostas.urls')),
    path('turmas/', include('turmas.urls')),

    # documentação
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
]