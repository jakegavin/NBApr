# Averaged NBA Power Rankings

This is a django-powered web app that will parse the source from a list of html sites and average an NBA teams power ranking. It then reranks the teams given their average power ranking. 

### Todo
*   Incorporate last modified into the team model
    *   Only pull new rankings from the site if the model hasn't been modified in 24
*   Improve CSS
*   Add custom filter to remove trailing comma rather than messy template tags
