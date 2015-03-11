from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.utils import timezone

from noe.engine import models as emodels
from noe.surveyAdmin.models import SurveyFactory
from noe.charts.models import *
from project.celeryapp import app

import datetime
import json
import csv

@login_required
def statisticalCSV(request, sf_id):

    try:
        sf = SurveyFactory.objects.get(id=sf_id, creator = request.user)
    except:
        if not request.user.is_superuser:
            return HttpResponseServerError("That survey could not be found or you are not the owner of the survey")
        else:
             sf = SurveyFactory.objects.get(id=sf_id)

    dataQuestions = emodels.DataQuestion.objects.filter(surveyFactory=sf)
    csvfile = '"User ID","Time finished'
    try:
        if (request.user.id == 493) and (request.user.username.lower() == 'safaricom'):
            csvfile = '"MSISDN","Time finished'
    except:
        pass
    respondents =[]

    respondents = emodels.DataResponse.objects.filter(question__surveyFactory = sf).distinct('respondent')

    for q in dataQuestions:
        csvfile=csvfile+ '","'+q.text

    for r in respondents:
        finished = emodels.SurveyProgress.objects.filter(respondent__id = int(r),surveyFactory = sf,finished=True).order_by('-finished_at')
        if finished:
            f = str(finished[0].finished_at)
        else:
            f = "Not yet finished"
        try:
            if request.user.id == 493 and request.user.username.lower() == 'safaricom':
                csvfile=csvfile+ '"\n'+ '"' + str(r.respondent.commID) + '","' + str(f) 
            else:
                csvfile=csvfile+ '"\n'+ '"' + str(r.id) + '","' + str(f) 
        except:
            csvfile=csvfile+ '"\n'+ '"' + str(r.id) + '","' + str(f) 

        for q in dataQuestions:
            try:
                response=emodels.DataResponse.objects.get(question = q, respondent = r)
                csvfile=csvfile+ '","' + str(response.text) 
            except:
                csvfile=csvfile +'","' + ' '
        
    csvfile=csvfile+ '"'         
        
    return HttpResponse(csvfile, content_type='text/csv')

@login_required
def improvedDownload(request, sf_id):

    try:
        sf = models.SurveyFactory.objects.get(id=sf_id, creator = request.user)
    except:
        if not request.user.is_superuser:
            return HttpResponseServerError("That survey could not be found or you are not the owner of the survey")
        else:
             sf = models.SurveyFactory.objects.get(id=sf_id)

    n = datetime.datetime.now()
    filename = str(sf.title)+'_'+str(n.day)+str(n.month)+str(n.year)+'.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
     
    finished = emodels.FinishedSurvey.objects.filter(surveyFactory = sf).distinct('respondent').order_by('-finished') 
    questions = emodels.DataQuestion.objects.filter(surveyFactory=sf)
    header = ["User id"]
    try:
        if (request.user.id == 493) and (request.user.username.lower() == 'safaricom'):
             header = ["MSISDN"]
    except:
        pass
    
    for item in questions:
        header.append(str(item.text))

    writer = csv.writer(response)
    writer.writerow(header)

    
    fNums = list(set(finished.values_list('respondent__id'))) #Get Distinct numbers

    for f in fNums:
        ''' Looping through all responses shall be slow. Could we get all responses by a user and break them down into sets of each question?
        '''
        
        f = str(int(list(f)[0])) #The Data is a tuple. Convert it to a string

        responses = emodels.DataResponse.objects.filter(respondent__id = f,question__surveyFactory__id = str(sf.id)).order_by('id').values_list('text',flat=True)
        
        x = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
        
        respGrouped = x(responses,len(questions))
        
        lastResp = respGrouped[-1] 
        l = len(lastResp)
        if  l !=  len(questions): #This will make sure the last list is of the correct lenght
            x = len(questions) - l #This will get us how many null cells are needed
            null = ['-']*x
            respGrouped[-1].extend(null)

        #respTrans = zip(*respGrouped)
        
        #print respTrans

        for item in respGrouped:
            ans = [str(f)]
            ans.extend(list(item))
            writer.writerow(ans)
            
    return response

@login_required
def improvedDownloadBranching(request, sf_id):

    try:
        sf = SurveyFactory.objects.get(id=sf_id, creator = request.user)
    except:
        if request.user.is_superuser:
            sf = models.SurveyFactory.objects.get(id=sf_id)
        else:
            return HttpResponseServerError("That survey could not be found or you are not the owner of the survey")
        
    response = createCSV(sf)
    return response

        #tasks.createCSV.apply_async(args=[sf], queue='createCSV')
    

@app.task(bind=True,name="noe.surveyAdmin.statisiticalCSV.taskCreateCSV",ignore_result=True,max_retries=2)
def taskCreateCSV(self,sf):
    try:
        start = datetime.datetime.now()
        print "creating csv at "+ str(start)
        createCSV(sf)  #''' Calling createCSV method'''
        end = datetime.datetime.now()
        print "Done creating csv at "+ str(end)
    except Exception as e:
        raise self.retry(exc=e, countdown=60)


