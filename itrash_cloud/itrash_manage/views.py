from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from itrash_cloud.settings import MEDIA_ROOT
import time
from .models import *


# Create your views here.
def dologin(request):
    if request.user.is_authenticated:
        return redirect('/portal')   # 这是检查是否重复登录
    if request.method == "GET":
        context={"error_message":0}
        return render(request,'itrash_manage/login.html',context)
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/portal')
        else:
            context={"error_message":"用户名密码不匹配"}
            return render(request,'itrash_manage/login.html',context)


@login_required
def portal(request):
    context={"user": request.user}
    return render(request,'itrash_manage/portal.html',context)


def dologout(request):
    context = {"error_message": "没有登录"}
    if request.user.is_authenticated:
        logout(request)
        context = {"error_message": "成功登出"}
    return render(request, 'itrash_manage/login.html', context)


def doaudit(request):
    if not request.user.is_authenticated:
        res = {"redirect": 1, "authenticated": 0, "url": "/login"}
        return JsonResponse(res)
    if request.method=="GET":
        try:
            lblStr=(SysInfo.objects.get(pk="label")).kvalue
        except SysInfo.DoesNotExist as e:
            lblStr="battery,bottle,fruit,glass,paper"
        if not lblStr:
            lblStr = "battery,bottle,fruit,glass,paper"
        lblList=lblStr.split(",")
        picinfo_list=PicInfo.objects.filter(audit=False)
        isnull=0 if picinfo_list else 1
        context={"isnull":isnull,"picinfo":enumerate(picinfo_list), "nntypes":lblList}
        return render(request,'itrash_manage/doaudit.html',context)
    elif request.method=="POST":
        try:
            pid = request.POST["pid"]
            real = request.POST["real"]
            tar = PicInfo.objects.get(pk=pid)
            tar.audit = True
            tar.real = real
            img_name = tar.image.name.split('/')[-1]
            old_img_path = tar.image.path
            old_img_dir=os.path.dirname(old_img_path)
            new_img_dir = os.path.join(MEDIA_ROOT, 'trashimg', real)
            new_img_path=os.path.join(MEDIA_ROOT, 'trashimg', real,img_name)
            rel_new_img_path = 'trashimg/'+ real + "/" + img_name
            if not os.path.exists(new_img_dir):
                os.mkdir(new_img_dir)
            os.rename(old_img_path, new_img_path)
            if not os.listdir(old_img_dir):
                os.rmdir(old_img_dir)
            tar.image = ImageFieldFile(tar, tar.image, rel_new_img_path)
            tar.save_nothumb()
            msg = "已分类：" + real
            succ = 1
            pass
        except Exception as e:
            msg=str(e)
            succ=0
        return JsonResponse({"succ":succ,"msg":msg})


def sysinfo(request):
    isauth = request.user.is_authenticated
    res = {"redirect": 1, "authenticated": isauth, "url": "/admin/itrash_manage/sysinfo" if isauth else "/login"}
    return JsonResponse(res)


def userpage(request):
    isauth=request.user.is_authenticated
    res={"redirect":1,"authenticated":isauth,"url":"/admin/auth/user/"if isauth else "/login"}
    return JsonResponse(res)

def usergppage(request):
    isauth=request.user.is_authenticated
    res={"redirect":1,"authenticated":isauth,"url":"/admin/auth/group/"if isauth else "/login"}
    return JsonResponse(res)

def changePicInfo(request):
    isauth=request.user.is_authenticated
    res={"redirect":1,"authenticated":isauth,"url":"/admin/itrash_manage/picinfo/"if isauth else "/login"}
    return JsonResponse(res)

def index(request):
    return redirect('/portal')

@csrf_exempt
def upload(request):
    res=""
    succ=0
    if SysInfo.objects.get_or_create(pk="enableUpload")[0].kvalue=="1":
        try:
            pred=request.POST["pred"]
            machine=None
            barcode=None
            keys=request.POST.keys()
            if "mid" in keys:
                machine=request.POST["mid"]
            if "barcode" in keys:
                barcode=request.POST["barcode"]
            img=request.FILES.get('img')
            imgsuffix=img.name.split(".")[-1]
            img.name=(str(int(time.time()))+"_"+machine+"."+imgsuffix) if machine else (str(int(time.time()))+"_xx"+"."+imgsuffix)
            newPic=PicInfo(predict=pred,machine=machine,barcode=barcode,image=img,audit=False)
            newPic.save()
            succ=1
            res="success:"+pred
        except Exception as e:
            res=str(e)
    else:
        res="Upload Disabled"
    return JsonResponse({"succ":succ,"res":res})


