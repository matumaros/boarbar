

from django.core.management.base import BaseCommand
from django.core.management import call_command

from language.models import Language
from word.models import WordVersion


class Command(BaseCommand):
    args = ''
    help = 'Setup servare database'

    def _create_languages(self):
        bavarian = Language(name='BAR', default_variant='bv_DA')
        bavarian.save()
        english = Language(name='ENG', default_variant='en_US')
        english.save()
        spanish = Language(name='SPA', default_variant='es_ES')
        spanish.save()
        WordVersion(
            name='Boariš 2018',
            link='https://en.wikipedia.org/wiki/Bavarian_language',
            language=bavarian
        )
        WordVersion(
            name='American English',
            link='https://en.wikipedia.org/wiki/American_English',
            language=english
        )
        WordVersion(
            name='Spanish',
            link='https://en.wikipedia.org/wiki/Spanish_language',
            language=spanish
        )

    def handle(self, *args, **options):
        call_command('migrate')
        self._create_languages()
