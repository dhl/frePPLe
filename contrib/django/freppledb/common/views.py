#
# Copyright (C) 2007 by Johan De Taeye
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
# General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA
#

# file : $URL$
# revision : $LastChangedRevision$  $LastChangedBy$
# date : $LastChangedDate$

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django import forms
from django.utils.translation import ugettext_lazy as _

from common.models import *
from common.report import *

from django.contrib.auth.models import User, Group


class PreferencesForm(forms.Form):
  buckets = forms.ChoiceField(label = _("Buckets"),
    initial=_('Default'),
    choices=Preferences.buckettype,
    help_text=_("Bucket size for reports"),
    )
  startdate = forms.DateField(label = _("Report start date"),
    required=False,
    help_text=_("Start date for filtering report data"),
    widget=forms.TextInput(attrs={'class':"vDateField"}),
    )
  enddate = forms.DateField(label = _("Report end date"),
    required=False,
    help_text=_("End date for filtering report data"),
    widget=forms.TextInput(attrs={'class':"vDateField"}),
    )

@login_required
def preferences(request):
  if request.method == 'POST':
    form = PreferencesForm(request.POST)
    if form.is_valid():
      try:
        pref = Preferences.objects.get(user=request.user)
        newdata = form.cleaned_data
        pref.buckets = newdata['buckets']
        pref.startdate = newdata['startdate']
        pref.enddate = newdata['enddate']
        pref.save()
        request.user.message_set.create(message='Successfully updated preferences')
      except:
        request.user.message_set.create(message='Failure updating preferences')
  else:
    pref = request.user.get_profile()
    form = PreferencesForm({
      'buckets': pref.buckets,
      'startdate': pref.startdate,
      'enddate': pref.enddate
      })
  return render_to_response('common/preferences.html', {
     'title': _('Edit my preferences'),
     'form': form,
     'reset_crumbs': True,
     },
     context_instance=RequestContext(request))


class UserList(ListReport):
  '''
  A list report to show users.
  '''
  template = 'auth/userlist.html'
  title = _("User List")
  basequeryset = User.objects.all()
  model = User
  frozenColumns = 1

  rows = (
    ('username', {
      'title': _('username'),
      'filter': FilterText(),
      }),
    ('email', {
      'title': _('E-mail'),
      'filter': FilterText(),
      }),
    ('first_name', {
      'title': _('first name'),
      'filter': FilterText(),
      }),
    ('last_name', {
      'title': _('last name'),
      'filter': FilterText(),
      }),
    ('is_staff', {
      'title': _('staff status'),
      'filter': FilterBool(),
      }),
    )


class GroupList(ListReport):
  '''
  A list report to show groups.
  '''
  template = 'auth/grouplist.html'
  title = _("Group List")
  basequeryset = Group.objects.all()
  model = Group
  frozenColumns = 0

  rows = (
    ('name', {
      'title': _('name'),
      'filter': FilterText(),
      }),
    )


class DatesList(ListReport):
  '''
  A list report to show dates.
  '''
  template = 'common/dateslist.html'
  title = _("Date List")
  basequeryset = Dates.objects.all()
  model = Dates
  frozenColumns = 1
  rows = (
    ('day', {
      'title': _('day'),
      'filter': FilterDate(),
      }),
    ('dayofweek', {
      'title': _('day of week'),
      'filter': FilterNumber(),
      }),
    ('week', {
      'title': _('week'),
      'filter': FilterText(),
      }),
    ('month', {
      'title': _('month'),
      'filter': FilterText(),
      }),
    ('quarter', {
      'title': _('quarter'),
      'filter': FilterText(),
      }),
    ('year', {
      'title': _('year'),
      'filter': FilterText(),
      }),
    ('standard', {
      'title': _('standard'),
      'filter': FilterText(),
      }),
    ('week_start', {
      'title': _('week start'),
      'filter': FilterDate(),
      }),
    ('month_start', {
      'title': _('month start'),
      'filter': FilterDate(),
      }),
    ('quarter_start', {
      'title': _('month start'),
      'filter': FilterDate(),
      }),
    ('year_start', {
      'title': _('year start'),
      'filter': FilterDate(),
      }),
    ('standard_start', {
      'title': _('standard start'),
      'filter': FilterDate(),
      }),
    )