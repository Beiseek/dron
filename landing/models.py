from django.db import models

class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class AboutBlock(SingletonModel):
    title = models.CharField(max_length=200, default="Тренажер БПЛА с реалистичной физикой и режимом от первого лица")
    text_in_frame = models.TextField(default="Отрабатывайте пилотирование в реальных полетных условиях и на разнообразных картах в режиме свободного полета. Усложните задачу: выследите и найдите подвижную цель на локациях с помощью специального режима «Поиск».")
    subtitle = models.CharField(max_length=200, default="Симулятор FPV дронов с детально проработанной физикой")

    def __str__(self):
        return "Основной блок 'О нас'"

class Trailer(SingletonModel):
    title = models.CharField(max_length=200, default="Трейлер симулятора", verbose_name="Заголовок секции")
    subtitle = models.TextField(default="Посмотрите видео, чтобы узнать больше о возможностях нашего симулятора", verbose_name="Подзаголовок секции")
    video_url = models.URLField(blank=True, null=True, help_text="URL видео с YouTube или другого видеохостинга")
    local_video = models.FileField(upload_to='videos/', blank=True, null=True, help_text="Либо загрузите видеофайл")

    def __str__(self):
        return "Трейлер"

class ProductInfo(SingletonModel):
    title = models.CharField(max_length=200, default="О продукте", verbose_name="Заголовок блока 'О продукте'")
    image = models.ImageField(upload_to='product_images/')
    description = models.TextField(default="""Симулятор управления дроном создан для тренировки навыков управления БПЛА. В нем представлено множество локаций и сценариев, таких как:

пилотирование дрона в городе;
использование дрона в лесной и сельской местности;
полеты на заброшенном заводе;
гонки на дронах;
и другие.

Каждый из биомов обладает своими уникальными особенностями, а вариативность сложности трасс позволяет беспрерывно оттачивать навыки пилотирования на высокой скорости. Это комплексное решение предназначено для подготовки как начинающих спортсменов, так и профессионалов дрон-рейсинга и не имеет аналогов в Российской Федерации.""")

    def __str__(self):
        return "Блок информации о продукте"

class ScreenshotAlbum(models.Model):
    title = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Screenshot(models.Model):
    album = models.ForeignKey(ScreenshotAlbum, on_delete=models.CASCADE, related_name='screenshots')
    image = models.ImageField(upload_to='screenshots/')
    caption = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Скриншот для {self.album.title}"

class AppScreenshot(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='app_screenshots/')
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Version(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    supported_os = models.CharField(max_length=300, default="Linux, Windows, macOS, РЕД ОС, Astra Linux, uncomOS")

    def __str__(self):
        return self.title

class FPVMode(SingletonModel):
    title = models.CharField(max_length=200, default="FPV режим", verbose_name="Заголовок FPV режима")
    image = models.ImageField(upload_to='fpv_images/')
    description = models.TextField(default="Симулятор FPV дронов с детально проработанной физикой для тренировок в режиме от первого лица.", verbose_name="Описание FPV режима")

    def __str__(self):
        return "Блок FPV режима"

class PurchaseOption(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    features = models.TextField(verbose_name="Особенности (каждая с новой строки)", default="Полный доступ к симулятору\nВсе локации и режимы\nТехническая поддержка")
    is_custom = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_features_list(self):
        return [feature.strip() for feature in self.features.split('\n') if feature.strip()]

class Footer(SingletonModel):
    email = models.EmailField(default="m.korovob@yandex.ru")
    phone = models.CharField(max_length=20, default="8 900 478 43 84")
    our_logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    partner_logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return "Футер"

class ContactForm(models.Model):
    PACKAGE_CHOICES = (
        ('basic', 'Базовая версия'),
        ('custom', 'Кастомная версия'),
    )

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    organization_name = models.CharField(max_length=200)
    package = models.CharField(max_length=20, choices=PACKAGE_CHOICES, default='basic')
    comment = models.TextField(blank=True, null=True)
    privacy_policy_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка от {self.full_name} ({self.organization_name})"


class PrivacyPolicy(SingletonModel):
    title = models.CharField(max_length=200, default="Политика конфиденциальности", verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление")
    
    class Meta:
        verbose_name = "Политика конфиденциальности"
        verbose_name_plural = "Политика конфиденциальности"
    
    def __str__(self):
        return self.title

class ContactFormSettings(SingletonModel):
    title = models.CharField(max_length=200, default="Заявка на приобретение лицензии", verbose_name="Заголовок формы")
    subtitle = models.TextField(default="Заполните форму, мы свяжемся с вами по указанным контактным данным и обсудим лучшие варианты приобретения симулятора", verbose_name="Описание формы")
    button_text = models.CharField(max_length=100, default="Заполнить форму", verbose_name="Текст кнопки")
    
    class Meta:
        verbose_name = "Настройки формы обратной связи"
        verbose_name_plural = "Настройки формы обратной связи"
    
    def __str__(self):
        return "Настройки формы обратной связи"


class PageSettings(SingletonModel):
    favicon = models.ImageField(upload_to='favicons/', blank=True, null=True, verbose_name="Фавикон (иконка сайта)")

    gallery_title = models.CharField(max_length=200, default="Галерея скриншотов", verbose_name="Заголовок секции 'Галерея'")
    gallery_subtitle = models.TextField(default="Посмотрите на реалистичную графику и разнообразие локаций", verbose_name="Подзаголовок секции 'Галерея'")

    app_gallery_title = models.CharField(max_length=200, default="Интерфейс приложения", verbose_name="Заголовок секции 'Интерфейс'")
    app_gallery_subtitle = models.TextField(default="Удобный и интуитивный интерфейс для комфортной работы", verbose_name="Подзаголовок секции 'Интерфейс'")

    versions_title = models.CharField(max_length=200, default="Версии симулятора", verbose_name="Заголовок секции 'Версии'")
    versions_subtitle = models.TextField(default="Выберите версию, которая подходит именно вам", verbose_name="Подзаголовок секции 'Версии'")
    
    purchase_options_title = models.CharField(max_length=200, default="Варианты приобретения", verbose_name="Заголовок секции 'Варианты приобретения'")
    purchase_options_subtitle = models.TextField(default="Выберите подходящий тариф для ваших потребностей", verbose_name="Подзаголовок секции 'Варианты приобретения'")

    class Meta:
        verbose_name = "Настройки секций страницы"
        verbose_name_plural = "Настройки секций страницы"

    def __str__(self):
        return "Настройки секций страницы"
