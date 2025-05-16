import time
from http.client import responses

from django.core.cache import cache
from django.http import HttpRequest, request, HttpResponseForbidden


def set_useragent_on_request_middleware(get_response):

    print("initial call")
    def middleware(request: HttpRequest):
        print("befor get response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print("after get response")

        return response

    return middleware


class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.response_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.request_count += 1
        print(f"request count: {self.request_count}")
        response = self.get_response(request)
        self.response_count += 1
        print(f"response count: {self.response_count}")
        return response

    def process_exeption(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exceptions so far")


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response=get_response
        #  Лимиты на кол-во запросов
        self.rate_limit = 3
        self.time_limit = 60

    def __call__(self, request:HttpRequest):
        ip = self.get_client_ip(request)

        if not ip:
            return HttpResponseForbidden("Не удалось определить ваш IP адрес.")

        # Создание ключа для кэша
        cache_key = f"throttle_{ip}"

        # Получение истории запроса из кэша
        request_history = cache.get(cache_key, [])

        # Удаление записей у которых истек временной промежуток по заданному таймеру.
        current_time = time.time()
        request_history = [t for t in request_history if current_time - t < self.rate_limit]

        # Проверка на превышение лимита в истории
        if len(request_history) >= self.rate_limit:
            return HttpResponseForbidden("Превышение лимита запроса при обращение к сервису, попробуйте позже.")

        # Запись запроса в историю
        request_history.append(current_time)
        cache.set(cache_key, request_history, self.time_limit)

        return self.get_response(request)



    def get_client_ip(self, request: HttpRequest):
        x_forwarded_for = request.META.get('HTTP_X_FORWADED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
            print(ip)
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
