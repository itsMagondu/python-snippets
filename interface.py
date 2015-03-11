from django.template import Context, loader
from django.shortcuts import *
from django.contrib import admin
from django.http import *
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import connection, transaction
from decimal import Decimal
import urllib
import datetime
import json
import smtplib
import noe.settings

from noe.surveyAdmin import models
from noe.contactList.models import Feature
from noe.panel.models import Feature as f
from noe.engine import models as emodels
from noe.survey2.survey import *
from noe.survey2.dhtmlxtreeParse import *


from noe.surveyAdmin.contactform import *
from noe.surveyAdmin.signupform import *
from noe.compensator.SambazaCompensator import SambazaCompensator

from xml.etree import ElementTree as ET

TWOPLACES = Decimal(10) ** -2 

def customers(request):
    args = {}
    args['base_url'] = settings.BASE_URL
    return render_to_response("partners.html",args)
  

def demo_page(request):
    args = {}
    args['base_url'] = settings.BASE_URL
    return render_to_response("partners.html",args)  

def map_demo(request):
    args = {}
    args['base_url'] = settings.BASE_URL
    return render_to_response("demo.html",args) 
                                                          
def signin(request):
    args = {}
    args['base_url'] = settings.BASE_URL
    return render_to_response("signin.html",args)    
                                                                
@login_required
def signup_home(request):
    args = {}
    args['username'] = request.user.username
    args['base_url'] = settings.BASE_URL
    return render_to_response('signup/signup.html',args)

@login_required
def search(request):
    args = {}
    args['username'] = request.user.username
    args['base_url'] = settings.BASE_URL
    args['users'] = User.objects.all()
    return render_to_response('signup/search.html',args)


#DIRECT TO REGISTRATION PAGE                                                                            
def register(request):
    args = {}
    args['base_url'] = settings.BASE_URL
    data = {'email' : request.POST.get('email','') }
    args['form'] = SignupForm(initial = data)                                                                                           
    return render_to_response('signup_request.html', args)

#DIRECT TO RESET PASSWORD PAGE                                                                                                                
def resetPassword(request):
    args = {}
    args['base_url'] = settings.BASE_URL
    html = "<div>"
    html = html + "THIS IS THE REGISTRAION PAGE"
    html = html + "</div>"
   # return HttpResponse(html)                                                                                                         
   # args['countries'] = countries                                                                                     
    return render_to_response('password.html', args)

#DIRECT TO RESET PASSWORD PAGE                                                                                                                
def createPassword(request):
    args = {}
    args['base_url'] = settings.BASE_URL
    html = "<div>"
    html = html + "THIS IS THE REGISTRAION PAGE"
    html = html + "</div>"
   # return HttpResponse(html)                                                                                                         
   # args['countries'] = countries                                                                                     
    return render_to_response('password_create.html', args)

@login_required
def index(request):
    args = {}
    args['sf_list'] = models.SurveyFactory.objects.filter(current=True, creator=request.user).order_by('title')
    args['username'] = request.user.username
    args['base_url'] = settings.BASE_URL
    balance = models.UserProfile.objects.get(user = request.user.id)
    args['balance'] = balance.messageCredits
    return render_to_response('index.html',args)

@login_required
def home(request):
    args = {}
    args['base_url'] = settings.BASE_URL
    if canUsePrescreenFeature(request.user):
        args['canUsePrescreenFeature'] = 'true'
    else:
        args['canUsePrescreenFeature'] = 'false'
    if canUseSurveyCircles(request.user):
        args['canUseSurveyCircles'] = True
    else:
        args['canUseSurveyCircles'] = False
    if canCompensate(request.user):
        args['cancompensate'] = "true"
    else:
        args['cancompensate'] =  "false"
    return render_to_response("Editor.html", args)

def canUsePrescreenFeature(user_id):
	a = Feature.objects.filter(user = user_id, prescreen = True).count()
	if a > 0:
		return True
	else:
		return False
		
def canUseSurveyCircles(user_id):
	a = f.objects.filter(user = user_id, circle = True).count()
	if a > 0:
		return True
	else:
		return False
		
def canCompensate(user_id):
	print "user _id " + str(user_id)
	try:
		return User.objects.get(username = user_id).is_superuser
	except:
		return False

@login_required
def faq(request):
    args = {}
    args['base_url'] = settings.BASE_URL
    return render_to_response("faq.html",args)


@login_required
def nonsupport(request):
    args = {}
    args['base_url'] = settings.BASE_URL
    return render_to_response("NonSupport.html",args)


#DIRECT TO PRIVACY PAGE                                                                                                                         
#Customer privacy essentials                                                                                                                  
def privacy(request):
    args = {}
    args['base_url'] = settings.BASE_URL
    html = "<div>"
    html = html + "THIS IS THE REGISTRAION PAGE"
    html = html + "</div>"
   # return HttpResponse(html)                                                                                                             
    return render_to_response('mSurveyPrivacy.html', args)

