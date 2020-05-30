import datetime

from psycopg2.extras import DateRange
from rest_framework import serializers

from .models import (
    BreedingStockEvent,
    CalfEvent,
    SingleBreedingStockEvent,
    SingleCalfEvent,
)
from ..animals.models import BreedingStock, Calf
from .utils import merge_events


class BreedingStockNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreedingStock
        fields = (
            "id",
            "tag_number",
            "name",
        )


class SingleBreedingStockEventSerializer(serializers.ModelSerializer):
    animal = BreedingStockNestedSerializer(read_only=True)

    class Meta:
        model = SingleBreedingStockEvent
        fields = (
            # "id",
            "animal",
            "completed",
            "completion_date",
            "attributes",
        )


class SKTWeightMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleBreedingStockEvent
        fields = (
            "id",
            "event",
            "animal",
            "completed",
            "completion_date",
            "attributes",
        )
        extra_kwargs = {"event": {"required": False}}

    def create(self, validated_data):
        return SingleBreedingStockEvent.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance

    def validate(self, data):
        if not data.get("event", None) and not self.instance:
            the_farm = BreedingStock.objects.get(pk=data["animal"].pk).farm
            title = None
            if "skt" in data["attributes"]:
                title = "скт"
            elif "weight" in data["attributes"]:
                title = "взвешивание"

            data["event"] = BreedingStockEvent.objects.filter(
                title__icontains="скт", farm=the_farm
            ).last()

            if not data.get("event", None):
                data["event"] = BreedingStockEvent.objects.create(
                    farm=the_farm,
                    title=title,
                    scheduled_date_range=DateRange(
                        datetime.date(2020, 1, 1), datetime.datetime.now().date()
                    ),
                )

        return data


class CalfNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calf
        fields = (
            "id",
            "tag_number",
            "name",
            "gender",
        )


class SingleCalfEventSerializer(serializers.ModelSerializer):
    animal = CalfNestedSerializer(read_only=True)

    class Meta:
        model = SingleCalfEvent
        fields = (
            # "id",
            "animal",
            "completed",
            "completion_date",
            "attributes",
        )


class BreedingStockEventSerializer(serializers.ModelSerializer):
    animals = SingleBreedingStockEventSerializer(
        source="singlebreedingstockevent_set", many=True, read_only=True
    )
    animals_list = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=BreedingStock.objects.all(), many=True,
    )

    class Meta:
        model = BreedingStockEvent
        fields = (
            "id",
            "title",
            "scheduled_date_range",
            "report",
            "type",
            "animals_list",
            "animals",
        )
        read_only_fields = (
            "id",
            "animals",
        )

    def create(self, validated_data):
        animals_list = validated_data.pop("animals_list", [])
        the_farm = self.context["request"].user.farm
        validated_data["farm"] = the_farm
        bs_event = BreedingStockEvent(**validated_data)

        merge_events(BreedingStockEvent, SingleBreedingStockEvent, bs_event, the_farm)

        # Create additional animals for bs_event
        for pk in animals_list:
            sb1 = SingleBreedingStockEvent.objects.filter(event=bs_event).last()

            if sb1:
                if sb1.animal.farm == BreedingStock.objects.get(pk=pk).farm:
                    SingleBreedingStockEvent.objects.get_or_create(
                        event=bs_event, animal=pk
                    )
            else:
                SingleBreedingStockEvent.objects.get_or_create(
                    event=bs_event, animal=pk
                )

        return bs_event

    def update(self, instance, validated_data):
        animals_list = validated_data.pop("animals_list", None)
        the_farm = self.context["request"].user.farm

        if "id" in validated_data:
            validated_data.pop("id")  # remove id, since we already have instance obj
        instance = super(BreedingStockEventSerializer, self).update(
            instance, validated_data
        )

        if animals_list:
            SingleBreedingStockEvent.objects.filter(event=instance).exclude(
                animal__in=animals_list
            ).delete()

            for pk in animals_list:
                sb1 = SingleBreedingStockEvent.objects.filter(event=instance).last()

                if sb1:
                    if sb1.animal.farm == BreedingStock.objects.get(pk=pk).farm:
                        SingleBreedingStockEvent.objects.get_or_create(
                            event=instance, animal=pk
                        )
                else:
                    SingleBreedingStockEvent.objects.get_or_create(
                        event=instance, animal=pk
                    )

        merge_events(BreedingStockEvent, SingleBreedingStockEvent, instance, the_farm)

        return instance


# class BreedingStockEventAnimalSerializer(EventSerializer):
#     tag_number = serializers.CharField(source='animal.tag_number')

#     class Meta(EventSerializer.Meta):
#         fields = EventSerializer.Meta.fields + ('tag_number',)


class CalfEventSerializer(serializers.ModelSerializer):
    animals = SingleCalfEventSerializer(
        source="singlecalfevent_set", many=True, read_only=True
    )
    animals_list = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Calf.objects.all(), many=True
    )

    class Meta:
        model = CalfEvent
        fields = (
            "id",
            "title",
            "scheduled_date_range",
            "report",
            "type",
            "animals",
            "animals_list",
        )
        read_only_fields = ("id", "animals")

    def create(self, validated_data):
        animals_list = validated_data.pop("animals_list", [])
        the_farm = self.context["request"].user.farm
        validated_data["farm"] = the_farm
        calf_event = CalfEvent(**validated_data)

        merge_events(CalfEvent, SingleCalfEvent, calf_event, the_farm)

        for pk in animals_list:
            sc1 = SingleCalfEvent.objects.filter(event=calf_event).last()

            if sc1:
                if sc1.animal.farm == Calf.objects.get(pk=pk).farm:
                    SingleCalfEvent.objects.get_or_create(event=calf_event, animal=pk)
            else:
                SingleCalfEvent.objects.get_or_create(event=calf_event, animal=pk)

        return calf_event

    def update(self, instance, validated_data):
        animals_list = validated_data.pop("animals_list", None)
        the_farm = self.context["request"].user.farm

        if "id" in validated_data:
            validated_data.pop("id")  # remove id, since we already have instance obj
        instance = super(CalfEventSerializer, self).update(instance, validated_data)

        if animals_list:
            SingleCalfEvent.objects.filter(event=instance).exclude(
                animal__in=animals_list
            ).delete()

            for pk in animals_list:
                sc1 = SingleCalfEvent.objects.filter(event=instance).last()

                if sc1:
                    if sc1.animal.farm == Calf.objects.get(pk=pk).farm:
                        SingleCalfEvent.objects.get_or_create(event=instance, animal=pk)
                else:
                    SingleCalfEvent.objects.get_or_create(event=instance, animal=pk)

        merge_events(CalfEvent, SingleCalfEvent, instance, the_farm)

        return instance
