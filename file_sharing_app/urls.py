from django.urls import path
from .views import FileDownloadView, OpsFileUploadView, activate, client_user_login, client_user_signup, index, ops_login, signout
from .views import FileUploadView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('',index, name='home'),
    path('login/',ops_login, name='Opsignin'),
    # path('upload/', upload_file, name='upload_file'),
    path('signup/', client_user_signup, name='signup'),
    path('ops_signup/', client_user_signup, name='signup'),
    path('signout/', signout, name='signout'),
    path('api/upload/', FileUploadView.as_view(), name='api_upload_file'),
    path('ops-upload/', OpsFileUploadView.as_view(), name='ops-file-upload'),
    # path('verify-email/<str:token>/', verify_email, name='verify_email'),
    path('client-login/',client_user_login, name='client_login'),
    # path('download-file/<int:file_id>/', download_file, name='download_file'),
    # path('list-files/', list_files, name='list_files'),
    # path('download-secure/<str:signed_url>/', download_secure_file, name='download_secure_file'),
   path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
#    path('api/token/', obtain_auth_token, name='api_token'),
#    path('api/download/<int:file_id>/', FileDownloadView.as_view(), name='file_download'),
#    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('download-file/<int:file_id>/', FileDownloadView.as_view(), name='download-file'),
]
# "token": "89aae0fede1d29bd8ee452be6dd139cbdc37ec17"