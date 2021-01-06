from rest_framework import serializers
from eventapp.models import (
    Profile,
    ImovelUpdateLog,
    Imovel,
    Notice,
    NoticeEventType,
    NoticeColor,
    NoticeEvent,
    NoticeFine,
    SurveyEventType,
    SurveyEvent,
    Activity,
)
from django.contrib.auth.models import User

from eventapp.utils import add_days
from django.db import transaction


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ("user",)


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    last_login = serializers.DateTimeField(
        read_only=True, format="%Y-%m-%dT%H:%M"
    )
    date_joined = serializers.DateTimeField(
        read_only=True, format="%Y-%m-%dT%H:%M"
    )

    class Meta:
        model = User
        exclude = ("password",)
        read_only_fields = (
            "last_login",
            "date_joined",
            "is_superuser",
            "groups",
            "user_permissions",
        )

    @transaction.atomic
    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        profile = Profile.objects.filter(user=instance).first()
        if not profile:
            profile = Profile.objects.create(user=instance)
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
        )
        read_only_fields = (
            "id",
            "first_name",
            "last_name",
        )


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ImovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imovel
        fields = (
            "id",
            "codigo_lote",
            "logradouro",
            "numero",
            "bairro",
            "cep",
            "area_lote",
            "inscricao_imobiliaria",
            "codigo",
            "matricula",
            "razao_social",
            "complemento",
            "numero_contribuinte",
            "name_string",
        )
        read_only_fields = ("name_string",)


class ImovelUpdateLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImovelUpdateLog
        fields = "__all__"


class NoticeEventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeEventType
        fields = "__all__"


class NoticeColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeColor
        fields = ("id", "css_color", "notice_event_types", "css_name")
        read_only_fields = ("css_name",)


class NoticeFineSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%Y-%m-%d")
    id = serializers.IntegerField(required=False)

    class Meta:
        model = NoticeFine
        fields = "__all__"
        read_only_fields = ("notice_event",)


class NoticeEventSerializer(serializers.ModelSerializer):
    notice_fines = NoticeFineSerializer(many=True, required=False)
    deadline_date = serializers.DateField(format="%Y-%m-%d", required=False)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = NoticeEvent
        fields = (
            "id",
            "date",
            "identification",
            "report_number",
            "notice",
            "notice_event_type",
            "deadline",
            "deadline_working_days",
            "deadline_date",
            "concluded",
            "notice_fines",
        )
        read_only_fields = (
            "notice",
            "deadline_date",
        )


def update_or_create_multiple_notice_events(
    notice, notice_events_data, force_create=False
):
    keep_notice_event = []
    for notice_event in notice_events_data:
        if "notice_fines" in notice_event.keys():
            notice_fines_data = notice_event.pop("notice_fines")
        else:
            notice_fines_data = []
        if "id" in notice_event.keys():
            id = notice_event.pop("id")
        else:
            id = 0

        deadline_date = add_days(
            notice_event["date"],
            notice_event["deadline"],
            notice_event["deadline_working_days"],
        )

        notice_event_instance = NoticeEvent.objects.filter(id=id).first()
        if notice_event_instance is not None and id != 0 and not force_create:
            for attr, value in notice_event.items():
                setattr(notice_event_instance, attr, value)
            notice_event_instance.deadline_date = deadline_date
            notice_event_instance.save()
        else:
            if "notice" in notice_event.keys():
                notice_event.pop("notice")
            if "deadline_date" in notice_event.keys():
                notice_event.pop("deadline_date")
            notice_event_instance = NoticeEvent.objects.create(
                **notice_event, notice=notice, deadline_date=deadline_date
            )
        keep_notice_event.append(notice_event_instance.id)
        # ====FINES====
        update_or_create_multiple_notice_fines(
            notice_event_instance, notice_fines_data, force_create
        )
    for notice_event in notice.notice_events.all():
        if notice_event.id not in keep_notice_event:
            notice_event.delete()


