from django import forms
from django.contrib import admin
from .models import Category,Genre,Movie,MovieShots,Actor,Rating,RatingStar,Reviews
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget



class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание" ,widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'
        
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display =["id","name", "url"] 
    list_display_links = ("name",) #ссылка

class ReviewInline(admin.TabularInline): # StackedInline
    model = Reviews
    extra = 1 #количества дополнительных полей 
    readonly_fields = ("name", "email")

class MovieShotsInline(admin.StackedInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" height="160"')

    get_image.short_description = "Изображение"

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display =["title","category", "url", "draft"]
    list_display_links = ("title",) #ссылка
    list_filter = ("category", "year")  #добавление фильтра
    search_fields = ("title", "category__name") #поиск
    inlines = [ReviewInline, MovieShotsInline]  #прикрепляет отзывы,кадры
    save_on_top = True #меню удалить и.т.д будет в начале и в конце
    save_as = True #помогает не переписывать кароче сондай
    list_editable = ("draft",) #поле черновик превращается в чеклист
    actions = ["publish","unpublish"]
    readonly_fields = ("get_image",)
    form = MovieAdminForm

    # fields = (("actors", "directors", "genres"),)
    fieldsets = (
        (None,{
            "fields": (("title", "tagline"),)
        }),
        (None,{
            "fields": (("description", "poster","get_image"),)
        }),
        (None,{
            "fields": (("year", "world_premiere", "country",),)
        }),
        ("Actors",{
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        ("Options",{
            "fields": (("bydget", "fees_in_usa", "fees_in_world"),)
        }),
        (None,{
            "fields": (("url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="150" height="160"')

    def unpublish(self, request, queryset):
        #снять с публикации
        row_update = queryset.update(draft = True)
        if row_update == 1:
            message_bit = "1 запись обновлена"
        else:message_bit = f"{row_update} записей была обновлена"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        #опубликовать с публикации
        row_update = queryset.update(draft = False)
        if row_update ==1:
            message_bit = "1 запись обновлена"
        else:message_bit = f"{row_update} записей была обновлена"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permission = ('change',)

    unpublish.short_description = "снять с публикации"
    unpublish.allowed_permission = ('change',)

    get_image.short_description = "Постер"

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display =["name","email", "parent", "movie", "id"]
    readonly_fields = ("name", "email") #это дает возможность только для чтения

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "age","get_image")
    readonly_fields = ("get_image",)
    
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "movie", "ip")
    
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")


admin.site.register(RatingStar)

admin.site.site_title = "Админка сайта"
admin.site.site_header = "Админка сайта"
