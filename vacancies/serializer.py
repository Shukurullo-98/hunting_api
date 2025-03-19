from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from authentication.models import User
from vacancies.models import Vacancy, Skill


class VacancyListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)

    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Vacancy
        fields = ['id', 'text', 'slug', 'status', 'created', 'username', 'skills']


class VacancyDetailSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancyCreateSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField()
    id = serializers.IntegerField(required=False)
    skills = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Skill.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Vacancy
        exclude = []
        fields = '__all__'


    def is_valid(self, *, raise_exception=False):
        self._skills = self.initial_data.pop('skills', [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        vacancy = Vacancy.objects.create(**validated_data)

        for skill in self._skills:
            skill_obj, _ = Skill.objects.get_or_create(name=skill)
            vacancy.skills.add(skill_obj)

        vacancy.save()
        return vacancy


class VacancyUpdateSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField()
    skills = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Skill.objects.all(),
        slug_field='name'
    )
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Vacancy
        exclude = []
        fields = ['id', 'text', 'status', 'slug', 'user', 'created', 'skills']


    def is_valid(self, *, raise_exception=False):
        self._skills = self.initial_data.pop('skills', [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        vacancy = super().save()

        for skill in self._skills:
            skill_obj, _ = Skill.objects.get_or_create(name=skill)
            vacancy.skills.add(skill_obj)

        vacancy.save()
        return vacancy


class VacancyDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['id']



class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

