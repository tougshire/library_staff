from django.db import models


class Department(models.Model):
    name = models.CharField(
        "name",
        max_length=80,
        help_text="The name of the department",
    )

    class Meta:
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name


class Position(models.Model):
    title = models.CharField(
        "title",
        max_length=80,
        help_text="The title of the position",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        help_text="The department of this position",
    )

    class Meta:
        ordering = [
            "department",
            "title",
        ]

    def __str__(self):
        return self.title


class Member(models.Model):
    friendly_name = models.CharField(
        "friendly name",
        max_length=50,
        help_text="The person's first name or a nick name",
    )
    last_name = models.CharField(
        "last name",
        max_length=50,
        help_text="The person's last name",
    )
    full_name = models.CharField(
        "full name",
        max_length=80,
        help_text="The legal first name and last name, optional middle names and additional name parts, of the staff member",
    )

    class Meta:
        ordering = ["last_name", "friendly_name"]

    def __str__(self):
        return f"{self.friendly_name} {self.last_name}"


class StaffPosition(models.Model):
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        help_text="The staff member assicated with the position",
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        help_text="The position filled by the staff member",
    )

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return f"{self.position} > {self.member}"


class AssignableType(models.Model):
    name = models.CharField(
        "name",
        max_length=80,
        help_text="The name of the type",
    )

    class Meta:
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name


class Assignable(models.Model):
    name = models.CharField(
        "name",
        max_length=80,
        help_text="The name of the type",
    )
    type = models.ForeignKey(
        AssignableType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The type of this assignable item",
    )

    class Meta:
        ordering = [
            "type",
            "name",
        ]

    def __str__(self):
        return self.name


class AssignableTo(models.Model):
    Position = models.ForeignKey(Member, on_delete=models.CASCADE, help_text="The ")
