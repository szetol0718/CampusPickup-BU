# File: views.py
# Author: Louis Szeto (szetol@bu.edu), 3/20/2026

from django.views.generic import ListView, DetailView
from .models import Voter
from datetime import date

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
