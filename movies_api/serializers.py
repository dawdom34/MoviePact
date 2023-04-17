from rest_framework import serializers



class DateFilterSerializer(serializers.Serializer):
    date = serializers.DateField(format=r'%Y-%m-%d')

    class Meta:
        fields = ['date']

