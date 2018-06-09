from django.utils.translation import ugettext as _ #引用国际化i18n
from django.utils.six import python_2_unicode_compatible
from django.db import models
from django.urls import reverse
from users.models import User

# Create your models here.
@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Book(models.Model):
    class Meta:
        verbose_name = '图书'
        verbose_name_plural = verbose_name
    isbn          = models.CharField('ISBN', max_length=13, unique=True)
    title           = models.CharField('书名', max_length=200)
    subtitle           = models.CharField('副标题', max_length=200, blank=True)
    pages           = models.IntegerField('页数', blank=True)
    author          = models.CharField('作者', max_length=60)
    translator          = models.CharField('译者', max_length=60, blank=True)
    price           = models.CharField('定价', max_length=60, blank=True)
    publisher       = models.CharField('出版社', max_length=200, blank=True)
    pubdate         = models.CharField('出版日期', max_length=60, blank=True)
    cover_img        = models.URLField('封面图', blank=True)
    summary        = models.TextField ('内容简介', blank=True, max_length=2000)
    author_intro        = models.TextField ('作者简介', blank=True, max_length=2000)
    available        = models.NullBooleanField ('是否可借', blank=True, default=True)
    create_time        = models.DateField ('入库时间', auto_now_add=True)
    borrower           = models.ForeignKey(User,verbose_name=_(u'借阅者'), blank=True, null=True,on_delete=models.CASCADE)
    borrow_date        = models.DateField('借阅日期', blank=True, null=True)
    return_date        = models.DateField('归还日期', blank=True, null=True)
    tags               = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.title
    def get_fields(self):
        # make a list of field/values.
        return [(field, field.value_to_string(self)) for field in Book._meta.fields]
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('library:detail', kwargs={'pk': self.pk})