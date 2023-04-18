from rest_framework import serializers

from movies.models import ProgramModel, SeatsModel, TicketsModel



class DateFilterSerializer(serializers.Serializer):
    date = serializers.DateField(format=r'%Y-%m-%d')

    class Meta:
        fields = ['date']


class CreateTicketSerializer(serializers.Serializer):
    program_id = serializers.IntegerField()
    seats = serializers.CharField()

    class Meta:
        fields = ['program_id', 'seats']

    def validate(self, attrs):
        program_id = attrs.get('program_id')
        seats = attrs.get('seats')
        user = self.context.get('user')

        try:
            program = ProgramModel.objects.get(id=int(program_id))

            # Check if given seats are avialable
            try:
                for seat in seats.split(','):
                    # If seat is already occupied
                    s = SeatsModel.objects.get(program=program, seats_numbers__contains=seat)
                    if len(seats.split(',')) > 1:
                        raise serializers.ValidationError('One of the selected seats is already occupied.')
                    else:
                        raise serializers.ValidationError('This place is already taken.')
            except SeatsModel.DoesNotExist:
                # Seats are avialble
                try:
                    # Check if the user has already booked seats for this seance, if so, add new seats to the existing ticket
                    ticket = TicketsModel.objects.get(program=program, user=user)
                    # Get the seats object for given seanse
                    users_seats = SeatsModel.objects.get(id=ticket.seats.id)
                    # Add new seats to the seats object
                    new_seats = str(users_seats) + ',' + seats
                    users_seats.seats_numbers = new_seats
                    users_seats.save()
                except TicketsModel.DoesNotExist:
                    # Create seats object
                    reserved_seats = SeatsModel.objects.create(program=program, seats_numbers=seats)
                    # Create ticket
                    TicketsModel.objects.create(program=program, user=user, seats=reserved_seats)
        except ProgramModel.DoesNotExist:
            raise serializers.ValidationError('Given seance does not exist!')
        return attrs
