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

#  file     : $URL$
#  revision : $LastChangedRevision$  $LastChangedBy$
#  date     : $LastChangedDate$
#  email    : jdetaeye@users.sourceforge.net

import os
from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _
from django.db import transaction
from django.conf import settings

from execute.models import log


class Command(BaseCommand):
  option_list = BaseCommand.option_list + (
    make_option('--verbosity', dest='verbosity',
        type='choice', choices=['0','1','2','3','4','5','6','7'], default='7',
        help='Verbosity level; 0=minimal output, 1=normal output, 2=all output'),
    make_option('--user', dest='user', default='',
        type='string', help='User running the command'),
    make_option('--type', dest='type', type='choice',
        choices=[0,1,2,3,4,5,6,7], default=7,
        help='Plan type; 0=minimal output, 1=normal output, 2=all output'),
  )
  help = "Runs frePPLe to generate a plan"

  requires_model_validation = False

  @transaction.autocommit
  def handle(self, **options):
    try:
      log(category='RUN', user=options['user'],
        message=_('Start running frepple with plan type ') + str(options['type'])).save()
      os.environ['PLAN_TYPE'] = str(options['type'])
      os.environ['FREPPLE_HOME'] = settings.FREPPLE_HOME.replace('\\','\\\\')
      os.environ['FREPPLE_APP'] = settings.FREPPLE_APP
      os.environ['PATH'] = settings.FREPPLE_HOME + os.pathsep + os.environ['PATH'] + os.pathsep + settings.FREPPLE_APP
      os.environ['LD_LIBRARY_PATH'] = settings.FREPPLE_HOME
      os.environ['DJANGO_SETTINGS_MODULE'] = 'freppledb.settings'
      if os.path.exists(os.path.join(os.environ['FREPPLE_APP'],'library.zip')):
        # For the py2exe executable
        os.environ['PYTHONPATH'] = os.path.join(os.environ['FREPPLE_APP'],'library.zip')
      else:
        # Other executables
        os.environ['PYTHONPATH'] = os.path.normpath(os.path.join(os.environ['FREPPLE_APP'],'..'))
      ret = os.system('frepple "%s"' % os.path.join(settings.FREPPLE_APP,'execute','commands.xml'))
      if ret: raise Exception('exit code of the batch run is %d' % ret)
      log(category='RUN', user=options['user'],
        message=_('Finished running frepple')).save()
    except Exception, e:
      log(category='RUN', message=u'%s: %s' % (_('Failure when running frepple'),e)).save()
      raise e