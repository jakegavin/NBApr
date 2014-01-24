from django.shortcuts import render
from ranking.models import Team, RankingSite

import re
import urllib2
import math

def AvgRankingView(request):
    teams = Team.objects.all()
    sites = RankingSite.objects.all()
    num_sites = len(sites)
    source_codes = {}
    rank_info = []

    for site in sites:
        if site.url2:
            a = urllib2.urlopen(site.url1).read()
            b = urllib2.urlopen(site.url2).read()
            c = a + b
            source_codes[site] = c
        else:
            source_codes[site] = urllib2.urlopen(site.url1).read()

    for team in teams:
        team.update_rank(source_codes)
    
    # Sort the teams list by decimal_rank
    def sort_by_decrank(Team):
        return Team.decimal_rank    
    teams = sorted(teams, key=sort_by_decrank)

    context = {'teams': teams, 'sites': sites, 'num_sites': num_sites}
    
    return render(request, 'ranking/avgranklist.html', context)