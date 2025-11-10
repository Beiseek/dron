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
    title = models.CharField(max_length=200, default="Тренажер БПЛА с реалистичной физикой и режимом от первого лица", verbose_name="Заголовок на главном экране")
    text_in_frame = models.TextField(default="Отрабатывайте пилотирование в реальных полетных условиях и на разнообразных картах в режиме свободного полета. Усложните задачу: выследите и найдите подвижную цель на локациях с помощью специального режима «Поиск».", verbose_name="Текст в рамке")
    subtitle = models.CharField(max_length=200, default="Симулятор FPV дронов с детально проработанной физикой", verbose_name="Подзаголовок (не используется)")
    hero_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True, verbose_name="Изображение фона Hero (верхняя секция)")

    class Meta:
        verbose_name = "1. Главный блок"
        verbose_name_plural = "1. Главный блок"

    def __str__(self):
        return "Главный блок"

class Trailer(SingletonModel):
    title = models.CharField(max_length=200, default="Трейлер симулятора", verbose_name="Заголовок секции")
    subtitle = models.TextField(default="Посмотрите видео, чтобы узнать больше о возможностях нашего симулятора", verbose_name="Подзаголовок секции")
    video_url = models.URLField(blank=True, null=True, help_text="URL видео с YouTube или другого видеохостинга", verbose_name="Ссылка на YouTube видео")
    local_video = models.FileField(upload_to='videos/', blank=True, null=True, help_text="Либо загрузите видеофайл", verbose_name="Локальное видео")

    class Meta:
        verbose_name = "2. Секция 'Трейлер'"
        verbose_name_plural = "2. Секция 'Трейлер'"

    def __str__(self):
        return "Трейлер"

class ProductInfo(SingletonModel):
    title = models.CharField(max_length=200, default="О продукте", verbose_name="Заголовок")
    image = models.ImageField(upload_to='product_images/', verbose_name="Изображение")
    description = models.TextField(default="...", verbose_name="Описание")

    class Meta:
        verbose_name = "3. Блок 'О продукте'"
        verbose_name_plural = "3. Блок 'О продукте'"

    def __str__(self):
        return "Блок информации о продукте"