def update_or_create_multiple_notice_fines(
    notice_event, notice_fines_data, force_create=False
):
    keep_fine_event = []
    for notice_fine in notice_fines_data:
        if "id" in notice_fine.keys():
            id = notice_fine.pop("id")
        else:
            id = 0
        notice_fine_instance = NoticeFine.objects.filter(id=id).first()
        if notice_fine_instance is not None and id != 0 and not force_create:
            for attr, value in notice_fine.items():
                setattr(notice_fine_instance, attr, value)
            notice_fine_instance.save()
        else:
            notice_fine_instance = NoticeFine.objects.create(
                **notice_fine, notice_event=notice_event
            )
        keep_fine_event.append(notice_fine_instance.id)
    for notice_fine in notice_event.notice_fines.all():
        if notice_fine.id not in keep_fine_event:
            notice_fine.delete()


class NoticeSerializer(serializers.ModelSerializer):
    notice_events = NoticeEventSerializer(many=True)
    date = serializers.DateField(format="%Y-%m-%d")
    imovel = ImovelSerializer(many=False, read_only=True)
    imovel_id = serializers.IntegerField()

    class Meta:
        model = Notice
        fields = (
            "id",
            "imovel",
            "imovel_id",
            "document",
            "date",
            "address",
            "description",
            "owner",
            "notice_events",
            "css_name",
        )
        read_only_fields = ("css_name",)

    @transaction.atomic
    def create(self, validated_data):
        if "notice_events" in validated_data.keys():
            notice_events_data = validated_data.pop("notice_events")
        else:
            notice_events_data = []
        if "imovel_id" in validated_data.keys():
            if validated_data["imovel_id"] == 0:
                validated_data["imovel_id"] = None
        notice = Notice.objects.create(**validated_data)
        # ====NOTICE_EVENTS====
        update_or_create_multiple_notice_events(
            notice, notice_events_data, True
        )
        first_date_instance = notice.notice_events.order_by("date").first()
        if first_date_instance:
            notice.date = first_date_instance.date
            notice.save()
        return notice

    @transaction.atomic
    def update(self, instance, validated_data):
        if "notice_events" in validated_data.keys():
            notice_events_data = validated_data.pop("notice_events")
        else:
            notice_events_data = []
        if "imovel_id" in validated_data.keys():
            if validated_data["imovel_id"] == 0:
                validated_data["imovel_id"] = None
        Notice.objects.filter(id=instance.id).update(**validated_data)
        notice = Notice.objects.get(id=instance.id)
        # ====NOTICE_EVENTS====
        update_or_create_multiple_notice_events(notice, notice_events_data)
        first_date_instance = notice.notice_events.order_by("date").first()
        if first_date_instance:
            notice.date = first_date_instance.date
            notice.save()
        return notice


class SurveyEventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyEventType
        fields = "__all__"


class SurveyEventSerializer(serializers.ModelSerializer):

    imovel = ImovelSerializer(many=False, read_only=True)
    date = serializers.DateField(format="%Y-%m-%d")
    imovel_id = serializers.IntegerField()

    class Meta:
        model = SurveyEvent
        fields = (
            "id",
            "imovel",
            "imovel_id",
            "document",
            "identification",
            "date",
            "survey_event_type",
            "address",
            "description",
            "concluded",
            "owner",
        )

    @transaction.atomic
    def create(self, validated_data):
        if "imovel_id" in validated_data.keys():
            if validated_data["imovel_id"] == 0:
                validated_data["imovel_id"] = ""
        return SurveyEvent.objects.create(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        if "imovel_id" in validated_data.keys():
            if validated_data["imovel_id"] == 0:
                validated_data["imovel_id"] = ""
        SurveyEvent.objects.filter(id=instance.id).update(**validated_data)
        return SurveyEvent.objects.get(id=instance.id)


class ActivitySerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Activity
        fields = "__all__"
