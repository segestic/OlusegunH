from django.contrib.auth.tokens import PasswordResetTokenGenerator

import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.patient.email_confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()

##----------------2ND ACIVATION---------------

class AccountActivationTokenGenerator2(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.doctor.email_confirmed)
        )

account_activation_token2 = AccountActivationTokenGenerator2()