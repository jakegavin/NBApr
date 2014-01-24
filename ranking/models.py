from django.db import models
import re

class Team(models.Model):
    name = models.CharField(max_length=70)
    city = models.CharField(max_length=70, blank=True)
    current_rank = models.IntegerField(blank=True, null=True)
    decimal_rank = models.DecimalField(decimal_places=7, max_digits=10, blank=True, null=True)
	
	# Sloppy - Fix this 
    def __unicode__(self):
        if self.name == 'Blazers':
            return self.city + ' Trail ' + self.name
        else:
            return self.city + ' ' + self.name
    
    def update_rank(self, site_sources):
        '''Update the rank given site_sources dict which has the source for all ranking sites'''
        ranks = []
        for site in site_sources.keys():
            source_code = site_sources[site]
            regex_pieces = site.split_regex()
            regex_term = regex_pieces[0] + re.escape(self.name) + regex_pieces[1]
            regex = re.findall(regex_term, source_code, re.I)
            if regex:
                ranks.append(int(regex[0][0]))
            else:
                pass
        if ranks:
            self.decimal_rank = round(float(sum(ranks)) / float(len(ranks)), 3)
            self.current_rank = int(round(self.decimal_rank))
        else:
            self.decimal_rank = None
            self.current_rank = None
        self.save()

class RankingSite(models.Model):
    name = models.CharField(max_length=70)
    author = models.CharField(max_length=70)
    publisher = models.CharField(max_length=70, blank=True)
    url1 = models.URLField(max_length=200)
    url2 = models.URLField(max_length=200, blank=True)
    regex = models.TextField('Regex (group1 - Rank, group 2 - Team). Use %team.name% for team.name', blank=True)

    def split_regex(self):
        match = re.search(r'.*(%team.name%).*', self.regex)
        regex1 = self.regex[:match.start(1)]
        regex2 = self.regex[match.start(1)+11:]
        return regex1, regex2

    def __unicode__(self):
        return self.name
