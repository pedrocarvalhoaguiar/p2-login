from django.contrib import admin

from reward.models import Reward


class RewardAdmin(admin.ModelAdmin):
    model = Reward
    list_display = ('name', 'description', 'created_at')
    list_filter = ('name', 'description', 'created_at')
    fieldsets = (
        (None, {'fields': ('name', 'description', 'valid_until', 'points_needed')}),
    )
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(Reward, RewardAdmin)
