

import logging

from word.views import SuggestView

logger = logging.getLogger(__name__)


class ContribView(SuggestView):
    template_name = 'contribute/main.html'





