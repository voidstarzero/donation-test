from django.contrib.auth.decorators import user_passes_test
from django.conf import settings

LOGGED_IN_HOME = settings.LOGGED_IN_HOME

def login_forbidden(function=None, redirect_field_name=None, redirect_to=LOGGED_IN_HOME):
    """
    Decorator for views that checks that the user is NOT logged in, redirecting
    to the homepage if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_to,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def do_donate(attendee_id, event_ref, amount):
    pass # placeholder

def meets_pw_requirements(new, confirm):
    if new != confirm: return False
    if 8 > len(new) > 50: return False
    return True
