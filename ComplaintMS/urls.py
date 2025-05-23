from django.urls import path
from . import views
from .views import reply_to_complaint,all_complaints_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('signin/', auth_views.LoginView.as_view(template_name='ComplaintMS/signin.html'), name='signin'),
    path('logout/', auth_views.LogoutView.as_view(template_name='ComplaintMS/logout.html'), name='logout'),
    path('password/', views.change_password, name='change_password'),
    path('passwords/', views.change_password_g, name='change_password_g'),
    path('counter/', views.counter, name='counter'),
    path('solved/', views.solved, name='solved'),
    path('reply/<int:complaint_id>/', reply_to_complaint, name='reply_to_complaint'),  # Corrected pattern
    path('login/', views.login, name='login'),
    path('download-users/', views.download_registered_users, name='download_users'),

    path('list/', views.list, name='list'),
    path('pdf/', views.pdf_viewer, name='view'),
    path('pdf_g/', views.pdf_viewer, name='view'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('slist/', views.slist),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('askme/', views.complaints, name='complaints'),
    path('allcomplaints/', views.allcomplaints, name='allcomplaints'),
    path('certificate/', views.certificate, name='certificate'),
    path('heat/', views.heat, name='heat'),

    ##
    path('career-roadmaps/', views.career_roadmaps, name='career_roadmaps'),
    path('career-talks/', views.career_talks, name='career_talks'),
    path('resources/', views.resources, name='resources'),
    # path('aptitude-test/', views.career_aptitude_test, name='aptitude_test'),
    path('seminars/', views.upcoming_seminars, name='seminars'),
    path('success-stories/', views.success_stories, name='success_stories'),

    # AJAX and utility URLs
    path('quick-suggestion/', views.quick_career_suggestion, name='quick_suggestion'),
    path('download/<int:resource_id>/', views.download_resource, name='download_resource'),
    path('register-seminar/<int:seminar_id>/', views.register_seminar, name='register_seminar'),

    ##
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='ComplaintMS/password_reset.html'), name='password_reset'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='ComplaintMS/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='ComplaintMS/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='ComplaintMS/password_reset_complete.html'), name='password_reset_complete'),
]
