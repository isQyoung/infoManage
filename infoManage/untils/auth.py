from django.shortcuts import redirect
from functools import wraps
from django.contrib.sessions.models import Session


# session认证装饰器
def login_check(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('info', None):
            return redirect("infoManage:login")
        else:
            session_id = request.session.session_key
            db_session = Session.objects.get(session_key=session_id)
            session_info = db_session.get_decoded()['info']
            cookie_info = request.session.get('info')
            # print(session_info, cookie_info)
            if session_info == cookie_info:
                # print('session和cookie一致')
                return func(request, *args, **kwargs)
            # print('session和cookie不一致')
            return redirect("infoManage:login")

    return wrapper