#DIRECT TO PRICING PAGE                                                                                                                               
def pricing(request):
    args = {}
    args['base_url'] = settings.BASE_URL
    html = "<div>"
    html = html + "THIS IS THE REGISTRAION PAGE"
    html = html + "</div>"

    #args['countries'] = countries
    return render_to_response('pricing.html', args)

#DIRECT TO TERMS PAGE                                                                                                                      
#terms of use                                                                                                                                
def terms(request):
    args = {}
    args['base_url'] = settings.BASE_URL
    html = "<div>"
    html = html + "THIS IS THE REGISTRAION PAGE"
    html = html + "</div>"
   # return HttpResponse(html)                                                                                                                   
    return render_to_response('terms.html', args)


@login_required
def editPage(request, sfid):
    args = {}
    args['sf_list'] = models.SurveyFactory.objects.filter(current=True, creator=request.user).order_by('title')
    sf = models.SurveyFactory.objects.get(id=sfid, creator=request.user, current=True)
    args['title'] = sf.title
    args['desc'] = sf.description
    args['mutable'] = sf.mutable

    args['username'] = request.user.username
    args['media_url'] = settings.MEDIA_URL
    args['base_url'] = settings.BASE_URL
    balance = models.UserProfile.objects.get(user = request.user.id)
    args['balance'] = balance.messageCredits

    args['sfid'] = sfid
    return HttpResponse(args)

@login_required
def dhtmlxtreeXML(request, sfid):
    rows = models.SurveyFactory.objects.filter(creator = request.user, id = sfid, current=True)
    if(len(rows) > 0):
        row = rows[0]
        xml = surveyToXML(row.surveyObj, row.title)
        return HttpResponse(xml, mimetype='text/xml')
    else:
        return HttpResponse("NO survey object found")

def saveSurvey(request, sfid):
    # At this point, survey table row should already exist

    if not (request.method == "POST"):                                                                                                                
        return HttpResponseServerError("No POST data sent to add to survey")         

    rows = models.SurveyFactory.objects.filter(creator = request.user, id = sfid, current=True)
    if(len(rows) > 0):
        row = rows[0]

        if(row.mutable == False):
            return HttpResponse("Survey not saved. Survey questions cannot be edited.")

        obj = buildTreeSurvey(request.raw_post_data)
        for endSurveyListener in row.surveyObj.endSurveyListeners:
            obj.registerEndSurveyListener(endSurveyListener)
        row.surveyObj = obj
        row.save()
        return HttpResponse("Success")
    else:
        return HttpResponse("No rows")

@login_required
def viewAccount(request):
    """This part displays all the data associated with a particluar user. This includes The account number, The balance on credits, all survyes created by this user and the username. I will need to optimize this code abit though on the database queries"""

    items = ET.Element("item")
    node = ET.Element("account")
    
    node.attrib["username"] = str(request.user.username)

    surveys = models.SurveyFactory.objects.filter(current=True, creator=request.user).values('id','title','mutable') 
    
    balance = models.UserProfile.objects.get(user = request.user.id)
    node.attrib['balance'] = str(balance.messageCredits)
    node.attrib['amount_ksh'] = str((balance.messageCredits * 7) + balance.balance)
    node.attrib['amount_dollar'] = str((balance.messageCredits * 0.07) + (balance.balance)/85.00)
    node.attrib['moneybalance'] = str(Decimal(Decimal(balance.moneyBalance) / 100).quantize(TWOPLACES))
    
    if ((Decimal(balance.moneyBalance) / 100) == 0):
        node.attrib['moneybalance'] = str(Decimal((balance.messageCredits * 0.07) + (balance.balance)/settings.EXCHANGE_RATE_KSH_DOLLAR)).quantize(TWOPLACES)
    
    node.attrib['account_no'] = str(balance.account)
    
    activeP = 0
    finishedP = 0
    total = 0

    for item in surveys:
        #Make each survey a node
        survey = ET.Element("survey")
    
        item["title"] = item["title"].encode()
        item["id"] =int(item["id"])
        item["editable"] = str(item["mutable"])
       
        survey.attrib["id"] = str(item["id"])
        survey.attrib["title"]= item["title"]
        survey.attrib["editable"]= item["editable"]
       
        sfid = str(item["id"])
        title_ = item["title"]
        
        surveyItems = models.SurveyFactory.objects.filter(id = sfid)
        
        activeP = emodels.ActiveSurvey.objects.filter(surveyFactory= surveyItems).count()
        finishedP = emodels.FinishedSurvey.objects.filter(surveyFactory=surveyItems).count()
        total = int(activeP)+int(finishedP)
        
        survey.attrib["active"] = str(activeP)
        survey.attrib["finished"] = str(finishedP)
        survey.attrib["total"] = str(total)      

        items.append(survey)
    
    node.append(items)
    args_xml = ET.tostring(node)
    
    return HttpResponse(args_xml,mimetype='text/xml')

