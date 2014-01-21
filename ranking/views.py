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
        ranks = []
        for site in sites:
            source_code = source_codes[site]
            regex_pieces = site.split_regex()
            regex_term = regex_pieces[0] + re.escape(team.name) + regex_pieces[1]
            regex = re.findall(regex_term, source_code, re.I)
            if regex:
                ranks.append(int(regex[0][0]))
            else:
                pass
        if ranks:
            team.decimal_rank = round(float(sum(ranks)) / float(len(ranks)), 3)
            team.current_rank = int(round(team.decimal_rank))
        else:
            team.decimal_rank = None
            team.current_rank = None
        team.save()
    
    # Sort the teams list by decimal_rank
    def sort_by_decrank(Team):
        return Team.decimal_rank    
    teams = sorted(teams, key=sort_by_decrank)

    context = {'teams': teams, 'sites': sites, 'num_sites': num_sites}
    
    return render(request, 'ranking/avgranklist.html', context)