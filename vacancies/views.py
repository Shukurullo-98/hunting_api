from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.db.models.aggregates import Count
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from vacancies.models import Vacancy, Skill
from vacancies.permission import VacancyCreatePermission
from vacancies.serializer import VacancyListSerializer, VacancyDetailSerializer, VacancyCreateSerializer, \
    VacancyUpdateSerializer, VacancyDestroySerializer, SkillSerializer


class SkillsViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class VacancyView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    def get(self, request, *args, **kwargs):
        vacancy_text = request.GET.get('text', None)
        if vacancy_text:
            self.queryset = self.queryset.filter(
                text__icontains=vacancy_text
            )
        skills = request.GET.getlist("skill", None)
        skills_q = None
        for skill in skills:
            if skills_q is None:
                skills_q = Q(skills__name__icontains=skill)
            else:
                skills_q |= Q(skills__name__icontains=skills)

        if skills_q:
            self.queryset = self.queryset.filter(skills_q)
        return super().get(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     super().get(request, *args, **kwargs)
    #     search_text = self.request.GET.get('search', None)
    #     if search_text:
    #         self.object_list = self.object_list.filter(text=search_text)
    #
    #     self.object_list = self.object_list.select_related('user').prefetch_related('skills').order_by("text")
    #
    #     paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
    #     page_number = request.GET.get('page')
    #     page_obj = paginator.get_page(page_number)
    #
    # vacancies = []
    #
    # for vacancy in page_obj:
    #     vacancies.append({
    #         'id': vacancy.id,
    #         'text': vacancy.text,
    #         'slug': vacancy.slug,
    #         'status': vacancy.status,
    #         'created': vacancy.created,
    #         'skills': list(vacancy.skills.all().values_list('name', flat=True)),
    #         'username': vacancy.user.username
    #     })
    #
    #     list(map(lambda x: setattr(x, 'username', x.user.username if x.user else None), page_obj))
    #     response = {
    #         "items": VacancyListSerializer(page_obj, many=True).data,
    #         "num_pages": paginator.num_pages,
    #         "total": paginator.count
    #     }
    #     return JsonResponse(response, safe=False)


class VacancyDetailView(RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer
    permission_classes = [IsAuthenticated]

    # def get(self, request, *args, **kwargs):
    #     vacancy = self.get_object()
    #
    #     return JsonResponse(VacancyDetailSerializer(vacancy).data)


# @method_decorator(csrf_exempt, name='dispatch')
class VacancyCreateView(CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer
    permission_classes = [IsAuthenticated, VacancyCreatePermission]

    # def post(self, request, *args, **kwargs):
    #     vacancy_data = VacancyCreateSerializer(data=json.loads(request.body))
    #     if vacancy_data.is_valid():
    #         vacancy_data.save()
    #     else:
    #         return JsonResponse(vacancy_data.errors)
    #
    #
    #     # vacancy = Vacancy.objects.create(
    #     #     slug=vacancy_data['slug'],
    #     #     text=vacancy_data['text'],
    #     #     status=vacancy_data['status'],
    #     # )
    #     # vacancy.user = get_object_or_404(User, pk=vacancy_data['user_id'])
    #     #
    #     # for skill in vacancy_data["skills"]:
    #     #     skill_obj, created = Skill.objects.get_or_create(
    #     #         name=skill,
    #     #         defaults={
    #     #             'is_active': True,
    #     #         }
    #     #     )
    #     #     vacancy.skills.add(skill_obj)
    #     # vacancy.save()
    #
    #     return JsonResponse(vacancy_data.data)


# @method_decorator(csrf_exempt, name='dispatch')
class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer

    # def patch(self, request, *args, **kwargs):
    #     super().post(request, *args, **kwargs)
    #     vacancy_data = json.loads(request.body)
    #     self.object.slug = vacancy_data['slug']
    #     self.object.text = vacancy_data['text']
    #     self.object.status = vacancy_data['status']
    #
    #     for skill in vacancy_data["skills"]:
    #         try:
    #             skill_obj = Skill.objects.get(name=skill)
    #         except Skill.DoesNotExist:
    #             return JsonResponse({"error": "Skills not found"}, status=404)
    #         self.object.skills.add(skill_obj)
    #
    #     self.object.save()
    #
    #     return JsonResponse({
    #         'id': self.object.id,
    #         'text': self.object.text,
    #         'slug': self.object.slug,
    #         'status': self.object.status,
    #         'created': self.object.created,
    #         'skills': list(self.object.skills.all().values_list('name', flat=True)),
    #         'user': self.object.user_id,
    #     })


# @method_decorator(csrf_exempt, name='dispatch')
class VacancyDeleteView(DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDestroySerializer
    # model = Vacancy
    # success_url = '/'

    # def delete(self, request, *args, **kwargs):
    #     super().delete(request, *args, **kwargs)
    #
    #     return JsonResponse(
    #         {"status": "ok"},
    #         status=200,
    #     )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_vacancies(request):
    user_qs = User.objects.annotate(vacancies=Count('vacancy'))

    paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    users = []
    for user in page_obj:
        users.append({
            "id": user.id,
            "name": user.username,
            "vacancies": user.vacancies
        })

    response = {
        "items": users,
        "total": paginator.count,
        "numa_page": paginator.num_pages
    }
    return JsonResponse(response)


class VacancyLikeView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer

    def put(self, request, *args, **kwargs):
        Vacancy.objects.filter(pk__in=request.data).update(likes=F('likes') + 1)

        return JsonResponse(VacancyDetailSerializer(Vacancy.objects.filter(pk__in=request.data), many=True).data,
                            safe=False)
