

from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import Proposal, ProposalTopic, ProposalComment, TopicComment


admin.site.register(Proposal, SimpleHistoryAdmin)
admin.site.register(ProposalTopic, SimpleHistoryAdmin)
admin.site.register(ProposalComment, SimpleHistoryAdmin)
admin.site.register(TopicComment, SimpleHistoryAdmin)
