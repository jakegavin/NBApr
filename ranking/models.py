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
