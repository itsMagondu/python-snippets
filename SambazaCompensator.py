from noe.compensator.AbstractCompensator import *
from noe.compensator.AbstractCompensateExecute import *
from noe.gateway.sambazaGateway import SambazaGateway
from noe.survey.AbstractSurveyListener import *
from noe.engine.models import *
from noe.compensator.models import *
import os, sys
import urllib
import requests

class SambazaCompensator(AbstractSurveyListener, AbstractCompensator):
    """Implements end-of-survey compensation for Sambaza (through
    Safaricom).  It should be instantiated and then added to a survey
    object (using the survey's registerEndSurveyListener()
    method). This would likely be done when the survey is first
    instantiated."""
    
    def __init__(self, units, company):
        """units is the number of kenya shillings to compensate the
        user for each survey completed."""
        self.units   = units
        self.company = company
    
    def eventOccured(self, survey):
        """This method will be called when the survey ends. Put the
        code to queue a row on the compensate queue."""

        userRow   = survey.getEngineService().getRespondent()
        surveyRow = survey.getEngineService().getActiveSurvey()

        executeObject = SambazaCompensateExecute(commID = userRow.commID,
                                                 units  = self.units)
                                                 
        c = CompensateQueue(commID         = userRow.commID,
                            commDomain     = userRow.commDomain,
                            finishedSurvey = surveyRow.id,
                            surveyFactory  = surveyRow.surveyFactory,
                            processed      = False,
                            executeObject  = executeObject)
        c.save()
        
        self.compensate()


class SambazaCompensateExecute(AbstractCompensateExecute):
    """FIXME: fill in docstring"""

    def __init__(self, commID, units):
        self.commID        = commID
        self.units         = units
    
    def execute(self):
        #msg = str(self.units) + '#' + '0' + str(self.commID).strip('+')[3:]
       # 
        #gw = SambazaGateway()
        #gw.send(msg

        params = urllib.urlencode({'rec': self.commID, 'amount': self.units,'key':'543212345','domain':'safaricom'})
        x = r.post('http://75.101.179.171/comp/compensate/put/',data = payload)
        
        print x
        t = open("/tmp/Output.html", "w")
        
        t.write(x.text)
        
        t.close
