

from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import Proposal, ProposalTopic, Comment


admin.site.register(Proposal, SimpleHistoryAdmin)
admin.site.register(ProposalTopic, SimpleHistoryAdmin)
admin.site.register(Comment, SimpleHistoryAdmin)
