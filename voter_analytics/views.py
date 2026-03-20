# File: views.py
# Author: Louis Szeto (szetol@bu.edu), 3/20/2026
# Description: Implements list, detail, and graph views with complex filtering logic.

from django.views.generic import ListView, DetailView
from .models import Voter
from datetime import date
import plotly
import plotly.graph_objects as go

class VoterListView(ListView):
    """View to display a paginated list of voters with filtering options."""
    template_name = 'voter_analytics/voter_list.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        """Filter the queryset based on GET parameters."""
        qs = super().get_queryset()
        
        # Handle filtering
        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        
        if party:
            qs = qs.filter(party_affiliation=party)
        if min_dob:
            qs = qs.filter(date_of_birth__year__gte=min_dob)
        if max_dob:
            qs = qs.filter(date_of_birth__year__lte=max_dob)
        if voter_score:
            qs = qs.filter(voter_score=voter_score)
            
        # Specific election checkboxes
        for election in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
            if self.request.GET.get(election):
                qs = qs.filter(**{election: True})
                
        return qs.order_by('last_name')

    def get_context_data(self, **kwargs):
        """Add additional context for the search form."""
        context = super().get_context_data(**kwargs)
        # Unique parties and birth years to populate dropdowns
        context['parties'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        context['years'] = range(1913, 2026)
        context['scores'] = range(6)
        return context

class VoterDetailView(DetailView):
    """View to display detailed information for a single voter."""
    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'v'

class VoterGraphsView(VoterListView):
    """View to display aggregate voter data using Plotly graphs."""
    template_name = 'voter_analytics/graphs.html'
    paginate_by = None 
    def get_context_data(self, **kwargs):
        # start with superclass context (which contains our filtered queryset)
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        #Distribution of Voters by Year of Birth
        years = [v.date_of_birth.year for v in voters]
        year_counts = {}
        for y in years:
            year_counts[y] = year_counts.get(y, 0) + 1
        
        # Sort by year for the x-axis
        sorted_years = sorted(year_counts.keys())
        counts_per_year = [year_counts[y] for y in sorted_years]

        fig1 = go.Bar(x=sorted_years, y=counts_per_year)
        graph_div_dob = plotly.offline.plot({
            "data": [fig1],
            "layout": {"title": "Distribution of Voters by Year of Birth", "xaxis_title": "Year", "yaxis_title": "Count"}
        }, auto_open=False, output_type="div")
        context['graph_div_dob'] = graph_div_dob


        # Distribution of Voters by Party Affiliation
        party_counts = {}
        for v in voters:
            party_counts[v.party_affiliation] = party_counts.get(v.party_affiliation, 0) + 1
        
        labels_party = list(party_counts.keys())
        values_party = list(party_counts.values())

        fig2 = go.Pie(labels=labels_party, values=values_party)
        graph_div_party = plotly.offline.plot({
            "data": [fig2],
            "layout": {"title": "Voters by Party Affiliation"}
        }, auto_open=False, output_type="div")
        context['graph_div_party'] = graph_div_party


        #Participation in Elections
        election_names = ['2020 State', '2021 Town', '2021 Primary', '2022 General', '2023 Town']
        election_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        
        # Count how many voters have 'True' for each field
        participation_y = [voters.filter(**{field: True}).count() for field in election_fields]

        fig3 = go.Bar(x=election_names, y=participation_y)
        graph_div_participation = plotly.offline.plot({
            "data": [fig3],
            "layout": {"title": "Voter Participation per Election", "xaxis_title": "Election", "yaxis_title": "Number of Voters"}
        }, auto_open=False, output_type="div")
        context['graph_div_participation'] = graph_div_participation

        return context