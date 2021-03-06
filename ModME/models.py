from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=200)
    fileName = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"


class SurveyFile(models.Model):
    survey = models.ForeignKey(Survey)
    name = models.CharField(max_length=200)


class Condition(models.Model):
    Name = models.CharField('name', max_length=200)
    experimentDuration = models.IntegerField('Length of experiment in minutes')

    task1 = models.IntegerField(default=-1)
    task1Data = models.CharField(default="{}", max_length=5000)
    task1GUI = models.BooleanField(default=False)

    task2 = models.IntegerField(default=-1)
    task2Data = models.CharField(default="{}", max_length=5000)
    task2GUI = models.BooleanField(default=False)

    task3 = models.IntegerField(default=-1)
    task3Data = models.CharField(default="{}", max_length=5000)
    task3GUI = models.BooleanField(default=False)

    task4 = models.IntegerField(default=-1)
    task4Data = models.CharField(default="{}", max_length=5000)
    task4GUI = models.BooleanField(default=False)

    surveys = models.ManyToManyField(Survey, blank=True)
    surveys.help_text = 'Hold down "Control", or "Command" on a Mac, to <em>de</em>select one.<br/>'

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = "Condition"
        verbose_name_plural = "Conditions"


class Task(models.Model):
    fileName = models.CharField(max_length=200)
    taskName = models.CharField(max_length=200)
    configurator = models.CharField(max_length=200)

    def __str__(self):
        return self.taskName


class File(models.Model):
    task = models.ForeignKey(Task)
    name = models.CharField(max_length=200)


class TableAdd(models.Model):
    tableName = models.CharField(max_length=100)
    uniqueString = models.CharField(max_length=30)
    applyed = models.BooleanField()


class Participant(models.Model):
    """ Protect a participant's confidentiality and privacy """
    alias = models.CharField(max_length=500, unique=True)

    def __unicode__(self):
        return self.alias


class Session(models.Model):
    """ A session may comprise multiple runs of one or more conditions """
    name = models.CharField(max_length=500)
    study = models.CharField(max_length=500, default='')

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (("name", "study"))


class Metadata(models.Model):
    """ Metadata describes the execution of a single condition by a participant """
    startTime = models.IntegerField()
    duration = models.IntegerField()
    session = models.ForeignKey('Session')
    condition = models.ForeignKey('Condition')
    participant = models.ForeignKey('Participant')
    allowEventReuse = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s:%s:%s" % (self.participant.alias, self.session.name, self.condition)

    class Meta:
        verbose_name_plural = "Metadata"
        unique_together = (("condition", "participant", "session"))


class Event(models.Model):
    """
    Event class has an entry every time an event of any type happens during the experiment
    Event types include input, alert, and timeout
    """
    time = models.IntegerField()
    metadata = models.ForeignKey('Metadata')
    eventType = models.CharField(max_length=200)
    chart = models.CharField(max_length=200)
    arg = models.CharField(max_length=200)
    domID = models.CharField(max_length=200)


class ResourceTank(models.Model):
    """
    Resource Tank class gets one entry for each tank in the Resource Management task at a rate given by the parameter
    Each entry gives state of a tank at that time
    """
    time = models.IntegerField()
    metadata = models.ForeignKey('Metadata')

    tankNumber = models.IntegerField()
    state = models.FloatField()

    class Meta:
        verbose_name = "Resource Tank"
        verbose_name_plural = "Resource Tanks"


class ResourceSwitch(models.Model):
    """
    Resource Tank class gets one entry for each switch in the Resource Management task at a rate given by the parameter
    Each entry gives the state of a switch at that time
    """
    time = models.IntegerField()
    metadata = models.ForeignKey('Metadata')

    switchNumber = models.IntegerField()
    state = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Resource Switch"
        verbose_name_plural = "Resource Switches"


class Tracking(models.Model):
    """
    Track class get on entry for each satellite in the Tracking task at a rate given by the parameter
    Each entry gives the state of a satellite at that time
    """
    time = models.IntegerField()
    metadata = models.ForeignKey('Metadata')

    x = models.FloatField()
    y = models.FloatField()
    domID = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    mouseX = models.FloatField()
    mouseY = models.FloatField()


class MouseTracking(models.Model):
    """
    MouseTracking class gets one entry every time the mouse moves
    Each entry give location of mouse and location of target
    """
    time = models.IntegerField()
    metadata = models.ForeignKey('Metadata')

    x = models.FloatField()
    y = models.FloatField()
    domID = models.CharField(max_length=200)
    targetX = models.FloatField()
    targetY = models.FloatField()

    class Meta:
        verbose_name = "Mouse Tracking"
        verbose_name_plural = "Mouse Trackings"


class NasaTlx(models.Model):
    """
    Survey class gets one entry for every task in the experiment and one for the experiment as a whole
    Holds values that were given by the participant at the end of the experiment
    """
    metadata = models.ForeignKey('Metadata')
    time = models.IntegerField()

    mental = models.IntegerField(default=-1)
    physical = models.IntegerField(default=-1)
    temporal = models.IntegerField(default=-1)
    performance = models.IntegerField(default=-1)
    effort = models.IntegerField(default=-1)
    frustration = models.IntegerField(default=-1)
    fatigue = models.IntegerField(default=-1)
    boredom = models.IntegerField(default=-1)

    class Meta:
        verbose_name = ("Nasa TLX")
        verbose_name_plural = ("Nasa TLX")
