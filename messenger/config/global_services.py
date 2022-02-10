import os
from datetime import datetime
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission
import traceback as traceback

from django.db import connection
from django.test.utils import CaptureQueriesContext


# MODELS
def get_upload_path(dir_name: str = None) -> str:
    """ Определение полного загрузочного пути media files """
    if dir_name is not None:
        return os.path.join(dir_name, datetime.now().date().strftime("%Y/%m/%d"))
    else:
        return 'images/'


# SERVICES
def logic_exception_handler(services_func):
    """ Декоратор обработки ошибок в services файлах """

    def wrapped(*args, **kwargs):
        try:
            return services_func(*args, **kwargs)
        except Exception as e:
            # services_func(*args, **kwargs)
            # Берём название функции в которой произошла ошибка из traceback
            frame_summary_list = list(traceback.TracebackException(
                exc_type=type(e),
                exc_traceback=e.__traceback__,
                exc_value=e).stack[-1]
                                      )
            function_name = frame_summary_list[-2]
            line_exception = frame_summary_list[-3]
            error_message = f"Error in function '{function_name}', line: {line_exception}  {e}"
        raise APIException(error_message)

    return wrapped


# TESTS
# def sql_processing(ctx, write=False) -> None:
#     if write:
#


def sql_processing(test_func):
    """ Декоратор для вывода SQL запросов при запуске теста """

    def wrapped(*args, **kwargs):
        with CaptureQueriesContext(connection) as ctx:
            test_func(*args, **kwargs)
        print('\n', '\n\n'.join(map(str, ctx.captured_queries)), '\n', len(ctx))
    return wrapped


# SETTINGS
class IsAuthenticatedVerified(BasePermission):
    """ Проверка прав пользователя на подтверждение почты """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_verified and request.user.is_authenticated)
