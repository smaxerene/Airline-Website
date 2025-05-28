from django.core.management.base import BaseCommand
from booking.models import Airport, Aircraft, ScheduledFlight
from datetime import datetime, timedelta, time
import pytz

class Command(BaseCommand):
    help = 'Loads all predefined scheduled flights'

    def handle(self, *args, **kwargs):
        # Set up airports (ensure these exist in DB)
        airports = {
            'NZNE': Airport.objects.get(code='NZNE'),  # Dairy Flat
            'YMML': Airport.objects.get(code='YMML'),  # Melbourne
            'NZRO': Airport.objects.get(code='NZRO'),  # Rotorua
            'NZGB': Airport.objects.get(code='NZGB'),  # Great Barrier
            'NZCI': Airport.objects.get(code='NZCI'),  # Chatham Islands
            'NZTL': Airport.objects.get(code='NZTL'),  # Lake Tekapo
        }

        aircrafts = {
            'SyberJet1': Aircraft.objects.get(name='SyberJet1'),
            'SyberJet2': Aircraft.objects.get(name='SyberJet2'),
            'CirrusJet1': Aircraft.objects.get(name='CirrusJet1'),
            'CirrusJet2': Aircraft.objects.get(name='CirrusJet2'),
            'HondaJet1': Aircraft.objects.get(name='HondaJet1'),
            'HondaJet2': Aircraft.objects.get(name='HondaJet2'),
        }

        base_date = datetime.today().date()

        def create_flight(flight_number, origin, destination, dep_date, dep_time, duration_minutes, aircraft, price):
            origin_tz = pytz.timezone(origin.timezone)
            destination_tz = pytz.timezone(destination.timezone)

            dep_datetime = origin_tz.localize(datetime.combine(dep_date, dep_time))
            arr_datetime = dep_datetime + timedelta(minutes=duration_minutes)
            arr_datetime = arr_datetime.astimezone(destination_tz)

            return ScheduledFlight.objects.create(
                flight_number=flight_number,
                origin=origin,
                destination=destination,
                departure_time=dep_datetime,
                arrival_time=arr_datetime,
                aircraft=aircraft,
                price=price
            )

        flights = []

        # Melbourne (weekly)
        for week in range(4):
            friday = base_date + timedelta(days=(4 - base_date.weekday()) % 7 + week * 7)
            sunday = friday + timedelta(days=2)
            flights.append(create_flight("DF100", airports['NZNE'], airports['YMML'], friday, time(10, 0), 240, aircrafts['SyberJet1'], 999))
            flights.append(create_flight("DF101", airports['YMML'], airports['NZNE'], sunday, time(15, 0), 270, aircrafts['SyberJet2'], 999))

        # Rotorua (weekdays x2)
        for i in range(5):  # Monday–Friday
            weekday = base_date + timedelta(days=(i - base_date.weekday()) % 7)
            flights.append(create_flight("DF200", airports['NZNE'], airports['NZRO'], weekday, time(7, 0), 60, aircrafts['CirrusJet1'], 150))
            flights.append(create_flight("DF201", airports['NZRO'], airports['NZNE'], weekday, time(9, 0), 55, aircrafts['CirrusJet1'], 150))
            flights.append(create_flight("DF202", airports['NZNE'], airports['NZRO'], weekday, time(16, 0), 60, aircrafts['CirrusJet1'], 150))
            flights.append(create_flight("DF203", airports['NZRO'], airports['NZNE'], weekday, time(18, 0), 55, aircrafts['CirrusJet1'], 150))

        # Great Barrier (Mon/Wed/Fri outbound, Tue/Thu/Sat return)
        outbound_days = [0, 2, 4]
        return_days = [1, 3, 5]
        for i in range(3):
            out_day = base_date + timedelta(days=(outbound_days[i] - base_date.weekday()) % 7)
            ret_day = base_date + timedelta(days=(return_days[i] - base_date.weekday()) % 7)
            flights.append(create_flight(f"DF3{i}0", airports['NZNE'], airports['NZGB'], out_day, time(8, 30), 45, aircrafts['CirrusJet2'], 120))
            flights.append(create_flight(f"DF3{i}1", airports['NZGB'], airports['NZNE'], ret_day, time(9, 30), 45, aircrafts['CirrusJet2'], 120))

        # Chatham Islands (Tue/Fri outbound, Wed/Sat return)
        out_days = [1, 4]
        ret_days = [2, 5]
        for i in range(2):
            out_day = base_date + timedelta(days=(out_days[i] - base_date.weekday()) % 7)
            ret_day = base_date + timedelta(days=(ret_days[i] - base_date.weekday()) % 7)
            flights.append(create_flight(f"DF4{i}0", airports['NZNE'], airports['NZCI'], out_day, time(8, 0), 120, aircrafts['HondaJet1'], 450))
            flights.append(create_flight(f"DF4{i}1", airports['NZCI'], airports['NZNE'], ret_day, time(10, 0), 110, aircrafts['HondaJet1'], 450))

        # Lake Tekapo (Mon out, Tue return)
        mon = base_date + timedelta(days=(0 - base_date.weekday()) % 7)
        tue = mon + timedelta(days=1)
        flights.append(create_flight("DF500", airports['NZNE'], airports['NZTL'], mon, time(9, 0), 180, aircrafts['HondaJet2'], 400))
        flights.append(create_flight("DF501", airports['NZTL'], airports['NZNE'], tue, time(10, 0), 170, aircrafts['HondaJet2'], 400))

        self.stdout.write(self.style.SUCCESS(f"✅ Loaded {len(flights)} scheduled flights."))
