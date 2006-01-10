# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005 Vasco Nunes
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# You may use and distribute this software under the terms of the
# GNU General Public License, version 2 or later

from gettext import gettext as _
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import mm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.rl_config import defaultPageSize
from reportlab.platypus import Image, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from xml.sax import saxutils
import os, gtk
import version
import gutils
import string
import sys

if self.config.get('font', '')!='':
	fontName = self.config.get('font', '')
	#pdfmetrics.registerFont(TTFont(fontName, font))
else:
	fontName = "Helvetica"

exec_location = os.path.abspath(os.path.dirname(sys.argv[0]))

plugin_name = "PDF"
plugin_description = _("PDF export plugin")
plugin_author = "Vasco Nunes"
plugin_author_email = "<vasco.m.nunes@gmail.com>"
plugin_version = "0.1"

class ExportPlugin:
    def __init__(self, database, locations, parent):
        self.db = database
        self.locations = locations
        self.parent = parent
        self.styles = getSampleStyleSheet()
        self.export_simple_pdf()

    def export_simple_pdf(self):
        """exports a simple movie list to a pdf file"""

        filename = gutils.file_chooser(_("Export a PDF"), action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK),name="griffith_simple_list.pdf")
        if filename[0]:
            overwrite = None
            if os.path.isfile(filename[0]):
                response = gutils.question(self,_("File exists. Do you want to overwrite it?"),1,self.parent)
                if response==-8:
                    overwrite = True
                else:
                    overwrite = False
                    
            if overwrite == True or overwrite == None:        
                c = SimpleDocTemplate(filename[0])    
                style = self.styles["Normal"]        
                Story = [Spacer(1,2*inch)]
                # define some custom stylesheet
                total = self.db.count_records('movies')
                p = Paragraph("<font name='" + fontName +"' size=\"18\">" + saxutils.escape((_("List of films")).encode('utf-8')) + '</font>', self.styles["Heading1"] )
                Story.append(p)
                Story.append(Paragraph(" ",style))
                p = Paragraph("<font name='" + fontName +"' size=\"10\">" + saxutils.escape((_("Total Movies: %s") % str(total)).encode('utf-8'))  + '</font>', self.styles["Heading3"])
                Story.append(p)
                Story.append(Paragraph(" ",style))
                data = self.db.get_all_data()
                for row in data:
                    number = str(row['number'])
		    number = number.encode('utf-8')
                    original_title = str(row['original_title'])
                    original_title = original_title.encode('utf-8')
                    title = str(row['title'])
                    title = title.encode('utf-8')
                    if row['year']:
                        year = ' - ' + str(row['year'])
                    else:
                        year = ""
		    year = year.encode('utf-8')
                    if row['director']:
                        director = ' - ' + str(row['director'])
                    else:
                        director = ""
                    director = director.encode('utf-8')
                    p = Paragraph("<font name=" + fontName + " size=\"7\">" + \
                        saxutils.escape(number + " | " + original_title) + \
                        "</font><font name=" + fontName + " size=\"7\">" + \
                        saxutils.escape(" (" + title + ")" + year + director) + \
                        "</font>", self.styles["Normal"])
                    Story.append(p)
                c.build(Story, onFirstPage=self.page_template, onLaterPages=self.page_template)
                gutils.info(self, _("PDF has been created."), self.parent)
            
    def page_template(self, canvas, doc):
        canvas.saveState()
        canvas.setFont(fontName,7)
        canvas.drawCentredString(defaultPageSize[0]/2, 40,_("Page %d") % doc.page)
        canvas.setFont(fontName,5)
        canvas.drawCentredString(defaultPageSize[0]/2, 20, (_("Document generated by Griffith v")+
            version.pversion+" - Copyright (C) "+version.pyear+" "+
            version.pauthor+" - " + _("Released Under the GNU/GPL License")).encode('utf-8'))                
        canvas.restoreState()
