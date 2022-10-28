from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.urls import reverse
from PIL import Image


class User(AbstractUser):

    CATEGORY = [
        ('Student', 'Student'),
        ('Faculty', 'Faculty'),
    ]
    role = models.CharField(max_length=7, choices=CATEGORY, default='Student')

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    bio = models.CharField(max_length=150, blank=True, null=True)
    profile_pic = models.ImageField(default ='default_pic.jpg', upload_to='img/profile_pic/', blank=True, null=True)
    facebook_url = models.CharField(max_length=250,blank = True, null=True)
    github_url = models.CharField(max_length=250,blank = True, null=True)
    twitter_url = models.CharField(max_length=250,blank = True, null=True)
    website_url = models.CharField(max_length=250,blank = True, null=True)
    linkedin_url = models.CharField(max_length=250,blank = True, null=True)


    def __str__(self):
        return str(self.user)

    def save(self,*args, **kwargs):
        super().save()
        if (self.profile_pic):
            img = Image.open(self.profile_pic.path)

            if (img.height > 350 or img.width >350):
                output_size = (350,350)
                img.thumbnail(output_size)
                img.save(self.profile_pic.path)

    

class Posts(models.Model):

    CATEGORY = [
        ('TU', 'Tutorial'),
        ('BL', 'Blog'),
        ('TP', 'Tip'),
        ('AT', 'Article'),
        ('QU', 'Question'),
    ]
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    category = models.CharField(max_length=2, choices=CATEGORY, default='QU', )
    image_file = models.ImageField(upload_to='img/post/', blank=True, null=True)
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    votes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="votes", default=None, blank=True)
    shares = models.IntegerField(default=0)
    tags = TaggableManager()
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="favorite", default=None, blank=True)
    class Meta:
        ordering = ['-date']


    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator.username,
            "title": self.title,
            "content": self.content,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "upvotes": self.upvotes,
            "downvotes": self.downvotes,
            "shares": self.shares,
            "favorites": self.favorites,    
        }


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('postDetail',kwargs={'pk': self.id})


class Vote(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="post_votes", default=None, blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote = models.BooleanField(default=True)

    def __str__(self):
        return self.post.creator.username


class Comments(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.comment
    def get_absolute_url(self):
        return reverse('deleteComment',kwargs={'pk': self.id})

class Following(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return self.follower.username


class Shared(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="post_shared")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title


class Archive(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="post_archived")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title
