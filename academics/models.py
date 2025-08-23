from django.db import models
from django.urls import reverse

# Create your models here.

class Academics(models.Model):
    RESOURCE_TYPES = [
        ('notes', 'Notes'),
        ('pyqs', 'Previous Year Questions'),
        ('books', 'Books'),
    ]

    DEPARTMENTS = [
        ('cse', 'Computer Science and Engineering'),
        ('it', 'Information Technology'),
        ('ece', 'Electronics and Communication Engineering'),
        ('mech', 'Mechanical Engineering'),
        ('civil', 'Civil Engineering'),
        ('chem', 'Chemical Engineering'),
        ('bt', 'Biotechnology'),
        ('math', 'Mathematics'),
        ('phy', 'Physics'),
        ('chemistry', 'Chemistry'),
    ]

    YEARS = [
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES, default='notes')

    department = models.CharField(max_length=10, choices=DEPARTMENTS)
    year = models.CharField(max_length=1, choices=YEARS)
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=20)

    file = models.FileField(upload_to='academic_resources/')
    external_link = models.URLField(blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")

    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.title} ({self.subject_name})"
    
    def get_absolute_url(self):
        return reverse('academics:resource_detail', kwargs={'pk': self.pk})
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_department_display_name(self):
        return dict(self.DEPARTMENTS).get(self.department, self.department)
    