@login_required
def delete(request,sfid):

    sfs = models.SurveyFactory.objects.filter(id=sfid, creator=request.user, current=True)
    if(len(sfs) > 0):
        sf = sfs[0]
        sf.current = False
        sf.active = False
        sf.joincode = ""
        sf.save()
        return HttpResponse("Delete Successful")
    else:
        return HttpResponse("Delete Failed")

@login_required
def duplicate(request,sfid):

    sfs = models.SurveyFactory.objects.filter(id=sfid, creator=request.user, current=True)
    if(len(sfs) > 0):
        sf = sfs[0]

        sf.id = None #will force Django to save as new row in table
        sf.title = sf.title + " copy"
        sf.created = datetime.datetime.now()
        sf.joincode = ""
        sf.active = False
        sf.mutable = True
        sf.save()
        
        return HttpResponse(str(sf.id))
    else:
        return HttpResponse("Duplicating failed")

def submitCreate(request):

    if not (request.method == "POST"):
        return HttpResponseServerError("No POST data sent.")

    xml = request.raw_post_data  
    print xml
    mylogfile = '/tmp/diy.log'
    f = open(mylogfile, 'a')
    f.write('DIY:'+str(xml)+ '\n')
    f.close()

    metadata = ET.XML(xml)
    
    sf_title = None
    sf_description = None
    sf_country = None
    max_resp = None
    can_retake = None
    join = None
    compensation = None

    for i in metadata:
        text = i.text
#        text = text.encode()
        text = removeNonAscii(text)

        if (i.tag == 'title'):
            sf_title = text
        elif (i.tag == 'description'):
            sf_description = text
        elif (i.tag == 'joincode'):
            join = text
        elif (i.tag == 'country'):
            sf_country = text
        elif (i.tag == 'max_respondents'):
            max_resp = text
        elif (i.tag == 'retake_survey'):
            can_retake = text
        elif (i.tag == 'compensation'):
            compensation = text
            
    c = None
    if (compensation != '0') or (compensation != None) :
        if (sf_country.lower() == "kenya"):
            c = SambazaCompensator(int(compensation),sf_title)
        
    if (join == "") or (sf_title == ""):
        return HttpResponseServerError(join+" "+ sf_title+""+"Must have joincode and title.")
  
    retake = False
    if(can_retake.lower() == 'yes'):
        retake = True;
                                                           
    #Compensation. Will not be active for the DIY                                                    
        

    if (max_resp == ""):
        return HttpResponseServerError("Number of respondents required.")
    else:
        try:
            max_respondents = int(max_resp)
        except:
            return HttpResponseServerError("Max respondents must be a number.")
      
    so = TreeSurvey()
    
    if c:
        so.registerEndSurveyListener(c)        

    new_sf = models.SurveyFactory(surveyObj=so, \
                                  joincode=join, \
                                  title=sf_title, \
                                  description=sf_description, \
                                  surveyCountry=sf_country,\
                                  current=True,\
                                  maxRespondents=max_respondents,\
                                  mutable=True,\
                                  reentrant = retake)
    
    if str(request.user) == "AnonymousUser":
        return HttpResponseServerError("You are logged out. Please refresh this page.")
        #return HttpResponseRedirect('/home/')
    new_sf.creator = request.user
    
    success = uniqueJoincodeSave(new_sf)

    if(not success):
        return HttpResponseServerError("Joincode already in use. Please choose a different one.")
    else:
        return HttpResponse(str(new_sf.id), mimetype='text/plain')


@login_required
def view(request,sfid):
    items = ET.Element("item")
    node = ET.Element("survey")
    #items.attrib['sf_list'] = str(models.SurveyFactory.objects.filter(current=True, creator=request.user).order_by('title'))
    node.attrib['username'] = str(request.user.username)
    
    if (sfid != ''):
        # If the SurveyFactory doesn't exist, doesn't belong to
        # the current user, or is not the current version,
        # redirect to the main page
        try:
            sf = models.SurveyFactory.objects.get(id=sfid, creator=request.user, current=True)
        except models.SurveyFactory.DoesNotExist:
            return HttpResponse("No Survey Found")

	balance = models.UserProfile.objects.get(user = request.user)

        # Pass arguments to template for display
        items.attrib['sf_id'] =str(sfid)
        items.attrib['title'] = str(sf.title)
        items.attrib['description'] = str(sf.description)
        items.attrib['country'] = str(sf.surveyCountry)
        items.attrib['joincode'] = str(sf.joincode)
        items.attrib['surveyObj'] = str(sf.surveyObj)
        items.attrib['created'] = str(sf.created)
        items.attrib['active'] = str(sf.active)
        items.attrib['limit'] = str(sf.maxRespondents)
        items.attrib['active_surveys'] = str(emodels.ActiveSurvey.objects.filter(surveyFactory = sf).count())
        items.attrib['finished'] = str(emodels.FinishedSurvey.objects.filter(surveyFactory = sf).count())
        items.attrib['retake'] = str(sf.reentrant)
        items.attrib['activate_link'] = str(getActivateLink(request.user,sf))
 	items.attrib['balance'] = str(balance.messageCredits)
        items.attrib['mutable'] = str(sf.mutable)
        
        node.append(items)

        args_xml = ET.tostring(node)
        #args_xml = DictToXML(args)

    return HttpResponse(args_xml,mimetype='text/xml')

