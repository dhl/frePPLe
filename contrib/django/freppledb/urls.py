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
# email : jdetaeye@users.sourceforge.net

from django.conf.urls.defaults import *
import sys, os.path
import freppledb.output.views
import freppledb.user.views
from django.conf import settings

urlpatterns = patterns('',

    # Frepple execution
    (r'^execute/log/$', 'django.views.generic.simple.direct_to_template',
       {'template': 'execute/log.html',
        'extra_context': {'title': 'Frepple log file'},
       }),
    (r'^execute/runfrepple/$', 'freppledb.execute.views.runfrepple'),
    (r'^execute/rundb/$', 'freppledb.execute.views.rundb'),
    (r'^execute/upload/$', 'freppledb.execute.views.upload'),
    (r'^execute/', 'django.views.generic.simple.direct_to_template',
       {'template': 'execute/execute.html',
        'extra_context': {'title': 'Execute'},
       }),

    # Main index page
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/admin/'}),

    # Admin pages
    (r'^admin/', include('django.contrib.admin.urls')),

    # Frepple reports
    (r'^buffer/([^/]+)/$', freppledb.output.views.bufferreport),
    (r'^buffer/$', freppledb.output.views.bufferreport),
    (r'^demand/([^/]+)/$', freppledb.output.views.demandreport),
    (r'^demand/$', freppledb.output.views.demandreport),
    (r'^resource/([^/]+)/$', freppledb.output.views.resourcereport),
    (r'^resource/$', freppledb.output.views.resourcereport),
    (r'^operation/([^/]+)/$', freppledb.output.views.operationreport),
    (r'^operation/$', freppledb.output.views.operationreport),
    (r'^path/([^/]+)/([^/]+)/$', freppledb.output.views.pathreport.view),

    # User preferences
    (r'preferences/$', freppledb.user.views.preferences),
)

# Allows the standalone development server to serve the static pages.
# In a production environment you need to configure your web server to take care of
# these pages.
if 'runserver' in sys.argv:
  urlpatterns += patterns('',(r'static/(?P<path>.*)$', 'django.views.static.serve',
       {'document_root': os.path.join(settings.FREPPLE_APP,'freppledb','static'), 'show_indexes': False}),
    )
