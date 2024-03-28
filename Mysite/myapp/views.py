# registration/views.py
from django.shortcuts import render, redirect
from .forms import Userregistrationform, ProfileEditform, LoginForm, AddQueryForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import profile, AddQuery, queryNotification
from django.http import JsonResponse


def register(request):
    if request.method == "POST":
        user_form = Userregistrationform(request.POST)
        profile_form = ProfileEditform(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()

            profile = profile_form.save(commit=False)
            profile.user = new_user
            profile.save()

            return render(request, "myapp/regSuccess.html")
    else:
        user_form = Userregistrationform()
        profile_form = ProfileEditform()
    return render(
        request,
        "myapp/register.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def user_login(request):
    if request.method == "POST":
        form = LoginForm(
            request.POST
        )  # get access to the form and get the data which is posted
        if form.is_valid():
            # authenticate takes the username and password and checks those were present in database or not
            # if it finds the username and password in database it returns a object(UserObject) that contains user details
            data = (
                form.cleaned_data
            )  # The purpose  is to provide access to the cleaned and valid form input values.
            user = authenticate(
                request, username=data["username"], password=data["password"]
            )
            if user is not None:
                # if the username and password is correct it will return the user object
                login(
                    request, user
                )  # used to log in a user after their credentials have been successfully authenticated.
                # return HttpResponse('Login Successfull')
                return render(
                    request, "myapp/logindone.html", {"message": "Login Successful"}
                )
                # return render(request,'users/index.html')
            else:
                return HttpResponse("invalid credentials")
    else:
        form = LoginForm()
    return render(request, "myapp/login.html", {"form": form})


# def Homepage(request):
#     username = request.user.username
#     # here i need to get the post of current user
#     currentuser = request.user
#     return render(request, "myapp/home.html", {"username": username})
def Homepage(request):
    querys = AddQuery.objects.all()

    if request.method == "POST":
        query_id = request.POST.get("query_id")
        quer = AddQuery.objects.get(id=query_id)
    # Get the current user's profile
    username = request.user.username
    currentuser = request.user
    try:
        current_profile = profile.objects.get(user=request.user)
        registration_number = current_profile.Roll
        phone_number = current_profile.call
    except profile.DoesNotExist:
        # Handle the case where profile doesn't exist for the user
        registration_number = None
    return render(
        request,
        "myapp/home.html",
        {
            "registration_number": registration_number,
            "querys": querys,
            "username": username,
            "phone_number": phone_number,
        },
    )


def create_query(request):
    if request.method == "POST":
        product_form = AddQueryForm(request.POST, request.FILES)
        if product_form.is_valid():
            new_product = product_form.save(commit=False)
            new_product.seller = request.user  # Assign the seller to the correct field
            new_product.save()
            return redirect("home")
    else:
        product_form = AddQueryForm()
    return render(request, "myapp/create_product.html", {"product_form": product_form})


def add_query(request):
    if request.method == "POST":
        owner_name = request.POST.get("username")
        query_creator_name = request.POST.get("query_creator_name")
        query_name = request.POST.get("query_name")

        # Check if the owner name is the same as the query creator name
        if owner_name == query_creator_name:
            return render(
                request,
                "myapp/success1.html",
                {"message": "You can't click on your Own Post"},
            )

        # Check if the query already exists in the database
        if queryNotification.objects.filter(
            owner_name=owner_name,
            query_creator_name=query_creator_name,
            query_name=query_name,
        ).exists():
            return render(
                request, "myapp/success2.html", {"message": "Notification already sent"}
            )

        # Retrieve the owner's profile
        owner_profile = get_object_or_404(profile, user__username=owner_name)

        # Create a new queryNotification instance
        query_item = queryNotification.objects.create(
            owner_name=owner_name,
            query_creator_name=query_creator_name,
            query_name=query_name,
            owner_PhNo=owner_profile.call,  # Assuming phone number is stored in 'num' field of profile model
            Owner_reg=owner_profile.Roll,  # Assuming registration number is stored in 'Registration' field of profile model
        )
        return render(request, "myapp/success3.html", {"message": "Notification sent"})
    return redirect("home")  # Redirect to home page if not a POST request


from .models import queryNotification, AddQuery


from .models import queryNotification, AddQuery


from .models import queryNotification, AddQuery


from .models import queryNotification, AddQuery


def dashboard(request):
    querys = AddQuery.objects.filter(seller=request.user)

    logged_in_user = request.user.username

    # Filter query notifications where the query creator name matches the logged-in user's username
    query_notifications = queryNotification.objects.filter(
        query_creator_name=logged_in_user
    )

    owner_query_list = []

    # Iterate through each query notification
    for query_notification in query_notifications:
        # Fetch owner name
        owner_name = query_notification.owner_name

        # Fetch owner's details from your model assuming `owner` is a ForeignKey or OneToOneField in your `queryNotification` model
        owner = query_notification.owner_name

        # Get owner's phone number and registration number
        # owner_phone_number = owner.owner_Phno
        # owner_registration_number = owner.owner_regNo

        # Get query name
        query_name = query_notification.query_name
        PhNo = query_notification.owner_PhNo
        regNo = query_notification.Owner_reg

        # Append owner name, phone number, registration number, and query name to the list as a dictionary
        owner_query_list.append(
            {
                "owner_name": owner_name,
                # "owner_phone_number": owner_phone_number,  # Include owner's phone number
                # "owner_registration_number": owner_registration_number,  # Include owner's registration number
                "query_name": query_name,
                "PhNo": PhNo,
                "regNo": regNo,
            }
        )

    return render(
        request,
        "myapp/dashboard.html",
        {
            "owner_query_list": owner_query_list,  # Pass the list of dictionaries to the template
            "querys": querys,
        },
    )


from .models import AddQuery, profile  # Import the profile model


def detail(request, id):
    query = AddQuery.objects.get(id=id)
    username = request.user.username
    try:
        current_profile = profile.objects.get(
            user=request.user
        )  # Retrieve the profile associated with the current user
        registration_number = current_profile.Roll
        phone_number = current_profile.call
    except profile.DoesNotExist:
        # Handle the case where profile doesn't exist for the user
        registration_number = None
        # Phone_number = None
    # stripe_pubishable_key = settings.STRIPE_PUBLISHABLE_KEY
    return render(
        request,
        "myapp/detail.html",
        {
            "query": query,
            "username": username,
            "registration_number": registration_number,
            "phone_number": phone_number,
        },
    )


from django.shortcuts import redirect, get_object_or_404


def delete_query(request, id):
    query = get_object_or_404(AddQuery, id=id)
    if request.method == "POST":
        query.delete()
        return redirect("dashboard")
    return redirect("dashboard")


def edit_query(request, id):
    query = get_object_or_404(AddQuery, id=id)
    form = AddQueryForm(instance=query)
    if request.method == "POST":
        form = AddQueryForm(request.POST, instance=query)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    return render(request, "myapp/edit.html", {"form": form})
