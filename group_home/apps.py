from django.apps import AppConfig


class GroupHomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'group_home'
    # 管理画面の左メニューのタイトルになります
    verbose_name = 'グループホーム運営管理'