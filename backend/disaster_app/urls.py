from django.urls import path
from . import views

urlpatterns = [

    
    # Home
    path("", views.home, name="home"),

    # Authentication
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),

    # User
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("history/", views.history, name="history"),
    path("notifications/", views.notifications, name="notifications"),

    # Disaster Information
    path("alerts/", views.alerts, name="alerts"),
    path("checklist/", views.checklist, name="checklist"),
    path("resources/", views.resources, name="resources"),

    
    # Emergency
    path("emergency/", views.emergency, name="emergency"),
    path("emergency-sos/", views.emergency_sos, name="emergency_sos"),

    # Admin
    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # SOS
    path(
        "update-status/<str:sos_id>/<str:status>/",
        views.update_sos_status,
        name="update_sos_status",
    ),

    path("manage-sos/", views.manage_sos, name="manage_sos"),
    path("delete-sos/<str:sos_id>/", views.delete_sos, name="delete_sos"),

    # Users
    path("manage-users/", views.manage_users, name="manage_users"),
    path("delete-user/<str:user_id>/", views.delete_user, name="delete_user"),

    # Alerts
    path("manage-alerts/", views.manage_alerts, name="manage_alerts"),
    path("add-alert/", views.add_alert, name="add_alert"),
    path("delete-alert/<str:alert_id>/", views.delete_alert, name="delete_alert"),

    # Resources
    path("manage-resources/", views.manage_resources, name="manage_resources"),
    path("add-resource/", views.add_resource, name="add_resource"),
    path("edit-resource/<str:resource_id>/", views.edit_resource, name="edit_resource"),
    path("delete-resource/<str:resource_id>/", views.delete_resource, name="delete_resource"),

    # Checklist
    path("manage-checklist/", views.manage_checklist, name="manage_checklist"),
    path("add-checklist/", views.add_checklist, name="add_checklist"),
    path("edit-checklist/<str:item_id>/", views.edit_checklist, name="edit_checklist"),
    path("delete-checklist/<str:item_id>/", views.delete_checklist, name="delete_checklist"),

    # Static Pages
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]