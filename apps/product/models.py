from django.db import models
from django.utils import formats
from tinymce.models import HTMLField
from utils.persian_slugify import persian_slugify


class BaseInformationModel(models.Model):
    title = models.CharField(max_length=127, verbose_name="نام")
    description = HTMLField(verbose_name='توضیحات')
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Product(BaseInformationModel):
    price = models.IntegerField(verbose_name="قیمت")
    discount = models.PositiveSmallIntegerField(default=0, verbose_name="درصد تخفیف")
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    rating = models.DecimalField(default=3, max_digits=2, decimal_places=1, editable=0, verbose_name='امتیاز محصول')
    reviews = models.PositiveIntegerField(default=0, editable=False, verbose_name="تعداد بررسی ها")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد محصول')
    visits = models.PositiveIntegerField(default=0, editable=False, verbose_name='بازدیدها')
    featured = models.BooleanField(default=False, verbose_name='منتخب')
    sales = models.PositiveIntegerField(default=0, editable=False, verbose_name='تعداد فروش')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    active_objects = ActiveProductManager()
    objects = models.Manager()

    class Meta:
        abstract = True

    def __len__(self):
        return self.stock

    def discounted_price(self):
        if self.discount > 0:
            return int(self.price * (100 - self.discount) / 100)
        else:
            return self.price

    def is_available(self):
        return True if self.stock > 0 else False


class Category(BaseInformationModel):
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Mechanism(BaseInformationModel):
    class Meta:
        verbose_name = 'مکانیزم'
        verbose_name_plural = 'مکانیزم ها'


class Designer(BaseInformationModel):
    class Meta:
        verbose_name = 'طراح بازی'
        verbose_name_plural = 'طراحین بازی'


class Publisher(BaseInformationModel):
    class Meta:
        verbose_name = 'ناشر'
        verbose_name_plural = 'ناشرین'


class BoardGame(Product):
    bgg_id = models.IntegerField(verbose_name='آیدی بردگیم گیک')
    side_description = HTMLField(verbose_name="توضیحات کنار عکس")
    player_count_min = models.SmallIntegerField(verbose_name="حداقل تعداد بازیکنان")
    player_count_max = models.SmallIntegerField(verbose_name="حداکثر تعداد بازیکنان")
    time_min = models.SmallIntegerField(verbose_name="حداقل زمان بازی")
    time_max = models.SmallIntegerField(verbose_name="حداکثر زمان بازی")
    age = models.SmallIntegerField(verbose_name="حداقل سن بازیکنان")
    complexity = models.FloatField(verbose_name="سختی بازی")
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, related_name='boardgames', verbose_name='ناشر')
    designers = models.ManyToManyField(Designer, verbose_name='طراح(های) بازی', related_name='boardgames')
    categories = models.ManyToManyField(Category, verbose_name='دسته بندی(ها)', related_name='boardgames')
    mechanisms = models.ManyToManyField(Mechanism, verbose_name='مکانیزم(ها)', related_name='boardgames')

    class Meta:
        verbose_name = 'بردگیم'
        verbose_name_plural = 'بردگیم ها'

    def complexity_in_word(self):
        complexity = self.complexity
        if complexity < 2:
            return 'سبک'
        elif complexity < 3:
            return 'نیمه سبک'
        elif complexity < 4:
            return 'نیمه سنگین'
        elif complexity <= 5:
            return 'سنگین'


# the model inherited from Product
PRODUCT_MODEL = BoardGame


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products', verbose_name="تصویر")
    featured = models.BooleanField(verbose_name="تصویر شاخص")
    product = models.ForeignKey(PRODUCT_MODEL, on_delete=models.CASCADE, related_name='images', verbose_name='محصول')

    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصاویر محصول'

    def __str__(self):
        return self.image.name