class ScreenshotAlbum(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Название локации")
    order = models.PositiveIntegerField(default=0, db_index=True, verbose_name="Порядок")

    class Meta:
        ordering = ['order']
        verbose_name = "Альбом скриншотов локаций"
        verbose_name_plural = "4. Альбомы скриншотов локаций"

    def __str__(self):
        return self.title

class Screenshot(models.Model):
    album = models.ForeignKey(ScreenshotAlbum, on_delete=models.CASCADE, related_name='screenshots', verbose_name="Альбом")
    image = models.ImageField(upload_to='screenshots/', verbose_name="Изображение")
    caption = models.CharField(max_length=100, blank=True, verbose_name="Подпись")

    class Meta:
        verbose_name = "Скриншот локации"
        verbose_name_plural = "Скриншоты локаций"

    def __str__(self):
        return f"Скриншот для {self.album.title}"

class AppScreenshot(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название скриншота")
    image = models.ImageField(upload_to='app_screenshots/', verbose_name="Изображение")
    description = models.TextField(blank=True, verbose_name="Описание (не используется)")
    order = models.PositiveIntegerField(default=0, db_index=True, verbose_name="Порядок")

    class Meta:
        ordering = ['order']
        verbose_name = "Скриншот интерфейса"
        verbose_name_plural = "5. Скриншоты интерфейса"

    def __str__(self):
        return self.title


class VersionsBlock(SingletonModel):
    basic_title = models.CharField(max_length=100, verbose_name="Название (Базовая)", default="Базовая версия")
    basic_description = models.TextField(verbose_name="Описание (Базовая)", default="Для школ, вузов, СПО, дополнительного образования. Подходит для обучения навыкам полета на квадрокоптерах весом до 30 кг и подготовки к решению определенных видов задач.")
    basic_supported_os = models.CharField(max_length=300, default="Linux, Windows, macOS, РЕД ОС, Astra Linux, uncomOS", verbose_name="Поддерживаемые ОС (Базовая)")

    custom_title = models.CharField(max_length=100, verbose_name="Название (Кастомная)", default="Кастомная версия")
    custom_description = models.TextField(verbose_name="Описание (Кастомная)", default="Разработка версии под ваши уникальные требования.")
    custom_supported_os = models.CharField(max_length=300, default="Linux, Windows, macOS, РЕД ОС, Astra Linux, uncomOS", verbose_name="Поддерживаемые ОС (Кастомная)")

    class Meta:
        verbose_name = "6. Секция 'Версии симулятора'"
        verbose_name_plural = "6. Секция 'Версии симулятора'"

    def __str__(self):
        return "Секция 'Версии симулятора'"


class FPVMode(SingletonModel):
    title = models.CharField(max_length=200, default="FPV режим", verbose_name="Заголовок")
    image = models.ImageField(upload_to='fpv_images/', verbose_name="Изображение")
    description = models.TextField(default="Симулятор FPV дронов с детально проработанной физикой для тренировок в режиме от первого лица.", verbose_name="Описание")

    class Meta:
        verbose_name = "7. Блок 'FPV режим'"
        verbose_name_plural = "7. Блок 'FPV режим'"

    def __str__(self):
        return "Блок FPV режима"


class PurchaseOptionsBlock(SingletonModel):
    basic_name = models.CharField(max_length=100, verbose_name="Название тарифа (Базовый)", default="Базовая версия")
    basic_price = models.CharField(max_length=100, verbose_name="Цена (Базовый)", default="5000 руб")
    basic_features = models.TextField(verbose_name="Особенности (Базовый)", default="Полный доступ к симулятору\nВсе локации и режимы\nТехническая поддержка")

    custom_name = models.CharField(max_length=100, verbose_name="Название тарифа (Кастомный)", default="Кастомная версия")
    custom_price = models.CharField(max_length=100, verbose_name="Цена (Кастомный)", default="Цена по запросу")
    custom_features = models.TextField(verbose_name="Особенности (Кастомный)", default="Индивидуальная разработка\nПерсональные настройки\nПриоритетная поддержка")

    class Meta:
        verbose_name = "8. Секция 'Варианты приобретения'"
        verbose_name_plural = "8. Секция 'Варианты приобретения'"

    def __str__(self):
        return "Секция 'Варианты приобретения'"

    def get_basic_features_list(self):
        return [feature.strip() for feature in self.basic_features.split('\n') if feature.strip()]

    def get_custom_features_list(self):
        return [feature.strip() for feature in self.custom_features.split('\n') if feature.strip()]


class Footer(SingletonModel):
    contact_title = models.CharField(max_length=200, default="Свяжитесь с нами", verbose_name="Заголовок")
    contact_subtitle = models.TextField(default="Мы всегда готовы ответить на ваши вопросы и обсудить сотрудничество.", verbose_name="Подзаголовок")
    email = models.EmailField(default="m.korovob@yandex.ru", verbose_name="Email")
    phone = models.CharField(max_length=20, default="8 900 478 43 84", verbose_name="Телефон")
    our_logo = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="Наш логотип (в футере)")
    partner_logo = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="Логотип партнера (в футере)")

    class Meta:
        verbose_name = "9. Контакты и футер"
        verbose_name_plural = "9. Контакты и футер"

    def __str__(self):
        return "Футер и блок контактов"

class PrivacyPolicy(SingletonModel):
    title = models.CharField(max_length=200, default="Политика конфиденциальности", verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление")
    
    class Meta:
        verbose_name = "Политика конфиденциальности"
        verbose_name_plural = "Политика конфиденциальности"
    
    def __str__(self):
        return self.title


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
        verbose_name = "0. Общие настройки страницы"
        verbose_name_plural = "0. Общие настройки страницы"

    def __str__(self):
        return "Общие настройки страницы"
