from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Questao(models.Model):
    
    area_choices = [
        ["Matemática", "Matemática"],
        ["Hardware", "Hardware"],
        ["Software", "Software"],
        ["Inteligência Artificial", "Inteligência Artificial"],
        ["Lógica", "Lógica"],
        ["Programação", "Programação"],
        ["Física", "Física"],
        ["Química", "Química"],
        ["Ciclo Básico", "Ciclo Básico"]
    ]

    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    body = models.TextField(null=False)
    area = models.CharField(max_length=200, choices=area_choices, null=False, default='Ciclo Básico')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return self.title
    
    def get_responses(self):
        return self.responses.filter(parent=None)
    
class Resposta(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    question = models.ForeignKey(Questao, null=False, on_delete=models.CASCADE, related_name='responses')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return self.body

    def get_responses(self):
        return Resposta.objects.filter(parent=self)

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.body

class Poll(models.Model):
    title = models.CharField(max_length=200, null=False)
    body = models.TextField(null=False)
    option_one = models.CharField(max_length=30)
    option_two = models.CharField(max_length=30)
    option_three = models.CharField(max_length=30)
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)
    option_three_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total(self):
        return self.option_one_count + self.option_two_count + self.option_three_count

    def __str__(self): 
        return self.title
    
    def get_responses(self):
        return self.responses.filter(parent=None)
