from django.shortcuts import render
from veggie.models import *
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from accounts.models import *
from veggie.seed import *


# Create your views here.
def get_students(request):
    query_set = Student.objects.all()

    # search funtionality
    if request.GET.get("search"):
        search = request.GET.get("search")
        query_set = query_set.filter(
            Q(student_name__icontains=search)
            | Q(department__department__icontains=search)
            | Q(student_id__student_id__icontains=search)
            | Q(student_email__icontains=search)
            | Q(student_age__icontains=search)
        )

    paginator = Paginator(query_set, 15)
    # pagination implementation
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return render(request, "report/students.html", {"query_set": page_obj})


def see_marks(request, student_id):
    query_set = StudentMarks.objects.filter(student__student_id__student_id=student_id)

    ranks = Student.objects.annotate(marks=Sum("studentmarks__marks")).order_by(
        "-marks"
    )
    total_marks = query_set.aggregate(total_marks=Sum("marks"))
    return render(
        request,
        "report/marks.html",
        {
            "query_set": query_set,
            "total_marks": total_marks,
        },
    )
