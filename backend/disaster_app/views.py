from django.shortcuts import render, redirect
from datetime import datetime
import bcrypt
from bson import ObjectId
from mongoengine.queryset.visitor import Q

from .alert_model import Alert
from .user_model import User
from .checklist_model import Checklist
from .resource_model import Resource
from .emergency_model import Emergency
from .sos_model import SOSRequest
from .notification_model import Notification
from .disaster_mapping import get_disaster
from .broadcast_engine import start_broadcast


# HELPER FUNCTIONS

def login_required(request):
    if "user_id" not in request.session:
        return redirect("/login/")
    return None


def admin_required(request):
    if "admin_id" not in request.session:
        return redirect("/login/")
    return None


def create_notification(title, message):
    Notification(
        title=title,
        message=message,
        created_at=datetime.now()
    ).save()


# HOME

def home(request):
    return render(request, "disaster_app/home.html")


# REGISTER


def register(request):

    if request.method == "POST":

        if User.objects(email=request.POST["email"]).first():
            return render(
                request,
                "disaster_app/register.html",
                {"error": "Email already exists"}
            )

        password = bcrypt.hashpw(
            request.POST["password"].encode(),
            bcrypt.gensalt()
        ).decode()

        User(
            name=request.POST["name"],
            email=request.POST["email"],
            password=password,
            phone=request.POST["phone"],
            location=request.POST["location"],
            role="user",
            created_at=datetime.now()
        ).save()

        return redirect("/login/")

    return render(request, "disaster_app/register.html")



# LOGIN


def login(request):

    if request.method == "POST":

        user = User.objects(
            email=request.POST["email"]
        ).first()

        if user and bcrypt.checkpw(
            request.POST["password"].encode(),
            user.password.encode()
        ):

            if user.role == "admin":
                request.session["admin_id"] = str(user.id)
                request.session["admin_name"] = user.name
                return redirect("/admin-dashboard/")

            request.session["user_id"] = str(user.id)
            request.session["user_name"] = user.name
            request.session["email"] = user.email

            return redirect("/dashboard/")

        return render(
            request,
            "disaster_app/login.html",
            {"error": "Invalid Email or Password"}
        )

    return render(request, "disaster_app/login.html")


# LOGOUT

def logout(request):
    request.session.flush()
    return redirect("/")


# PROFILE

def profile(request):

    check = login_required(request)
    if check:
        return check

    user = User.objects(
        id=ObjectId(request.session["user_id"])
    ).first()

    return render(
        request,
        "disaster_app/profile.html",
        {"user": user}
    )


# USER DASHBOARD

def dashboard(request):

    check = login_required(request)
    if check:
        return check

    return render(
        request,
        "disaster_app/dashboard.html",
        {
            "name": request.session["user_name"],
            "alert_count": Alert.objects.count(),
            "resource_count": Resource.objects.count(),
            "history_count": SOSRequest.objects(
                name=request.session["user_name"]
            ).count(),
            "emergency_count": Emergency.objects(
                user_name=request.session["user_name"]
            ).count()
        }
    )


# ALERTS

def alerts(request):

    check = login_required(request)
    if check:
        return check

    disaster_type = request.GET.get("type", "")
    severity = request.GET.get("severity", "")

    alert_list = Alert.objects()

    if disaster_type:
        alert_list = alert_list.filter(disaster_type=disaster_type)

    if severity:
        alert_list = alert_list.filter(severity=severity)

    alert_list = alert_list.order_by("-created_at")

    return render(
        request,
        "disaster_app/alerts.html",
        {
            "alerts": alert_list,
            "selected_type": disaster_type,
            "selected_severity": severity
        }
    )


# DELETE ALERT


def delete_alert(request, alert_id):

    check = admin_required(request)
    if check:
        return check

    alert = Alert.objects(id=ObjectId(alert_id)).first()

    if alert:
        alert.delete()

    return redirect("/manage-alerts/")

# CHECKLIST


def checklist(request):

    check = login_required(request)
    if check:
        return check

    checklist_items = Checklist.objects().order_by("category")

    return render(
        request,
        "disaster_app/checklist.html",
        {
            "checklist": checklist_items
        }
    )


# ADD CHECKLIST

def add_checklist(request):

    check = admin_required(request)
    if check:
        return check

    if request.method == "POST":

        Checklist(
            item=request.POST["item"],
            category=request.POST["category"],
            completed=False
        ).save()

        return redirect("/manage-checklist/")

    return render(request, "disaster_app/add_checklist.html")

