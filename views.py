from urllib.parse import urlencode
from django.http import QueryDict
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.list import ListView
from library_staff.models import Position
from tougshire_vistas.models import Vista
from tougshire_vistas.views import (
    delete_vista,
    get_latest_vista,
    get_vista_queryset,
    make_vista,
    make_vista_fields,
    retrieve_vista,
    vista_context_data,
)


class PositionList(PermissionRequiredMixin, ListView):
    permission_required = "library_staff.view_position"
    model = Position
    paginate_by = 30

    def setup(self, request, *args, **kwargs):
        self.vista_settings = {
            "max_search_keys": 5,
            "fields": [],
        }

        self.vista_settings["fields"] = make_vista_fields(
            Position,
            field_names=[
                "title",
                "department",
            ],
        )

        self.vista_defaults = QueryDict(
            urlencode(
                [
                    (
                        "order_by",
                        [
                            "name",
                        ],
                    ),
                    ("paginate_by", self.paginate_by),
                ],
                doseq=True,
            ),
            mutable=True,
        )

        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()

        self.vistaobj = {
            "querydict": QueryDict(),
            "queryset": queryset,
            "model_name": "Position",
        }

        return get_vista_queryset(self)

    def get_paginate_by(self, queryset):
        if (
            "paginate_by" in self.vistaobj["querydict"]
            and self.vistaobj["querydict"]["paginate_by"]
        ):
            return self.vistaobj["querydict"]["paginate_by"]

        return super().get_paginate_by(self)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        vista_data = vista_context_data(self.vista_settings, self.vistaobj["querydict"])
        vista_data["labels"]["Position"] = "Position"

        context_data = {**context_data, **vista_data}
        context_data["vista_default"] = dict(self.vista_defaults)

        context_data["vistas"] = Vista.objects.filter(
            user=self.request.user, model_name="library_staff.position"
        ).all()  # for choosing saved vistas

        if self.request.POST.get("vista_name"):
            context_data["vista_name"] = self.request.POST.get("vista_name")

        context_data["count"] = self.object_list.count()

        return context_data