def picrecord(request):
    if not request.user.is_authenticated:
        res = {"redirect": 1, "authenticated": 0, "url": "/login"}
        return JsonResponse(res)
    picinfo_list = PicInfo.objects.filter(audit=True)
    isnull = 0 if picinfo_list else 1
    context = {"isnull": isnull, "picinfo": enumerate(picinfo_list)}
    return render(request, 'itrash_manage/picrecord.html', context)


def overview(request):
    if not request.user.is_authenticated:
        res = {"redirect": 1, "authenticated": 0, "url": "/login"}
        return JsonResponse(res)
    auditedTrash=PicInfo.objects.filter(audit=True).count()
    correctTrash=PicInfo.objects.filter(audit=True,predict=F("real")).count()
    TrashAcc=str(round(correctTrash/auditedTrash*100,2))+"%" if auditedTrash else "100%"
    context={"totalTrash":PicInfo.objects.count(),"pendingTrash":PicInfo.objects.filter(audit=False).count(),"TrashAcc":TrashAcc,"correctTrash":correctTrash}
    return render(request, 'itrash_manage/overview.html', context)

def picrelbl(request):
    msg="失败"
    succ=0
    try:
        if request.method=="POST":
            pid=request.POST["pid"]
            picinfo=PicInfo.objects.get(pk=pid)
            picinfo.audit=False
            picinfo.save_nothumb()
            succ=1
            msg="成功"
    except Exception as e:
        msg=str(e)
    return JsonResponse({"succ":succ,"msg":msg})


def changeLbl(request):
    succ=0
    msg="失败"
    try:
        if request.method == "POST":
            lblStr = request.POST.get("lblStr")
            lblsetting = SysInfo.objects.get_or_create(pk="label")[0]
            lblsetting.kvalue = lblStr
            lblsetting.save()
            succ = 1
            msg = "成功更改类别,请刷新"
    except Exception as e:
        msg=str(e)
    return JsonResponse({"succ":succ,"msg":msg})


def stat(request,type):
    res={"succ":0}
    if type==1:
        harmtrash=SysInfo.objects.get_or_create(pk="harmtrash")[0].kvalue.split(",")
        cycletrash = SysInfo.objects.get_or_create(pk="cycletrash")[0].kvalue.split(",")
        wettrash = SysInfo.objects.get_or_create(pk="wettrash")[0].kvalue.split(",")
        drytrash = SysInfo.objects.get_or_create(pk="drytrash")[0].kvalue.split(",")
        harmtrash_c=PicInfo.objects.filter(audit=True,real__in=harmtrash).count()
        cycletrash_c = PicInfo.objects.filter(audit=True,real__in=cycletrash).count()
        wettrash_c = PicInfo.objects.filter(audit=True,real__in=wettrash).count()
        drytrash_c = PicInfo.objects.filter(audit=True,real__in=drytrash).count()
        res={"succ":1,"trashCount":[drytrash_c,cycletrash_c,wettrash_c,harmtrash_c]}
    elif type==2:
        harmtrash = HarmTrash.objects.count()
        cycletrash = CycleTrash.objects.count()
        drytrash = DryTrash.objects.count()
        wettrash = WetTrash.objects.count()
        res = {"succ": 1, "trashCount": [harmtrash, cycletrash, drytrash, wettrash]}
    return JsonResponse(res)


def deletePic(request):
    succ = 0
    msg = "失败"
    try:
        if request.method == "POST":
            pid = request.POST.get("pid")
            lblsetting = PicInfo.objects.get(pk=pid)
            lblsetting.delete()
            succ = 1
            msg = "成功删除图片,请刷新"
    except Exception as e:
        msg = str(e)
    return JsonResponse({"succ": succ, "msg": msg})


def control(request):
    if request.method=="GET":
        context={"enableUpload":int(SysInfo.objects.get_or_create(pk="enableUpload")[0].kvalue)}
        print(SysInfo.objects.get_or_create(pk="enableUpload")[0].kvalue)
        return render(request,'itrash_manage/control.html',context)
    if request.method=="POST":
        succ=0
        msg="失败"
        try:
            st=request.POST["st"]
            stobj=SysInfo.objects.get_or_create(pk="enableUpload")[0]
            stobj.kvalue =st
            stobj.save()
            succ = 1
            msg = "成功"
        except Exception as e:
            msg=str(e)
        return JsonResponse({"succ":succ,"msg":msg})


def queryTrash(request,q):
    harmtrash=HarmTrash.objects.filter(name__contains=q)
    cycletrash = CycleTrash.objects.filter(name__contains=q)
    drytrash = DryTrash.objects.filter(name__contains=q)
    wettrash = WetTrash.objects.filter(name__contains=q)
    context={"harmtrash":harmtrash,"cycletrash":cycletrash,"drytrash":drytrash,"wettrash":wettrash}
    return render(request,"itrash_manage/queryResult.html",context)
