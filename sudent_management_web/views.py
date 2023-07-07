from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from sudent_management_web.EmailBackEnd import EmailBackEnd
from django.contrib import messages
from django.urls import reverse
import json
import random
import time
from agora_token_builder import RtcTokenBuilder
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from sudent_management_web.models import Subjects, SessionYearModel, Students, Attendance, AttendanceReport, LeaveReportStaff, Staffs, FeedBackStaff, CustomUser, Courses, RoomMember
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def showDemoPage(request):
    return render(request, "demo.html")

def ShowLoginPage(request):
    return render(request, "login_page.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user= EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user!=None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request, "Invaild Login Details")
            return HttpResponseRedirect("/")

def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User: " +request.user.email+" usertype : "+request.user.user_type)
    else:
        return HttpResponse("Please Logn First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def getToken(request):
    appId = "1667456588664237b0003a48c66643ff"
    appCertificate = "85f24868843a4483a50c7cf0a2d37eb8"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)

@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)

def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)