@login_required
def saveSurveyDetails(request, sfid):
    try:
        sf = models.SurveyFactory.objects.get(id=sfid, creator=request.user, current=True)
    except models.SurveyFactory.DoesNotExist:
        return HttpResponseRedirect(settings.BASE_URL)
    
    if not (request.method == "POST"):
        return HttpResponseServerError("No POST data sent.")

    post = request.raw_post_data

    metadata = ET.XML(post)
    
    title = None
    desc = None
    limit = None
    country = None
    retake = None
    joincode = None
    
    for i in metadata:
        print "in metadata"
        text = i.text
        print  "before: "+text
        text = removeNonAscii(text)
        print "After: "+text

        if (i.tag == 'title'):
            title = text
        elif (i.tag == 'description'):
            desc = text
        elif (i.tag == 'joincode'):
            joincode = text
        elif (i.tag == 'country'):
            country = text
        elif (i.tag == 'max_respondents'):
            limit = text
        elif (i.tag == 'retake_survey'):
            retake = text
    
    if(retake == 'No'):
        retake = False
    else:
        retake = True

    jcchanged = False
    if(joincode != sf.joincode):
        jcchanged = True
        sf.joincode = joincode

    sf.title = title
    sf.description = desc
    sf.reentrant = retake
    sf.maxRespondents = limit
    sf.surveyCountry = country

    if(jcchanged == True and joincode != ""):
        success = uniqueJoincodeSave(sf)
        if(not success):
            return HttpResponseServerError("Joincode already in use. Please choose a different one.")
        else:
            return HttpResponse("Success")
    else:
        sf.save()
        return HttpResponse("Success")


def saveSurvey(request, sfid):
    # At this point, survey table row should already exist. Call this method after you create a survey object

    if not (request.method == "POST"):                                                                                                                
        return HttpResponseServerError("No POST data sent to add to survey")         

    rows = models.SurveyFactory.objects.filter(creator = request.user, id = sfid, current=True)
    if(len(rows) > 0):
        row = rows[0]

        if(row.mutable == False):
            return HttpResponse("Survey not saved. Survey questions cannot be edited.")

        obj = buildTreeSurvey(request.raw_post_data)
        for endSurveyListener in row.surveyObj.endSurveyListeners:
            obj.registerEndSurveyListener(endSurveyListener)
        row.surveyObj = obj
        row.save()
        return HttpResponse("Success")
    else:
        return HttpResponse("No rows")

      
@login_required
def activate(request,sfid,activate):

    sf = models.SurveyFactory.objects.get(id=sfid, creator=request.user, current=True)

    # Only an admin can activate
    #if not request.user.is_staff:
    #    return HttpResponseServerError("Only an admin can activate.")

    if activate == '1':
        if len(sf.surveyObj.getAllQuestions()) == 0:
            return HttpResponseServerError("Your survey has no questions. Please add a question.")
        if(sf.joincode == ""):
            return HttpResponseServerError("Cannot activate a survey with an empty joincode. Please change the joincode.")
        sf.active = True

        if(sf.mutable == True):
            # This is first time survey has been activated
            sf.mutable = False
            factoryObj = sf.surveyObj
            factoryObj.numberQuestions()

            questions = factoryObj.getAllQuestions()
            for q in questions:
                id = q.getQid()

                qRow = emodels.DataQuestion(surveyFactory = sf, surveyQuestionID = id, text = q.getQuestionText(), numAnswers = q.countAnswers())
                qRow.save()

                ans = q.getAnswers()
                for a in ans:
                    Arow = emodels.DataPossibleResponse(question = qRow, text = a)
                    Arow.save()

                
    else:
        sf.active = False
    sf.save()
    return HttpResponse("Success")


