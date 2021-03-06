"""
anonymize_data command
"""

from django.core.management.base import AppCommand
from django.db import transaction
from django.utils import importlib

from anonymizer import Anonymizer


class Command(AppCommand):

    def handle_app(self, app, **options):
        #TODO: add support for anonymizing selected models with modulename.Model
        anonymizers_module = ".".join(app.__name__.split(".")[:-1] + ["anonymizers"])
        mod = importlib.import_module(anonymizers_module)

        anonymizers = []
        for k, v in mod.__dict__.items():
            is_anonymizer = False
            if 'Anonymizer' in k:
                is_anonymizer = True
            try:
                if issubclass(v, Anonymizer):
                    is_anonymizer = True
            except TypeError:
                pass

            if v is Anonymizer:
                is_anonymizer = False

            if k.startswith('_'):
                is_anonymizer = False

            if is_anonymizer:
                v().validate()
                anonymizers.append(v)

        anonymizers.sort(key=lambda c:c.order)
        for anonymizer in anonymizers:
            with transaction.commit_on_success():
                anonymizer().run()

