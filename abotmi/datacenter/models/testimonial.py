from django.db import models


def profile_picture_name(instance, filename):
    return '/'.join(['reia', "testimonial", filename])


class Testimonial(models.Model):
    '''
    headline --> The headline of the testimonial.
    description --> Testimonial content in detail.
    picture --> The picture url of the endorser.
    endorser --> The person who gives testimonial.
    endorser_designation --> Endorser's designation.
    endorser_company --> Endorser's company.
    status --> Boolean- status of the testimonial.
    '''
    headline = models.CharField(
        max_length=200, blank=True)
    description = models.TextField(blank=True)
    picture = models.ImageField(upload_to=profile_picture_name, blank=True)
    endorser = models.CharField(
        max_length=100, blank=True)
    endorser_designation = models.CharField(
        max_length=100, blank=True)
    endorser_company = models.CharField(
        max_length=100, blank=True)
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    def __unicode__(self):
        return self.headline