def getActivateLink(user, sf):
    #FIXME: should use a custom field not staff status to determine this
    if user.is_staff:
        return "<a href='"+settings.BASE_URL+"activate/" + str(sf.id) + "/1'>Activate</a>"
    # if user is not staff, request activation through email
    subject = "Survey Activation Request"
    to = "team@m-survey.org"
    body = "User " + user.username + " requests activation for survey " + str(sf) + "."
    mailto = "mailto:"+to+"?Subject="+subject+"&Body="+body
    urllib.quote(mailto)
    return "<a href='" + mailto + "'>Request Activation</a>"


def getPreviewHTML(so,active):
    html = "<div>"
    # Intro Message
    if (so.introMessage):
        html = html + "<div id='welcome'>"
        html = html + so.introMessage + "</div><br/><br/>"
    
    # Questions
    html = html +  questionListHTML(so.questions,[],active) + "<div></div><br>"
    
    # End Message
    if (so.endMessage):
        html = html + "<br/><div id='thank_you'>"
        html = html + so.endMessage + "</div>"
    html = html + "</div><br/><br/>"
    return html

def questionListHTML(qlist, indexList, active):
    html = "<ul>"
    n = 0
    for qind in range(len(qlist)):
        n = n + 1
	q = qlist[qind]
        """INCLUDE QUESTION NUMBER IN HTML"""
	html = html + "<li>"
	html = html + q.question
        if (q.allThatApply):
            html = html + " (All that apply)"
        if (not active):
            html = html + " <input type='image' src='../../media/images/delete-button.png' alt='delete question' onclick=\"removeQuestion('"
            html = html + ",".join(indexList+[str(qind)])
            html = html + "')\">"
            #html = html + "<button onclick=\"removeQuestion('"
            #html = html + ",".join(indexList+[str(qind)])
            #html = html + "')\">Remove Question</button>"

        html = html + "<ol>"
        for aind in range(len(q.answers)):
            html = html + "<li>"
            html = html + q.answers[aind]
            if (not q.allThatApply):
                html = html + questionListHTML(q.question_lists[aind],indexList+[str(qind),str(aind)],active)
            html = html + "</li>"
        html = html + "</ol>"
        html = html + "</li>"

    html = html + "</ul>"
    if (not active):
	#reduce button size if questions are in tree
	if (len(indexList)==0):	
        	html = html + "<input type='image' src='../../media/images/add_button.png' alt='add question' onclick=\"addQuestion('"
        	html = html + ",".join(indexList)
        	html = html + "')\"></br>"
	else:
        	html = html + "<input type='image' src='../../media/images/add_button_small.png' alt='add question' onclick=\"addQuestion('"
        	html = html + ",".join(indexList)
        	html = html + "')\"></br>"
    return html


@login_required
def getCSV(request, sf_id):
    # Get SurveyFactory with id from URL
    try:
        sf = models.SurveyFactory.objects.get(id=sf_id, creator=request.user, current=True)
    except:
        return HttpResponseServerError(sf_id + " is an invalid survey id.")

    dataQuestions = emodels.DataQuestion.objects.filter(surveyFactory=sf)

    # Header row
    csv = '"user id","timestamp (UTC)","question","answer"\n'

    for q in dataQuestions:
        responses = emodels.DataResponse.objects.filter(question = q)
        for r in responses:
            csv = csv + '"' + str(r.respondent.id) + '","' + str(r.timestamp) + '","' + str(q.text) + '","' + str(r.text) + '"\n'
    return HttpResponse(csv, mimetype='text/csv')


def uniqueJoincodeSave(row):
    """saves a surveyFactory only if its joincode is unique and returns true, Otherwise
   returns false."""
    
    cursor = connection.cursor()
    cursor.execute("LOCK TABLES surveyAdmin_surveyfactory WRITE,engine_reservedjoincode WRITE")
    
    success = False
    try:
        n = models.SurveyFactory.objects.filter(current = True, joincode = row.joincode).count()
        r = emodels.ReservedJoincode.objects.filter(active = True, text = row.joincode).count()

        if(n == 0 and r == 0):
            row.save()
            transaction.commit_unless_managed()
            success = True
    finally:
        cursor.execute("unlock tables")

    return success

# """THis will strip out all non assci characters"""
def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)
    
def DictToXML(args):
    i_root =  ET.Element('survey')
    for (field, val) in args.iteritems():
        ET.SubElement(i_root, field).text = val
    i_root = ET.tostring(i_root)
    return i_root     
    

