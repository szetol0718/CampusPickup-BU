from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("campus_pickup", "0004_ride_destination_latitude_ride_destination_longitude_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ride",
            name="pickup_time",
        ),
        migrations.RemoveField(
            model_name="ride",
            name="request_type",
        ),
    ]
