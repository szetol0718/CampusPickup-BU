# File: models.py
# Author: Louis Szeto (szetol@bu.edu), 3/20/2026
# Description: Defines the Voter model and includes a robust data import function that handles messy date strings.

from django.db import models
import csv
from datetime import datetime

class Voter(models.Model):
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.IntegerField()
    street_name = models.TextField()
    apt_number = models.TextField(blank=True, null=True)
    zip_code = models.TextField()
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.TextField()
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.party_affiliation})"

def parse_date(date_str):
    if not date_str or date_str.strip() == "":
        return datetime(1900, 1, 1).date() 
    try:
        return datetime.strptime(date_str.strip(), '%Y-%m-%d').date()
    except ValueError:
        try:
            return datetime.strptime(date_str.strip(), '%m/%d/%Y').date()
        except ValueError:
            return datetime(1900, 1, 1).date()

def load_data():
    """
    Reads the CSV and creates Voter objects using robust date parsing.
    """
    Voter.objects.all().delete()
    filename = 'newton_voters.csv'
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Conversion logic
            v = Voter(
                last_name=row['Last Name'],
                first_name=row['First Name'],
                street_number=int(row['Residential Address - Street Number']),
                street_name=row['Residential Address - Street Name'],
                apt_number=row['Residential Address - Apartment Number'] or None,
                zip_code=row['Residential Address - Zip Code'],
                # Use the robust parser for both date fields
                date_of_birth=parse_date(row['Date of Birth']),
                date_of_registration=parse_date(row['Date of Registration']),
                party_affiliation=row['Party Affiliation'].strip(),
                precinct_number=row['Precinct Number'],
                v20state=row['v20state'].upper() == 'TRUE',
                v21town=row['v21town'].upper() == 'TRUE',
                v21primary=row['v21primary'].upper() == 'TRUE',
                v22general=row['v22general'].upper() == 'TRUE',
                v23town=row['v23town'].upper() == 'TRUE',
                voter_score=int(row['voter_score'])
            )
            v.save()
            
    print(f"Done! Successfully imported {Voter.objects.count()} records.")