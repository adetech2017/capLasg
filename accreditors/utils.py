from datetime import datetime
from .models import Accreditor



def generate_unique_string():
    # Get the last two digits of the current year
    current_year = datetime.now().year % 100

    # Read the last counter from the Accreditor table
    last_accreditor = Accreditor.objects.order_by('-id').first()
    if last_accreditor:
        last_counter = int(last_accreditor.accreditor_code[-4:])
    else:
        last_counter = 0

    # Increment the counter and pad it with leading zeros
    counter = last_counter + 1
    counter_padded = str(counter).zfill(4)

    # Combine the components to form the unique string
    unique_string = f"{current_year:02d}{counter_padded}"
    return unique_string