# EDIT CHECKLIST
def edit_checklist(request, item_id):

    check = admin_required(request)
    if check:
        return check

    checklist = Checklist.objects(id=ObjectId(item_id)).first()

    if not checklist:
        return redirect("/manage-checklist/")

    if request.method == "POST":

        checklist.item = request.POST["item"]
        checklist.category = request.POST["category"]

        checklist.save()

        return redirect("/manage-checklist/")

    return render(
        request,
        "disaster_app/edit_checklist.html",
        {"checklist": checklist}
    )

# DELETE CHECKLIST
def delete_checklist(request, item_id):

    check = admin_required(request)
    if check:
        return check

    checklist = Checklist.objects(id=ObjectId(item_id)).first()

    if checklist:
        checklist.delete()

    return redirect("/manage-checklist/")


# RESOURCES
def resources(request):

    check = login_required(request)
    if check:
        return check

    city = request.GET.get("city", "")
    resource_type = request.GET.get("type", "")

    resource_list = Resource.objects()

    if city:
        resource_list = resource_list.filter(address__icontains=city)

    if resource_type:
        resource_list = resource_list.filter(resource_type=resource_type)

    resource_list = resource_list.order_by("name")

    return render(
        request,
        "disaster_app/resources.html",
        {
            "resources": resource_list,
            "city": city,
            "type": resource_type
        }
    )


# ADD RESOURCE
def add_resource(request):

    check = admin_required(request)
    if check:
        return check

    if request.method == "POST":

        Resource(
            name=request.POST["name"],
            resource_type=request.POST["resource_type"],
            address=request.POST["address"],
            contact=request.POST["contact"]
        ).save()

        create_notification(
            "New Resource",
            request.POST["name"]
        )

        return redirect("/manage-resources/")

    return render(request, "disaster_app/add_resource.html")

# EDIT RESOURCE
def edit_resource(request, resource_id):

    check = admin_required(request)
    if check:
        return check

    resource = Resource.objects(id=ObjectId(resource_id)).first()

    if not resource:
        return redirect("/manage-resources/")

    if request.method == "POST":

        resource.name = request.POST["name"]
        resource.resource_type = request.POST["resource_type"]
        resource.address = request.POST["address"]
        resource.contact = request.POST["contact"]

        resource.save()

        return redirect("/manage-resources/")

    return render(
        request,
        "disaster_app/edit_resource.html",
        {"resource": resource}
    )

# DELETE RESOURCE
def delete_resource(request, resource_id):

    check = admin_required(request)
    if check:
        return check

    resource = Resource.objects(id=ObjectId(resource_id)).first()

    if resource:
        resource.delete()

    return redirect("/manage-resources/")


# HISTORY
def history(request):

    check = login_required(request)
    if check:
        return check

    history_list = SOSRequest.objects(
        name=request.session["user_name"]
    ).order_by("-created_at")

    return render(
        request,
        "disaster_app/history.html",
        {
            "history": history_list
        }
    )


# NOTIFICATIONS
def notifications(request):

    check = login_required(request)
    if check:
        return check

    notification_list = Notification.objects().order_by("-created_at")

    return render(
        request,
        "disaster_app/notifications.html",
        {
            "notifications": notification_list
        }
    )

# EMERGENCY REQUEST
def emergency(request):

    check = login_required(request)
    if check:
        return check

    if request.method == "POST":

        emergency_type = request.POST["emergency_type"]

        Emergency(
            user_name=request.session["user_name"],
            email=request.session["email"],
            location=request.POST["location"],
            emergency_type=emergency_type,
            created_at=datetime.now()
        ).save()

        create_notification(
            "Emergency Request",
            f'{request.session["user_name"]} requested emergency assistance.'
        )

        start_broadcast(
            emergency_type,
            request.POST["location"]
        )

        return render(
            request,
            "disaster_app/emergency.html",
            {
                "message": "Emergency request submitted successfully."
            }
        )

    return render(request, "disaster_app/emergency.html")


