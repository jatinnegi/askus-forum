from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_username(username):
    if username.__len__() < 5 or username.__len__() > 30:
        raise ValidationError(_("Username must be between 5-30 characters"))

    for c in username:
        if ord(c) < 97:
            if ord(c) > 47 and ord(c) < 58:
                continue
            if ord(c) == 95 or ord(c) == 45:
                continue
            if ord(c) < 65 or ord(c) > 90:
                raise ValidationError(
                    _("Username must contain only alphabets, numbers, _ or -"))

        if ord(c) > 122:
            raise ValidationError(
                _("Username must contain only alphabets, numbers, _ or -"))

    if username[0] == '-' or username[0] == '_' or username[0].isdigit():
        raise ValidationError(_("Username must start with an alphabet"))
