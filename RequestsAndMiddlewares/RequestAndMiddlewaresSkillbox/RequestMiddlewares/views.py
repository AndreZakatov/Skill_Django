from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def process_get_view(request: HttpRequest) -> HttpResponse:

    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    resault = a + b
    context = {
        "a": a,
        "b": b,
        "resault": resault,
    }

    return render(request, "RequestMiddlewares/request_query_params.html", context=context)



def user_form(request: HttpRequest) -> HttpResponse:
    return render(request, 'RequestMiddlewares/user_bio_form.html')


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST" and request.FILES.get("send_file"):
        if "send_file" in request.FILES:
            my_file = request.FILES["send_file"]
            file_size = my_file.size

            if file_size > 1 * 1024 * 1024:
                context["error"] = f"Превышены размеры файла в 1 МБ"
                return render(request, f"RequestMiddlewares/error_limit_upload.html", {'error':
                                                                                          f'Превышение лимита в 1 мб\nРазмер вашего файла {round(file_size/1000000, 2)} мб.'})
            else:
                fs = FileSystemStorage()
                fs.save(my_file.name, my_file)
                context["success"] = f"Файл {my_file.name} успешно згружен"
                return render(request, "RequestMiddlewares/file_upload.html", {'seccess': True})

    return render(request, "RequestMiddlewares/file_upload.html")