# SOS REQUEST
def emergency_sos(request):

    check = login_required(request)
    if check:
        return check

    if request.method == "POST":

        try:

            pincode = request.POST["pincode"]

            disaster = get_disaster(pincode)

            SOSRequest(
                name=request.session["user_name"],
                phone=request.POST["phone"],
                location=request.POST["location"],
                pincode=pincode,
                emergency_type=disaster,
                status="Pending",
                created_at=datetime.now()
            ).save()

            create_notification(
                "SOS Request",
                f'{request.session["user_name"]} submitted SOS for {disaster}.'
            )

            start_broadcast(
                disaster,
                request.POST["location"]
            )

            return render(
                request,
                "disaster_app/emergency.html",
                {
                    "success": "SOS request submitted successfully."
                }
            )

        except Exception as e:

            return render(
                request,
                "disaster_app/emergency.html",
                {
                    "error": str(e)
                }
            )

    return render(request, "disaster_app/emergency.html")

# DELETE SOS
def delete_sos(request, sos_id):

    check = admin_required(request)
    if check:
        return check

    sos = SOSRequest.objects(id=ObjectId(sos_id)).first()

    if sos:
        sos.delete()

    return redirect("/manage-sos/")


# ADMIN LOGIN
def admin_login(request):
    return redirect("/login/")

# ADMIN DASHBOARD
def admin_dashboard(request):

    check = admin_required(request)
    if check:
        return check

    context = {

        "admin_name": request.session["admin_name"],

        "user_count": User.objects.count(),

        "alert_count": Alert.objects.count(),

        "resource_count": Resource.objects.count(),

        "sos_count": SOSRequest.objects.count(),

        "emergency_count": Emergency.objects.count(),

        "users": User.objects.order_by("-created_at")[:5],

        "alerts": Alert.objects.order_by("-created_at")[:5],

        "sos_requests": SOSRequest.objects.order_by("-created_at")[:5],

        "emergencies": Emergency.objects.order_by("-created_at")[:5],

    }

    return render(
        request,
        "disaster_app/admin_dashboard.html",
        context
    )



# UPDATE SOS STATUS
def update_sos_status(request, sos_id, status):

    check = admin_required(request)
    if check:
        return check

    sos = SOSRequest.objects(
        id=ObjectId(sos_id)
    ).first()

    if sos:
        sos.status = status
        sos.save()

    return redirect("/admin-dashboard/")

# MANAGE USERS
def manage_users(request):

    check = admin_required(request)
    if check:
        return check

    search = request.GET.get("search", "")

    users = User.objects()

    if search:
        users = users.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search)
        )

    users = users.order_by("-created_at")

    return render(
        request,
        "disaster_app/manage_users.html",
        {
            "users": users,
            "search": search
        }
    )


# DELETE USER
def delete_user(request, user_id):

    check = admin_required(request)
    if check:
        return check

    user = User.objects(id=ObjectId(user_id)).first()

    if user and user.role != "admin":
        user.delete()

    return redirect("/manage-users/")

# MANAGE ALERTS
def manage_alerts(request):

    check = admin_required(request)
    if check:
        return check

    alerts = Alert.objects().order_by("-created_at")

    return render(
        request,
        "disaster_app/manage_alerts.html",
        {
            "alerts": alerts
        }
    )

# ADD ALERT
def add_alert(request):

    check = admin_required(request)
    if check:
        return check

    if request.method == "POST":

        Alert(
            title=request.POST["title"],
            description=request.POST["description"],
            disaster_type=request.POST["disaster_type"],
            severity=request.POST["severity"],
            location=request.POST["location"],
            created_at=datetime.now()
        ).save()

        create_notification(
            "New Alert",
            request.POST["title"]
        )

        return redirect("/manage-alerts/")

    return render(
        request,
        "disaster_app/add_alert.html"
    )


# MANAGE RESOURCES
def manage_resources(request):

    check = admin_required(request)
    if check:
        return check

    resources = Resource.objects().order_by("name")

    return render(
        request,
        "disaster_app/manage_resources.html",
        {
            "resources": resources
        }
    )

# MANAGE CHECKLIST
def manage_checklist(request):

    check = admin_required(request)
    if check:
        return check

    checklist = Checklist.objects().order_by("category")

    return render(
        request,
        "disaster_app/manage_checklist.html",
        {
            "checklist": checklist
        }
    )

# MANAGE SOS
def manage_sos(request):

    check = admin_required(request)
    if check:
        return check

    sos = SOSRequest.objects().order_by("-created_at")

    return render(
        request,
        "disaster_app/manage_sos.html",
        {
            "sos": sos
        }
    )


# ABOUT
def about(request):
    return render(request, "disaster_app/about.html")

# CONTACT
def contact(request):
    return render(request, "disaster_app/contact.html")