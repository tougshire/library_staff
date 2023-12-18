from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest
from .models import (
    Assignable,
    AssignableTo,
    AssignableType,
    Department,
    Member,
    Position,
    StaffPosition,
)


class StaffPositionInline(admin.StackedInline):
    model = StaffPosition
    extra = 1


class AssignableToAdmin(admin.ModelAdmin):
    pass


class AssignableTypeAdmin(admin.ModelAdmin):
    pass


class AssignableAdmin(admin.ModelAdmin):
    pass


class DepartmentAdmin(admin.ModelAdmin):
    pass


class PositionAdmin(admin.ModelAdmin):
    list_display = ["__str__", "get_member", "level"]
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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # for all positions witha greater level (which actually represents a lower position):
        for position in Position.objects.filter(level__gt=obj.level):
            # if my position is in the called position's chain of command: 
            if position.in_chain(obj):
                # save() calls set_level() which adjusts the position's place chain of command level
                position.save()


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
    (Assignable, AssignableAdmin),
    (AssignableTo, AssignableToAdmin),
    (AssignableType, AssignableTypeAdmin),
    (Department, DepartmentAdmin),
    (Position, PositionAdmin),
    (Member, MemberAdmin),
    (StaffPosition, StaffPositionAdmin),
]

for model, modeladmin in model_modeladmins:
    admin.site.register(model, modeladmin)
