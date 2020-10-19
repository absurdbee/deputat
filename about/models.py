from django.db import models


class Feedback(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=50)
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Сообщение', max_length=500)

    class Meta:
        verbose_name = 'Сообщение с формы связи'
        verbose_name_plural = 'Сообщения с формы связи'
        
    def __str__(self):
        return 'Имя: {}'.format(self.name)
