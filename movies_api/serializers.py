from rest_framework import serializers

from movies.models import ProgramModel, SeatsModel, TicketsModel
from movies.utils import check_if_refundable



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
    

class ReturnTicketSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField()

    class Meta:
        fields = ['ticket_id']

    def validate(self, attrs):
        ticket_id = attrs.get('ticket_id')
        user = self.context.get('user')
        try:
            ticket = TicketsModel.objects.get(id=int(ticket_id))
            # Confirm that the ticket belong to authenticated user
            if ticket.user == user:
                # Check if ticket is refundable
                if check_if_refundable(ticket_id):
                    # Delete seats and ticket
                    seats = SeatsModel.objects.get(id=ticket.seats.id)
                    seats.delete()
                    ticket.delete()
                else:
                    raise serializers.ValidationError('You cannot return this ticket. Less than 12 hours left until the show')
            else:
                raise serializers.ValidationError('Error while returning the ticket.')
        except TicketsModel.DoesNotExist:
            raise serializers.ValidationError('Ticket does not exist.')
        return attrs
