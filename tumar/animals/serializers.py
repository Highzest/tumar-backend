from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers

from ..indicators.serializers import ImageryRequestSerializer
from .models import (
    Farm,
    Animal,
    Geolocation,
    Machinery,
    Cadastre,
    BreedingStock,
    BreedingBull,
    Calf,
    StoreCattle,
)


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = (
            "id",
            "farm",
            "imei",
            "tag_number",
            "name",
            "updated",
            "imsi",
            "battery_charge",
            "status",
            "image",
        )
        read_only_fields = (
            "id",
            "updated",
            "status",
            "battery_charge",
        )


class BreedingStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreedingStock
        fields = (
            "id",
            "farm",
            "tag_number",
            "name",
            "birth_date",
            "image",
            "breed",
        )
        read_only_fields = ("id",)


class CalfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calf
        fields = (
            "id",
            "farm",
            "tag_number",
            "name",
            "birth_date",
            "image",
            "breed",
            "wean_date",
            "gender",
            "mother",
        )
        read_only_fields = ("id",)


class BreedingBullSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreedingBull
        fields = (
            "id",
            "farm",
            "tag_number",
            "name",
            "birth_date",
            "image",
            "breed",
            "birth_place",
        )
        read_only_fields = ("id",)


class StoreCattleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreCattle
        fields = (
            "id",
            "farm",
            "tag_number",
            "name",
            "birth_date",
            "image",
            "wean_date",
        )
        read_only_fields = ("id",)


class CadastreSerializer(serializers.ModelSerializer):
    # since drf has a bug with required=True
    geometry = geo_serializers.GeometryField(source="geom", required=False)

    class Meta:
        model = Cadastre
        fields = (
            "id",
            "title",
            "cad_number",
            "geometry",
            "farm",
            "area",
        )


class CadastreImageryRequestSerializer(serializers.ModelSerializer):
    # since drf has a bug with required=True
    geometry = geo_serializers.GeometryField(source="geom", required=False)
    imagery_requests = ImageryRequestSerializer(many=True, read_only=True)

    class Meta:
        model = Cadastre
        fields = (
            "id",
            "title",
            "cad_number",
            "geometry",
            "area",
            "imagery_requests",
        )


class MachinerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Machinery
        fields = (
            "id",
            "farm",
            "type",
            "machinery_code",
        )


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = (
            "id",
            "user",
            "iin",
            "legal_person",
            "iik",
            "bank",
            "bin",
            "address",
            "calf_count",
            "breedingstock_count",
            "breedingbull_count",
            "storecattle_count",
            "total_pastures_area_in_ha",
        )
        read_only_fields = (
            "calf_count",
            "breedingstock_count",
            "breedingbull_count",
            "storecattle_count",
            "total_pastures_area_in_ha",
        )


class CreateFarmSerializer(serializers.ModelSerializer):
    cadastres = serializers.ListField()

    class Meta:
        model = Farm
        fields = (
            "id",
            "iin",
            "legal_person",
            "iik",
            "bank",
            "bin",
            "address",
            "cadastres",
        )

    def to_representation(self, instance):
        serializer = FarmCadastresSerializer(instance)
        return serializer.data

    def create(self, validated_data):
        cadastres = validated_data.pop("cadastres")
        validated_data["user"] = self.context["request"].user
        farm = Farm.objects.create(**validated_data)

        for cad_number in cadastres:
            Cadastre.objects.create(farm=farm, cad_number=cad_number)

        return farm


class FarmAnimalsSerializer(FarmSerializer):
    animals = AnimalSerializer(many=True, read_only=True)

    class Meta(FarmSerializer.Meta):
        fields = FarmSerializer.Meta.fields + ("animals",)


class FarmCadastresSerializer(FarmSerializer):
    cadastres = CadastreSerializer(many=True, read_only=True)

    class Meta(FarmSerializer.Meta):
        fields = FarmSerializer.Meta.fields + ("cadastres",)


class GeolocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocation
        fields = (
            "id",
            "position",
            "time",
        )


class GeolocationAnimalSerializer(GeolocationSerializer):
    animal = AnimalSerializer()

    class Meta(GeolocationSerializer.Meta):
        fields = GeolocationSerializer.Meta.fields + ("animal",)
