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
    reports_to = models.ForeignKey(
        "position",
        verbose_name="reports to",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reporter",
        help_text="The position that this position reports to",
    )
    level = models.IntegerField(
        "level",
        default=0,
        help_text="An automatically generated number to help with ordering",
    )

    chain = []

    class Meta:
        ordering = [
            "level",
            "department",
            "title",
        ]

    class CircularChainDetected(Exception):
        """A circle in the chain of command has been detected"""

    def __str__(self):
        return self.title

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.set_chain()
        self.set_level()

        return super().save(force_insert, force_update, using, update_fields)

    def set_chain(self):
        self.chain = []
        reports_to = self.reports_to
        while reports_to is not None:
            if reports_to == self or reports_to in self.chain:
                if reports_to == self:
                    raise (
                        self.CircularChainDetected(f"Self detected in chain of command")
                    )
                else:
                    raise (
                        self.CircularChainDetected(
                            f"{ reports_to } detected more than once in chain of command"
                        )
                    )
                break
            self.chain.append(reports_to)
            reports_to = reports_to.reports_to

    def set_level(self):
        self.level = len(self.chain)

    def in_chain(self, position_to_check):
        self.set_chain
        return position_to_check in self.chain


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
        verbose_name = "assignable item"

        ordering = [
            "type",
            "name",
        ]

    def __str__(self):
        return self.name


class AssignableTo(models.Model):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="assignable_item",
        help_text="The position to receive the item",
    )
    assignable = models.ForeignKey(
        Assignable,
        on_delete=models.CASCADE,
        help_text="The assignable item assignable to the position",
    )
    Responsible = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="responsibility",
        help_text="The position responsible to ensure the person has received the assignable item",
    )
