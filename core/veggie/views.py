from django.shortcuts import render, redirect
from veggie.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import *
from django.contrib.auth import get_user_model
from veggie.seed import *

# User = get_user_model()


@login_required(login_url="/login/")
# Create your views here.
def receipes(request):
    if request.method == "POST":
        data = request.POST
        receipe_image = request.FILES.get("receipe_image")
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")

        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image,
        )

        return redirect("/receipes/")
    receipes = Receipe.objects.all()
    context = {"receipes": receipes}
    return render(request, "receipes.html", context)


@login_required(login_url="/login/")
def delete_receipe(request, id):
    query_set = Receipe.objects.get(id=id)
    query_set.delete()
    return redirect("/receipes/")


@login_required(login_url="/login/")
def update_receipe(request, id):
    query_set = Receipe.objects.get(id=id)
    if request.method == "POST":
        data = request.POST
        receipe_image = request.FILES.get("receipe_image")
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")

        query_set.receipe_name = receipe_name
        query_set.receipe_description = receipe_description
        if receipe_image:
            query_set.receipe_image = receipe_image

        query_set.save()
        return redirect("/receipes/")

    context = {"receipe": query_set}
    return render(request, "update_receipes.html", context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username)
        if not user.exists():
            messages.error(request, "Invalid username")
            return redirect("/login/")

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid credential")
            return redirect("/login/")

        else:
            login(request, user)
            return redirect("/receipes/")

    return render(request, "login.html")


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "Email already exists")
            return redirect("/register/")

        user = User.objects.create(
            first_name=first_name, last_name=last_name, username=username
        )
        user.set_password(password)
        user.save()
        messages.info(request, "User registration done")

        return redirect("/register/")

    return render(request, "register.html")


def logout_page(request):
    logout(request)
    return redirect("/login/")


def practice(request):
    # student name contain/starts/end
    query_set = Student.objects.filter(student_name__startswith="Ad")

    # endswith
    query_set = Student.objects.filter(student_email__endswith=".org")

    # contains
    query_set = Student.objects.filter(student_name__icontains="ame")

    # get data from another table, i.e. get department
    query_set = Student.objects.filter(student_name__icontains="ame")
    for i in query_set:
        print(i.department)

    # want to access nested columns in department table.
    # user i.department.date, i.department.column_names
    # we can point out multiple level nested keys. Using similer approch.

    # get student where department is same (Civil)
    query_set = Student.objects.filter(department__department="Civil")
    print(query_set.count())
    # use contains in nested access
    query_set = Student.objects.filter(department__department__icontains="vil")

    # in operator.
    d = ["Civil", "Computer Science"]
    query_set = Student.objects.filter(department__department__in=d)

    # exclude (we dont want some department in result)
    query_set = Student.objects.exclude(department__department="Civil")

    # check if we are getting data of not. return bool.
    query_set.exists()

    # serializing (get values)
    # gives list of dict, which we can access later.
    query_set.values()

    # use distinct
    query_set = Student.objects.all().distinct("student_name")

    # get specific column
    query_set = Student.objects.values_list("id", "student_name")

    # union (2 query set combine), intersection,difference.
    # select only distinct value, to allow duplicates set all=True
    """query_set1 = Student.objects.values_list("id")
    query_set2 = Student.objects.get(id=5)

    # query_set.union(query_set1, query_set2)
    query_set.intersection(query_set1, query_set2)
    # uses Except from SQL
    query_set.difference(query_set1, query_set2)"""

    # aggregate functions (applies on single column)
    # min, max, sum, avg etc.
    avg_query_set = Student.objects.aggregate(Avg("student_age"))
    print(avg_query_set)
    max_query_set = Student.objects.aggregate(Max("student_age"))
    print(max_query_set)
    min_query_set = Student.objects.aggregate(Min("student_age"))
    print(min_query_set)
    sum_query_set = Student.objects.aggregate(Sum("student_age"))
    print(sum_query_set)

    # Group By/ Annotate
    student = Student.objects.values("student_age").annotate(Count("student_age"))
    print(student)
    # annotate on multiple columns
    student = Student.objects.values("student_age", "department").annotate(
        Count("student_age"), Count("department")
    )
