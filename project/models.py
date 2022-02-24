from django.utils import timezone
from django.db import models
from users.models import Profile


# Create your models here. 
class Project(models.Model):
    owner=models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photos/',null=True,blank=True,default='website.jpg')
    description = models.TextField(null=True,blank=True)
    demo_link = models.CharField(max_length=2000,null=True,blank=True)
    source_link = models.CharField(max_length=2000,null=True,blank=True)
    Tag = models.ManyToManyField('Tag',blank=True)
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(default = timezone.now)

    vote_total = models.IntegerField(default=0,null=True,blank=True)
    vote_ratio = models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return self.title

    @property
    def reviewers(self):
        return self.review_set.all().values_list('owner__id',flat=True)

    @property
    def getVoteCount(self):
        reviews=self.review_set.all()
        upVotes=reviews.filter(value='up')
        upCount = upVotes.count()
        totalCount= reviews.count()
        self.vote_total = totalCount
        self.vote_ratio = (upCount/totalCount)*100
        self.save()
        

                

class Review(models.Model):
    vote_type = [('Up','Up Vote'),
                 ('Down','Down Vote')]
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)             

    project = models.ForeignKey(Project,on_delete=models.CASCADE) 
    body = models.TextField(null=True,blank=True)
    value = models.CharField(max_length=100,choices=vote_type)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value

    class Meta:
        unique_together=[['project','owner']]    



class Tag(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.name    
        