def getCountries():
    return [{'code': "AF", 'name': "Afghanistan"},{'code': "AX", 'name': "Aland Islands"},{'code': "AL", 'name': "Albania"},{'code': "DZ", 'name': "Algeria"},{'code': "AS", 'name': "American Samoa"},{'code': "AD", 'name': "Andorra"},{'code': "AO", 'name': "Angola"},{'code': "AI", 'name': "Anguilla"},{'code': "AQ", 'name': "Antarctica"},{'code': "AG", 'name': "Antigua and Barbuda"},{'code': "AR", 'name': "Argentina"},{'code': "AM", 'name': "Armenia"},{'code': "AW", 'name': "Aruba"},{'code': "AU", 'name': "Australia"},{'code': "AT", 'name': "Austria"},{'code': "AZ", 'name': "Azerbaijan"},{'code': "BS", 'name': "Bahamas"},{'code': "BH", 'name': "Bahrain"},{'code': "BD", 'name': "Bangladesh"},{'code': "BB", 'name': "Barbados"},{'code': "BY", 'name': "Belarus"},{'code': "BE", 'name': "Belgium"},{'code': "BZ", 'name': "Belize"},{'code': "BJ", 'name': "Benin"},{'code': "BM", 'name': "Bermuda"},{'code': "BT", 'name': "Bhutan"},{'code': "BO", 'name': "Bolivia, Plurinational State of"},{'code': "BQ", 'name': "Bonaire, Saint Eustatius and Saba"},{'code': "BA", 'name': "Bosnia and Herzegovina"},{'code': "BW", 'name': "Botswana"},{'code': "BV", 'name': "Bouvet Island"},{'code': "BR", 'name': "Brazil"},{'code': "IO", 'name': "British Indian Ocean Territory"},{'code': "BN", 'name': "Brunei Darussalam"},{'code': "BG", 'name': "Bulgaria"},{'code': "BF", 'name': "Burkina Faso"},{'code': "BI", 'name': "Burundi"},{'code': "KH", 'name': "Cambodia"},{'code': "CM", 'name': "Cameroon"},{'code': "CA", 'name': "Canada"},{'code': "CV", 'name': "Cape Verde"},{'code': "KY", 'name': "Cayman Islands"},{'code': "CF", 'name': "Central African Republic"},{'code': "TD", 'name': "Chad"},{'code': "CL", 'name': "Chile"},{'code': "CN", 'name': "China"},{'code': "CX", 'name': "Christmas Island"},{'code': "CC", 'name': "Cocos (Keeling) Islands"},{'code': "CO", 'name': "Colombia"},{'code': "KM", 'name': "Comoros"},{'code': "CG", 'name': "Congo"},{'code': "CD", 'name': "Congo, The Democratic Republic of the"},{'code': "CK", 'name': "Cook Islands"},{'code': "CR", 'name': "Costa Rica"},{'code': "CI", 'name': "Cote D'ivoire"},{'code': "HR", 'name': "Croatia"},{'code': "CU", 'name': "Cuba"},{'code': "CW", 'name': "Curacao"},{'code': "CY", 'name': "Cyprus"},{'code': "CZ", 'name': "Czech Republic"},{'code': "DK", 'name': "Denmark"},{'code': "DJ", 'name': "Djibouti"},{'code': "DM", 'name': "Dominica"},{'code': "DO", 'name': "Dominican Republic"},{'code': "EC", 'name': "Ecuador"},{'code': "EG", 'name': "Egypt"},{'code': "SV", 'name': "El Salvador"},{'code': "GQ", 'name': "Equatorial Guinea"},{'code': "ER", 'name': "Eritrea"},{'code': "EE", 'name': "Estonia"},{'code': "ET", 'name': "Ethiopia"},{'code': "FK", 'name': "Falkland Islands (Malvinas)"},{'code': "FO", 'name': "Faroe Islands"},{'code': "FJ", 'name': "Fiji"},{'code': "FI", 'name': "Finland"},{'code': "FR", 'name': "France"},{'code': "GF", 'name': "French Guiana"},{'code': "PF", 'name': "French Polynesia"},{'code': "TF", 'name': "French Southern Territories"},{'code': "GA", 'name': "Gabon"},{'code': "GM", 'name': "Gambia"},{'code': "GE", 'name': "Georgia"},{'code': "DE", 'name': "Germany"},{'code': "GH", 'name': "Ghana"},{'code': "GI", 'name': "Gibraltar"},{'code': "GR", 'name': "Greece"},{'code': "GL", 'name': "Greenland"},{'code': "GD", 'name': "Grenada"},{'code': "GP", 'name': "Guadeloupe"},{'code': "GU", 'name': "Guam"},{'code': "GT", 'name': "Guatemala"},{'code': "GG", 'name': "Guernsey"},{'code': "GN", 'name': "Guinea"},{'code': "GW", 'name': "Guinea-Bissau"},{'code': "GY", 'name': "Guyana"},{'code': "HT", 'name': "Haiti"},{'code': "HM", 'name': "Heard Island and McDonald Islands"},{'code': "VA", 'name': "Holy See (Vatican City State)"},{'code': "HN", 'name': "Honduras"},{'code': "HK", 'name': "Hong Kong"},{'code': "HU", 'name': "Hungary"},{'code': "IS", 'name': "Iceland"},{'code': "IN", 'name': "India"},{'code': "ID", 'name': "Indonesia"},{'code': "IR", 'name': "Iran, Islamic Republic of"},{'code': "IQ", 'name': "Iraq"},{'code': "IE", 'name': "Ireland"},{'code': "IM", 'name': "Isle of Man"},{'code': "IL", 'name': "Israel"},{'code': "IT", 'name': "Italy"},{'code': "JM", 'name': "Jamaica"},{'code': "JP", 'name': "Japan"},{'code': "JE", 'name': "Jersey"},{'code': "JO", 'name': "Jordan"},{'code': "KZ", 'name': "Kazakhstan"},{'code': "KE", 'name': "Kenya"},{'code': "KI", 'name': "Kiribati"},{'code': "KP", 'name': "Korea, Democratic People's Republic of"},{'code': "KR", 'name': "Korea, Republic of"},{'code': "KW", 'name': "Kuwait"},{'code': "KG", 'name': "Kyrgyzstan"},{'code': "LA", 'name': "Lao People's Democratic Republic"},{'code': "LV", 'name': "Latvia"},{'code': "LB", 'name': "Lebanon"},{'code': "LS", 'name': "Lesotho"},{'code': "LR", 'name': "Liberia"},{'code': "LY", 'name': "Libyan Arab Jamahiriya"},{'code': "LI", 'name': "Liechtenstein"},{'code': "LT", 'name': "Lithuania"},{'code': "LU", 'name': "Luxembourg"},{'code': "MO", 'name': "Macao"},{'code': "MK", 'name': "Macedonia, The Former Yugoslav Republic of"},{'code': "MG", 'name': "Madagascar"},{'code': "MW", 'name': "Malawi"},{'code': "MY", 'name': "Malaysia"},{'code': "MV", 'name': "Maldives"},{'code': "ML", 'name': "Mali"},{'code': "MT", 'name': "Malta"},{'code': "MH", 'name': "Marshall Islands"},{'code': "MQ", 'name': "Martinique"},{'code': "MR", 'name': "Mauritania"},{'code': "MU", 'name': "Mauritius"},{'code': "YT", 'name': "Mayotte"},{'code': "MX", 'name': "Mexico"},{'code': "FM", 'name': "Micronesia, Federated States of"},{'code': "MD", 'name': "Moldova, Republic of"},{'code': "MC", 'name': "Monaco"},{'code': "MN", 'name': "Mongolia"},{'code': "ME", 'name': "Montenegro"},{'code': "MS", 'name': "Montserrat"},{'code': "MA", 'name': "Morocco"},{'code': "MZ", 'name': "Mozambique"},{'code': "MM", 'name': "Myanmar"},{'code': "NA", 'name': "Namibia"},{'code': "NR", 'name': "Nauru"},{'code': "NP", 'name': "Nepal"},{'code': "NL", 'name': "Netherlands"},{'code': "NC", 'name': "New Caledonia"},{'code': "NZ", 'name': "New Zealand"},{'code': "NI", 'name': "Nicaragua"},{'code': "NE", 'name': "Niger"},{'code': "NG", 'name': "Nigeria"},{'code': "NU", 'name': "Niue"},{'code': "NF", 'name': "Norfolk Island"},{'code': "MP", 'name': "Northern Mariana Islands"},{'code': "NO", 'name': "Norway"},{'code': "OM", 'name': "Oman"},{'code': "PK", 'name': "Pakistan"},{'code': "PW", 'name': "Palau"},{'code': "PS", 'name': "Palestinian Territory, Occupied"},{'code': "PA", 'name': "Panama"},{'code': "PG", 'name': "Papua New Guinea"},{'code': "PY", 'name': "Paraguay"},{'code': "PE", 'name': "Peru"},{'code': "PH", 'name': "Philippines"},{'code': "PN", 'name': "Pitcairn"},{'code': "PL", 'name': "Poland"},{'code': "PT", 'name': "Portugal"},{'code': "PR", 'name': "Puerto Rico"},{'code': "QA", 'name': "Qatar"},{'code': "RE", 'name': "Reunion"},{'code': "RO", 'name': "Romania"},{'code': "RU", 'name': "Russian Federation"},{'code': "RW", 'name': "Rwanda"},{'code': "BL", 'name': "Saint Barthelemy"},{'code': "SH", 'name': "Saint Helena, Ascension and Tristan Da Cunha"},{'code': "KN", 'name': "Saint Kitts and Nevis"},{'code': "LC", 'name': "Saint Lucia"},{'code': "MF", 'name': "Saint Martin (French Part)"},{'code': "PM", 'name': "Saint Pierre and Miquelon"},{'code': "VC", 'name': "Saint Vincent and the Grenadines"},{'code': "WS", 'name': "Samoa"},{'code': "SM", 'name': "San Marino"},{'code': "ST", 'name': "Sao Tome and Principe"},{'code': "SA", 'name': "Saudi Arabia"},{'code': "SN", 'name': "Senegal"},{'code': "RS", 'name': "Serbia"},{'code': "SC", 'name': "Seychelles"},{'code': "SL", 'name': "Sierra Leone"},{'code': "SG", 'name': "Singapore"},{'code': "SX", 'name': "Sint Maarten (Dutch Part)"},{'code': "SK", 'name': "Slovakia"},{'code': "SI", 'name': "Slovenia"},{'code': "SB", 'name': "Solomon Islands"},{'code': "SO", 'name': "Somalia"},{'code': "ZA", 'name': "South Africa"},{'code': "GS", 'name': "South Georgia and the South Sandwich Islands"},{'code': "ES", 'name': "Spain"},{'code': "LK", 'name': "Sri Lanka"},{'code': "SD", 'name': "Sudan"},{'code': "SR", 'name': "Suriname"},{'code': "SJ", 'name': "Svalbard and Jan Mayen"},{'code': "SZ", 'name': "Swaziland"},{'code': "SE", 'name': "Sweden"},{'code': "CH", 'name': "Switzerland"},{'code': "SY", 'name': "Syrian Arab Republic"},{'code': "TW", 'name': "Taiwan, Province of China"},{'code': "TJ", 'name': "Tajikistan"},{'code': "TZ", 'name': "Tanzania, United Republic of"},{'code': "TH", 'name': "Thailand"},{'code': "TL", 'name': "Timor-Leste"},{'code': "TG", 'name': "Togo"},{'code': "TK", 'name': "Tokelau"},{'code': "TO", 'name': "Tonga"},{'code': "TT", 'name': "Trinidad and Tobago"},{'code': "TN", 'name': "Tunisia"},{'code': "TR", 'name': "Turkey"},{'code': "TM", 'name': "Turkmenistan"},{'code': "TC", 'name': "Turks and Caicos Islands"},{'code': "TV", 'name': "Tuvalu"},{'code': "UG", 'name': "Uganda"},{'code': "UA", 'name': "Ukraine"},{'code': "AE", 'name': "United Arab Emirates"},{'code': "GB", 'name': "United Kingdom"},{'code': "US", 'name': "United States"},{'code': "UM", 'name': "United States Minor Outlying Islands"},{'code': "UY", 'name': "Uruguay"},{'code': "UZ", 'name': "Uzbekistan"},{'code': "VU", 'name': "Vanuatu"},{'code': "VE", 'name': "Venezuela, Bolivarian Republic of"},{'code': "VN", 'name': "Viet Nam"},{'code': "VG", 'name': "Virgin Islands, British"},{'code': "VI", 'name': "Virgin Islands, U.S."},{'code': "WF", 'name': "Wallis and Futuna"},{'code': "EH", 'name': "Western Sahara"},{'code': "YE", 'name': "Yemen"},{'code': "ZM", 'name': "Zambia"},{'code': "ZW", 'name': "Zimbabwe"},]

