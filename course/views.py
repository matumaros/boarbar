

from django.views.generic import DetailView, TemplateView

from collection.models import Collection


# class CourseView(DetailView):
#     template_name = 'course/course.html'
#     http_method_names = ['get']
#     model = Collection

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         context.update({
#             'course': self.object,
#         })
#         return context


class CourseListView(TemplateView):
    template_name = 'course/main.html'
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course = Collection.objects.first()
        text = course.processed_text(
            '<a class={type} href="/word/{id}">{word}</a>'
        )
        context.update({
            'course': course,
            'text': text,
        })
        return context
