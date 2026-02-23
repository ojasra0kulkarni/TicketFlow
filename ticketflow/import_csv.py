import os
import django
import csv
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ticketflow.settings")
django.setup()

from ticketflowapp.models import Ticket

file_path = "tickets_export.csv"

with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    print("CSV Columns:")
    print(reader.fieldnames)

    for row in reader:
        Ticket.objects.create(
            ticket_id=row['Ticket ID'],
            priority=row['Priority'],
            status=row['Status'],
            subject=row['Subject'],
            description=row['Description'],
            address=row['Address'],
            order_id=row['order_id'],
            raised_at=datetime.fromisoformat(row['Raised At']),
            closed_at=datetime.fromisoformat(row['Closed At']) if row['Closed At'] else None
        )

print("✅ Data Imported Successfully")