def send_email(request):
	args = {}
	if (request.method == "POST"):
		form = CaptchaForm(request.POST)
		# check the input
		if form.is_valid():
			human = True
			subject = request.POST.get('subject','')
			from_email = 'mSurvey Team<team@msurvey.co.ke>'
			to_email = "feedback@msurvey.co.ke"
			html_content = "From: mSurvey Team<team@msurvey.co.ke>"
			html_content = html_content + "\nTo:" + to_email
			html_content = html_content + "\nMIME-Version: 1.0"
			html_content = html_content + "\nContent-type: text/html"
			html_content = html_content + "\nSubject: " + subject
			html_content = html_content + "\n\n"
			html_content = html_content + request.POST.get('message','')
			html_content = html_content + "<br><br>" 
			html_content = html_content + "Yours truly,<br>" 
			html_content = html_content + request.POST.get('name','')+ "\n"
			html_content = html_content + request.POST.get('email','')
			
			try:
				smtp_user = "AKIAJNMYKO7A3NSJNZXQ"
				smtp_pass = "AjRTQfqglh9YQmVVT1JxK2q7npOakgUJdLfXAlK0ckOz"
				smtp_server = "email-smtp.us-east-1.amazonaws.com"
				smtp_port = "587"
				smtp = smtplib.SMTP(smtp_server,smtp_port)
				smtp.starttls()
				smtp.ehlo()
				smtp.login(smtp_user,smtp_pass)
				smtp.sendmail(from_email,to_email,html_content)
				smtp.close()
				args['response'] = "We have received your message."
			except e:
				args['response'] = "We have not received your message." + e
		else:
			args['response'] = "Are you really human?, Please try again."  
	else:
		form = CaptchaForm()
		args['response'] = "Sorry, please try again."  

	return HttpResponse(json.dumps(args), mimetype="application/json")








