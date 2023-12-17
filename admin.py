from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest
from .models import Department, Position, Member, StaffPosition


class StaffPositionInline(admin.StackedInline):
    model = StaffPosition
    extra = 1


class DepartmentAdmin(admin.ModelAdmin):
    pass


class PositionAdmin(admin.ModelAdmin):
    list_display = ["__str__", "get_member"]
    inlines = [StaffPositionInline]

    @admin.display(
        description="member",
    )
    def get_member(self, obj):
        staff_positions = StaffPosition.objects.filter(position=obj)
        member_names = ""
        for staff_position in staff_positions:
            member_names = member_names + f", {staff_position.member}"

        return member_names[2:]


class MemberAdmin(admin.ModelAdmin):
    list_display = ["__str__", "get_positions"]
    inlines = [StaffPositionInline]

    def get_positions(self, obj):
        staff_positions = StaffPosition.objects.filter(member=obj)
        position_names = ""
        for staff_position in staff_positions:
            position_names = position_names + f", {staff_position.position}"

        return position_names[2:]


class StaffPositionAdmin(admin.ModelAdmin):
    pass


model_modeladmins = [
    (Department, DepartmentAdmin),
    (Position, PositionAdmin),
    (Member, MemberAdmin),
    (StaffPosition, StaffPositionAdmin),
]

for model, modeladmin in model_modeladmins:
    admin.site.register(model, modeladmin)
