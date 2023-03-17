from .models import TicketsModel

from datetime import datetime


def check_if_refundable(ticket_id) -> bool:
    """
    Checks whether the ticket is refundable
    Ticket is refundable if difference between seance and current date is not less than 12 hours
    """
    ticket = TicketsModel.objects.get(id=int(ticket_id))
    date_format = r'%Y-%m-%d %H:%M:%S'
    # Create string with the same format
    ticket_date = ticket.program.date.strftime(date_format)
    todays_date = datetime.now().strftime(date_format)
    
    # Create datetime object based on previous strings
    start = datetime.strptime(ticket_date, date_format)
    end = datetime.strptime(todays_date, date_format)

    # Calculate the difference
    diff = start - end

    # Convert to hours
    diff_in_hours = diff.total_seconds() / 3600

    return True if diff_in_hours >= 12 else False