def createCSV(sf):
    n = datetime.datetime.now()
    filename = str(sf.title)+'_'+str(n.day)+str(n.month)+str(n.year)+'.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+filename+'"'

    participants = emodels.SurveyProgress.objects.filter(surveyFactory = sf).distinct('respondent')
    questions = emodels.DataQuestion.objects.filter(surveyFactory=sf)
    header = ["User id"]
    try:
        if (request.user.id == 493) and (request.user.username.lower() == 'safaricom'):
            header = ["MSISDN"]
    except:
        pass


    qd = {}
    q_row = {}
    count = 0
    for q in questions:
        text = q.text.strip()
        if text in qd:
            lst = qd[text]
            lst.append(count)
            qd[text] = lst
        else:
            qd[text] = [count]
        count += 1

    questions2 = []
    for que in questions:
        text = que.text.strip()
        if text not in questions2:
            questions2.append(text)

    for item in questions2:
        header.append(str(item))

    writer = csv.writer(response)
    writer.writerow(header)

    numbers = participants.values_list('respondent__id',flat=True).distinct() 
    for f in numbers:
        for que in questions2:
            q_row[que] = []
        ''' Looping through all responses shall be slow. Could we get all responses by a user and break them down into sets of each question?
        '''
        f = str(f)
        #f = str(int(list(f)[0])) #The Data is a tuple. Convert it to a string

        responses = emodels.DataResponse.objects.filter(respondent__id = f,question__surveyFactory__id = str(sf.id)).order_by('id').values('question__surveyQuestionID','text')


        qs = []
        current = 0
        '''Get all responses. Check for missing responses Append null values where null values exist'''
        len_q = len(questions2)
        qs = ['-']*len_q #Insitialize an empty list of the length of the survey

        #For each response, replace teh null with a response
        for item in responses:
            qid = int(item.get('question__surveyQuestionID'))
            for k,v in qd.items():
                if qid in v:
                    lst = q_row[k]
                    lst.append(item['text'])
                    q_row[k] = lst
        count = 0
        for ques in questions2:
            qs[count]=(str(','.join(q_row[ques])))
            if qs[count] == '':
              qs[count] = "-"
            count += 1

        x = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]

        respGrouped = x(qs,len(questions2))

        lastResp = respGrouped[-1]
        l = len(lastResp)

        for item in respGrouped:
            ans = [str(f)]
            try:
                if (request.user.id == 493) and (request.user.username.lower() == 'safaricom'):
                    ans = [str(emodels.Respondent.objects.get(id = f).commID)]
            except:
                pass
            ans.extend(list(item))

            print ans
            writer.writerow(ans)

    return response

@login_required
def statisticalJSON(request, sf_id):

    try:
        sf = models.SurveyFactory.objects.get(id=sf_id, creator = request.user)
    except:
        if not request.user.is_superuser:
            return HttpResponseServerError("That survey could not be found or you are not the owner of the survey")
        else:
             sf = models.SurveyFactory.objects.get(id=sf_id)

    dataQuestions = emodels.DataQuestion.objects.filter(surveyFactory=sf_id)
    
    header = ["user_id"]

    for q in dataQuestions:
        header.append(q.text)

    print "printing header now"
    print header

    resp = emodels.DataResponse.objects.filter(question__surveyFactory__id = sf_id).values_list('respondent__id',flat=True).distinct()

    print "printing respondents now"
    print resp

    args = {}
    args['survey'] = sf.title
    row = {}

    for r in resp:
        re = {}

        finished = emodels.FinishedSurvey.objects.filter(respondent__id = str(r),surveyFactory = sf).order_by('-finished')
        if finished:
            re['finished'] = str(finished[0].finished)
        else:
            re['finished'] = "Not Yet Finished"
            
        for q in dataQuestions:
            try:
                response=emodels.DataResponse.objects.get(question = q, respondent__id = r)
                re[str(q.text)] = (response.text).strip()
            except:
                re[str(q.text)] = ""
        print re
        row[str(r)] = re

    args['response'] =  row
    print "printing csv now"
    print row

    jsondata = json.dumps(args)  
    
    return HttpResponse(jsondata, content_type='text/json')
    
@login_required
def pivotJSON(request, sf_id):
    try:
        sf = models.SurveyFactory.objects.get(id=sf_id, creator = request.creator)
    except:
        if not request.user.is_superuser:
            return HttpResponseServerError("That survey could not be found or you are not the owner of the survey")
        else:
             sf = models.SurveyFactory.objects.get(id=sf_id)

    dataQuestions = emodels.DataQuestion.objects.filter(surveyFactory=sf_id)
    
    header = []

    for q in dataQuestions:
        try:
            x = PivotSettings.objects.get(question = q)
            header.append(x.tag)
        except:
            continue

    print "printing header now"
    print header

    resp = emodels.DataResponse.objects.filter(question__surveyFactory__id = sf_id).values_list('respondent__id',flat=True).distinct()
    row = []

    for r in resp:
        re = {}
            
        for q in dataQuestions:
            try:
                x = PivotSettings.objects.get(question = q)
                if not x.show: continue
            except:
                continue
            try:
                response = emodels.DataResponse.objects.get(question = q, respondent__id = r)
                re[str(x.tag)] = (response.text).strip()
            except:
                re[str(x.tag)] = ""
        print re
        row.append(re)
    jsondata = json.dumps(row)  
    
    return HttpResponse(jsondata, content_type='text/json')

