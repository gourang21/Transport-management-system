from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,logout
from django.contrib.auth import login as dj_login
from django.contrib.auth.forms import UserChangeForm 
from transportapp.forms import EditProfileForm
from django.urls import reverse
from .models import *
from django.contrib.sessions.models import Session
from django.core.files.storage import FileSystemStorage
from datetime import datetime,date
from twilio.rest import Client
from django.core.paginator import Paginator, EmptyPage , PageNotAnInteger
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.http import JsonResponse
# Create your views here.

def home(request):
    if request.session.has_key('is_logged'):
        return redirect("/dashboard")

    return render(request, "home/home.html")

def signup(request):
    if request.session.has_key('is_logged'):
        return redirect("/dashboard")
    messages.success(request," Welcome to Sign up")
    return render(request, "home/signup.html")

# def login(request):
#     if request.session.has_key('is_logged'):
#         return redirect("/dashboard")
#     messages.success(request," Welcome to Login")
#     return render(request, "home/login.html")

def dashboard(request):
    if request.session.has_key('is_logged'):
        messages.success(request," Welcome to Dashboard")
    
        return render(request, "app/dashboard.html")
    return redirect('/login')

def get_data(request,*args,**kwargs):
        labels = ["Credit","Debit"]
        default_items=[10000,5000]
        data={
            "labels":labels,
            "default":default_items,
            # "users":User.objects.all().count(),
        }
        return JsonResponse(data)

# User= get_user_model()
# class ChartData(APIView):
#     authentication_classes = []
#     permission_classes = []

#     def get(self, request, format=None):
#         labels = ["Credit","Debit"]
#         default_items=[10000,5000]
#         data={
#             "labels":labels,
#             "default":default_items,
#             "users":User.objects.all().count(),
#         }
#         return Response(data)

#functions for handaling all processes related to cashbook 
def cashbook(request):
    if request.session.has_key('is_logged'):
        return render(request, "app/cashbook.html")
    return redirect('/login')

def cashbook_submit(request):
    if request.session.has_key('is_logged'):
        if request.method =='POST':
            cashbook_date=request.POST["cashbook_date"]
            particular=request.POST["particular"]
            cashbook_amount=request.POST["cashbook_amount"]
            transection_type=request.POST["transection_type"]
            user_id=request.session['user_id']
            obj=User.objects.get(id=user_id)
            cash_record=Cashbook(user=obj,cashbook_date=cashbook_date,particular=particular,cashbook_amount=cashbook_amount,transection_type=transection_type)
            cash_record.save()
            return render(request, "app/cashbook.html")
        else:
            return HttpResponse('404 - NOT FOUND ')
    return redirect('/login')  
        
def cashbook_edit(request,id):
    if request.session.has_key('is_logged'):
        cash=Cashbook.objects.get(id=id)
        cash_dic={'cash': cash}
        return render(request, "app/edit_cashbook.html",cash_dic)
    return redirect('/login')

def cashbook_update(request,id):
    if request.session.has_key('is_logged'):
        if request.method =='POST':
            cash=Cashbook.objects.get(id=id)
            cash.cashbook_date=request.POST["cashbook_date"]
            cash.particular=request.POST["particular"]
            cash.cashbook_amount=request.POST["cashbook_amount"]
            cash.transection_type=request.POST["transection_type"]
            cash.save()
            return redirect("/cashbook_show")
        else:
            return HttpResponse('404 - NOT FOUND ')
    return redirect('/login')    

def cashbook_delete(request,id):
    if request.session.has_key('is_logged'):
        cash=Cashbook.objects.get(id=id)
        cash.delete()
        return redirect('/cashbook_show')
    return redirect('/login')

def cashbook_show(request):
    if request.session.has_key('is_logged'):
        user_id = request.session['user_id']
        user =  User.objects.get(id = user_id)
        cash_record=Cashbook.objects.filter(user=user).order_by("-cashbook_date")
        paginator = Paginator(cash_record , 6)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)
        context = {'page_obj' : page_obj}
        return render(request,"app/cashbook_show.html",context)  
    return redirect('/login')

#functions for hnadling all processes related to bilty 
def bilty(request):
    if request.session.has_key('is_logged'):
        return render(request, "app/bilty.html")
    return redirect('/login')

def bilty_submit(request):
    if request.session.has_key('is_logged'):
        if request.method =='POST':
            lr_no=request.POST["lr_no"]
            invoiceno=request.POST["invoiceno"]
            truckno=request.POST["truckno"]
            date=request.POST["date"]
            consignor_details=request.POST["consignor_details"]
            consignee_details=request.POST["consignee_details"]
            rate=request.POST["rate"]
            weight=request.POST["weight"]
            fair=request.POST["fair"]
            mob=request.POST["mob"]
            advance=request.POST["advance"]
            recived_money=request.POST["recived_money"]
            goods_description=request.POST["goods_description"]
            if request.method=="POST":
                try:
                    lr_no_exist=Bilty.objects.get(lr_no=request.POST["lr_no"])
                    messages.error(request,"L.R. No. Already in Use")
                    return redirect("/bilty")
                except:
                    user_id=request.session['user_id']
                    obj=User.objects.get(id=user_id)
                    bilty_record=Bilty(user=obj,invoiceno=invoiceno,truckno=truckno,date=date,consignor_details=consignor_details,consignee_details=consignee_details,lr_no=lr_no,rate=rate,weight=weight,fair=fair,advance=advance,recived_money=recived_money,goods_description=goods_description,mob=mob)

                    # m=Bilty.objects.get(mob=request.POST["mob"])
                    if bilty_record.mob!="":     
                        account_sid ="AC35e5afb59d5e77987ece7986d1f4a661"
                        auth_token = "dfa1375b00d62d1328d174614286e252"
                        client = Client(account_sid, auth_token)

                        message = client.messages.create(
                                                    to="+91"+str(bilty_record.mob),
                                                    from_="+12082132722",
                                                    body="consignment booking:\n" + bilty_record.consignor_details +" "+"\n" + " L.R.NO:" +" " + bilty_record.lr_no +"\n"
                                                )
                    bilty_record.save()
            return redirect("/bilty")
        else:
            return HttpResponse('404 - NOT FOUND ')
    return redirect('/login')

def bilty_edit(request,id):
    if request.session.has_key('is_logged'):
        bilty=Bilty.objects.get(id=id)
        bilty_dic={'bilty': bilty}
        return render(request, "app/edit_bilty.html", bilty_dic)
    return redirect('/login')

def bilty_update(request,id):
    if request.session.has_key('is_logged'):
        if request.method =='POST':
            bilty=Bilty.objects.get(id=id)
            bilty.truckno=request.POST["truckno"]
            bilty.invoiceno=request.POST["invoiceno"]
            bilty.date=request.POST["date"]
            bilty.consignor_details=request.POST["consignor_details"]
            bilty.consignee_details=request.POST["consignee_details"]
            bilty.lr_no=request.POST["lr_no"]
            bilty.rate=request.POST["rate"]
            bilty.weight=request.POST["weight"]
            bilty.fair=request.POST["fair"]
            bilty.advance=request.POST["advance"]
            bilty.recived_money=request.POST["recived_money"]
            bilty.goods_description=request.POST["goods_description"]
            bilty.save()
            return redirect("/bilty_show")
        else:
            return HttpResponse('404 - NOT FOUND ')
    return redirect('/login')    

def bilty_delete(request,id):
    if request.session.has_key('is_logged'):
        bilty=Bilty.objects.get(id=id)
        bilty.delete()
        return redirect('/bilty_show')
    return redirect('/login')

def bilty_show(request):
    if request.session.has_key('is_logged'):
        user_id = request.session['user_id']
        user =  User.objects.get(id = user_id)
        bilty_record= Bilty.objects.filter(user=user).order_by("-lr_no")
        paginator = Paginator( bilty_record, 6)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)
        context = {'page_obj' : page_obj}
        return render(request,"app/bilty_show.html",context)      
    return redirect('/login')

#functions for handling all processes related to documnets 
def documents(request):
    if request.session.has_key('is_logged'):
        return render(request, "app/documents.html")
    return redirect('/login')

def upload(request):
    if request.method=="POST":
        truckno=request.POST["truckno"]
        puc=request.FILES["puc"]
        insurance=request.FILES["insurance"]
        rc=request.FILES["rc"]
        india_permit=request.FILES["india_permit"]
        state_permit=request.FILES["state_permit"]
        fitness=request.FILES["fitness"]
        decleration=request.FILES["decleration"]
        danda=request.FILES["danda"]
        user_id=request.session['user_id']
        obj=User.objects.get(id=user_id)
        doc_record=Document(user=obj,truckno=truckno,puc=puc,insurance=insurance,rc=rc,india_permit=india_permit,state_permit=state_permit,fitness=fitness,decleration=decleration,danda=danda)
        doc_record.save()
        # fs= FileSystemStorage()
        # fs.save(puc.name, puc)
        # fs.save(insurance.name, insurance)
        # fs.save(rc.name, rc)
        # fs.save(india_permit.name, india_permit)
        # fs.save(state_permit.name, state_permit)
        # fs.save(fitness.name, fitness)
        # fs.save(decleration.name, decleration)
        # fs.save(danda.name, danda)
    return render(request,"app/documents.html")    

def delete_doc(request,id):
    if request.method=="POST":
        docs=Document.objects.get(id=id)
        docs.delete()
        return redirect("document_show")    

def edit_doc(request,id):
    if request.session.has_key('is_logged'):
        docs=Document.objects.get(id=id)
        docs_dic={'docs': docs}
        return render(request, "app/edit_doc.html",docs_dic)
    return redirect('/login')       

def update_doc(request,id):
    if request.session.has_key('is_logged'):
        if request.method =='POST':
            docs=Document.objects.get(id=id)
            docs.truckno=request.POST["truckno"]
            docs.puc=request.FILES["puc"]
            docs.insurance=request.FILES["insurance"]
            docs.rc=request.FILES["rc"]
            docs.india_permit=request.FILES["india_permit"]
            docs.state_permit=request.FILES["state_permit"]
            docs.fitness=request.FILES["fitness"]
            docs.decleration=request.FILES["decleration"]
            docs.danda=request.FILES["danda"]
            docs.save()
            return redirect("/document_show")
        else:
            return HttpResponse('404 - NOT FOUND ')
    return redirect('/login')  

def document_show(request):
    if request.session.has_key('is_logged'):
        user_id = request.session['user_id']
        user =  User.objects.get(id = user_id)  
        docs=Document.objects.filter(user=user)
        paginator = Paginator( docs, 6)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)
        context = {'page_obj' : page_obj}
        return render(request,"app/document_show.html",context)  
    return redirect('/login') 

#functions for handling all processes related to Loans Record
def loans_record(request):
    if request.session.has_key('is_logged'):
        return render(request, "app/loans_record.html")
    return redirect('/login')

def cal_interest(loan_amount, interest_rate, loan_duration):
    return ((loan_amount+((loan_amount*interest_rate*loan_duration)/100))/(loan_duration*12))

def loans_record_submit(request):
    if request.session.has_key('is_logged'):
        if request.method =='POST':
            truckno=request.POST["truckno"]
            owner_name=request.POST["owner_name"]
            loan_amount=request.POST["loan_amount"]
            interest_rate=request.POST["interest_rate"]
            loan_duration=request.POST["loan_duration"]
            installment_date=request.POST["installment_date"]
            month_paid=request.POST["month_paid"]
            installment_amount=cal_interest(float(loan_amount), float(interest_rate), float(loan_duration))
            user_id=request.session['user_id']
            obj=User.objects.get(id=user_id)
            loan_record=Loan_Record(user=obj,truckno=truckno,owner_name=owner_name,loan_amount=loan_amount,interest_rate=interest_rate,loan_duration=loan_duration,installment_date=installment_date,month_paid=month_paid)
            loan_record.installment_amount=installment_amount
            if int(month_paid) != 0:
                loan_record.months=(int(loan_duration)*12)-int(month_paid)
            else:
                loan_record.months=int(loan_duration)*12    
            loan_record.save()
            return redirect("loans_record")
        else:
            return HttpResponse('404 - NOT FOUND ')
    return redirect('/login')

def loan_paid(request,id):
    if request.session.has_key('is_logged'):
            loan_record = Loan_Record.objects.get(id=id)
            paid=loan_record.month_paid*loan_record.installment_amount
            remain=(loan_record.loan_amount+((loan_record.loan_amount*loan_record.interest_rate*loan_record.loan_duration)/100))-paid
            loan_record.remain=remain
            loan_record.paid=paid
            if loan_record.months==0:
                messages.info(request,"ALL INSTALLMENTS ARE PAID THANK YOU!!!")
            a = {'loan_paid':loan_record}
            return render(request,"app/void.html", a)
    return redirect('/login')   

def loans_paid_update(request,id):
    if request.session.has_key('is_logged'):
        if request.method =='POST':
            loan=Loan_Record.objects.get(id=id)
            try:
                loan.inlineRadioOptions=request.POST["inlineRadioOptions"]
                if loan.inlineRadioOptions=="yes" and int(loan.months) !=0:                            
                    loan.month_paid=int(loan.month_paid)+1
                    loan.months=int(loan.months)-1
                else:
                    loan.month_paid=loan.month_paid
                    loan.months=loan.months
                loan.save()
                return redirect('/loans_record_show')
            except:
                messages.warning(request,"PLEASE CHOOSE A VALID OPTION")
                return redirect('/loans_record_show')    
        else:
            return HttpResponse('NOT FOUND ')

    return redirect('/login')

def loans_record_edit(request,id):
    if request.session.has_key('is_logged'):
        loan=Loan_Record.objects.get(id=id)
        loan_dic={'loan': loan}
        return render(request, "app/edit_loan.html", loan_dic)
    return redirect('/login')

def loans_record_update(request,id):
    if request.session.has_key('is_logged'):
        if request.method =='POST':
            loan=Loan_Record.objects.get(id=id)
            loan.truckno=request.POST["truckno"]
            loan.owner_name=request.POST["owner_name"]
            loan.loan_amount=request.POST["loan_amount"]
            loan.interest_rate=request.POST["interest_rate"]
            loan.loan_duration=request.POST["loan_duration"]
            loan.installment_date=request.POST["installment_date"]
            installment_amount=cal_interest(float(loan.loan_amount), float(loan.interest_rate), float(loan.loan_duration))
            loan.installment_amount=installment_amount
            # loan.month_paid=request.POST["month_paid"]
            # loan.months=request.POST["months"]
            loan.save()
            return redirect("/loans_record_show")
        else:
            return HttpResponse('404 - NOT FOUND ')
    return redirect('/login')

def loans_record_delete(request,id):
    if request.session.has_key('is_logged'):
        loan=Loan_Record.objects.get(id=id)
        loan.delete()
        return redirect('/loans_record_show')
    return redirect('/login')

def loans_record_show(request):
    if request.session.has_key('is_logged'):    
        user_id = request.session['user_id']
        user =  User.objects.get(id = user_id)
        loan_record= Loan_Record.objects.filter(user=user).order_by("installment_date")
        paginator = Paginator(loan_record , 4)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)
        context = {'page_obj' : page_obj}
        return render(request,"app/loans_record_show.html",context)  
    return redirect('/login') 

#functions for handling all processes related to trip profile
def trip_profile(request):
    if request.session.has_key('is_logged'):
        return render(request, "app/trip_profile.html")
    return redirect('/login')

def trip_submit(request):
    if request.session.has_key('is_logged'):
        if request.method =='POST':
            truckno=request.POST["truckno"]
            company_name=request.POST["company_name"]
            pickup=request.POST["pickup"]
            diesel=request.POST["diesel"]
            trip_kilometers=request.POST["trip_kilometers"]
            trip_expenses=request.POST["trip_expenses"]
            toll_tax=request.POST["toll_tax"]
            fair=request.POST["fair"]
            balance=request.POST["balance"]
            unloading_amount=request.POST["unloading_amount"]
            balance_collected=request.POST["balance_collected"]
            unloading_description=request.POST["unloading_description"]
            destination=request.POST["destination"]
            delivery_date=request.POST["delivery_date"]
            good_type=request.POST["good_type"]
            rate=request.POST["rate"]
            weight=request.POST["weight"]

            try:
                user_id=request.session['user_id']
                obj=User.objects.get(id=user_id)
                trip=TripProfile(user=obj,truckno=truckno,company_name=company_name,pickup=pickup,diesel=diesel,trip_kilometers=trip_kilometers,trip_expenses=trip_expenses,toll_tax=toll_tax,fair=fair,balance=balance,unloading_amount=unloading_amount,balance_collected=balance_collected,unloading_description=unloading_description,destination=destination,delivery_date=delivery_date,good_type=good_type,rate=rate,weight=weight)
                print("9")
            except Exception:
                print("10")
                pass
            try:
                print("1")
                destination2=request.POST["destination2"]
                delivery_date2=request.POST["delivery_date2"]
                good_type2=request.POST["good_type2"]
                rate2=request.POST["rate2"]
                weight2=request.POST["weight2"]
                user_id=request.session['user_id']
                obj=User.objects.get(id=user_id)
                trip=TripProfile(user=obj,truckno=truckno,company_name=company_name,pickup=pickup,diesel=diesel,trip_kilometers=trip_kilometers,trip_expenses=trip_expenses,toll_tax=toll_tax,fair=fair,balance=balance,unloading_amount=unloading_amount,balance_collected=balance_collected,unloading_description=unloading_description,destination=destination,destination2=destination2,delivery_date=delivery_date,delivery_date2=delivery_date2,good_type=good_type,good_type2=good_type2,rate=rate,rate2=rate2,weight=weight,weight2=weight2)

            except Exception:
                print ("2")
                pass


            try:
                print("3")
                destination3=request.POST["destination3"]
                delivery_date3=request.POST["delivery_date3"]
                good_type3=request.POST["good_type3"]
                rate3=request.POST["rate3"]
                weight3=request.POST["weight3"]
                user_id=request.session['user_id']
                obj=User.objects.get(id=user_id)
                trip=TripProfile(user=obj,truckno=truckno,company_name=company_name,pickup=pickup,diesel=diesel,trip_kilometers=trip_kilometers,trip_expenses=trip_expenses,toll_tax=toll_tax,fair=fair,balance=balance,unloading_amount=unloading_amount,balance_collected=balance_collected,unloading_description=unloading_description,destination=destination,destination2=destination2,delivery_date=delivery_date,delivery_date2=delivery_date2,good_type=good_type,good_type2=good_type2,rate=rate,rate2=rate2,weight=weight,weight2=weight2,destination3=destination3,delivery_date3=delivery_date3,good_type3=good_type3,rate3=rate3,weight3=weight3)

            except Exception:
                print("4")
                pass

            try:
                print("5")
                destination4=request.POST["destination4"]
                delivery_date4=request.POST["delivery_date4"]
                good_type4=request.POST["good_type4"]
                rate4=request.POST["rate4"]
                weight4=request.POST["weight4"]
                user_id=request.session['user_id']
                obj=User.objects.get(id=user_id)
                trip=TripProfile(user=obj,truckno=truckno,company_name=company_name,pickup=pickup,diesel=diesel,trip_kilometers=trip_kilometers,trip_expenses=trip_expenses,toll_tax=toll_tax,fair=fair,balance=balance,unloading_amount=unloading_amount,balance_collected=balance_collected,unloading_description=unloading_description,destination=destination,destination2=destination2,delivery_date=delivery_date,delivery_date2=delivery_date2,good_type=good_type,good_type2=good_type2,rate=rate,rate2=rate2,weight=weight,weight2=weight2,destination3=destination3,delivery_date3=delivery_date3,good_type3=good_type3,rate3=rate3,weight3=weight3,destination4=destination4,delivery_date4=delivery_date4,good_type4=good_type4,rate4=rate4,weight4=weight4)

            except Exception:
                print("6")
                pass

            try:
                print("7")
                destination5=request.POST["destination5"]
                delivery_date5=request.POST["delivery_date5"]
                good_type5=request.POST["good_type5"]
                rate5=request.POST["rate5"]
                weight5=request.POST["weight5"]
                user_id=request.session['user_id']
                obj=User.objects.get(id=user_id)
                trip=TripProfile(user=obj,truckno=truckno,company_name=company_name,pickup=pickup,diesel=diesel,trip_kilometers=trip_kilometers,trip_expenses=trip_expenses,toll_tax=toll_tax,fair=fair,balance=balance,unloading_amount=unloading_amount,balance_collected=balance_collected,unloading_description=unloading_description,destination=destination,destination2=destination2,delivery_date=delivery_date,delivery_date2=delivery_date2,good_type=good_type,good_type2=good_type2,rate=rate,rate2=rate2,weight=weight,weight2=weight2,destination3=destination3,delivery_date3=delivery_date3,good_type3=good_type3,rate3=rate3,weight3=weight3,destination4=destination4,delivery_date4=delivery_date4,good_type4=good_type4,rate4=rate4,weight4=weight4,destination5=destination5,delivery_date5=delivery_date5,good_type5=good_type5,rate5=rate5,weight5=weight5)
            
            except Exception:
                print("8")
                pass
                    
            finally:
                print("11")
                trip.save()
            return redirect("/trip_profile")

        return HttpResponse("404-page not found")
    return redirect("/login")

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

#Opens up page as PDF
class ViewPDF(View):
    def get(self, request,id,*args, **kwargs):
        data1 = TripProfile.objects.get(id=id)
        data={"data":data1}
        pdf = render_to_pdf('app/pdf_template.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

def trip_show(request):
    if request.session.has_key('is_logged'):    
        user_id = request.session['user_id']
        user =  User.objects.get(id = user_id)
        trip=TripProfile.objects.filter(user=user).order_by("delivery_date")
        paginator = Paginator(trip, 6)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)
        context = {'page_obj' : page_obj}
        return render(request,"app/trip_profile_show.html",context)  
    return redirect('/login')

def trip_profile_edit(request,id):
    if request.session.has_key('is_logged'):
        trip=TripProfile.objects.get(id=id)
        trip_dic={'trip': trip}
        return render(request, "app/edit_trip_profile.html",trip_dic)
    return redirect('/login')

def trip_profile_update(request,id):
    if request.session.has_key('is_logged'):
        if request.method =='POST':
            trip=TripProfile.objects.get(id=id)
            trip.truckno=request.POST["truckno"]
            trip.company_name=request.POST["company_name"]
            trip.pickup=request.POST["pickup"]
            trip.destination=request.POST["destination"]
            trip.destination2=request.POST["destination2"]
            trip.destination3=request.POST["destination3"]
            trip.destination4=request.POST["destination4"]
            trip.destination5=request.POST["destination5"]
            trip.delivery_date=request.POST["delivery_date"]
            trip.delivery_date2=request.POST["delivery_date2"]
            # trip.delivery_date3=request.POST["delivery_date3"]
            # trip.delivery_date4=request.POST["delivery_date4"]
            # trip.delivery_date5=request.POST["delivery_date5"]
            trip.good_type=request.POST["good_type"]
            trip.good_type2=request.POST["good_type2"]
            trip.good_type3=request.POST["good_type3"]
            trip.good_type4=request.POST["good_type4"]
            trip.good_type5=request.POST["good_type5"]
            trip.weight=request.POST["weight"]
            trip.weight2=request.POST["weight2"]
            trip.weight3=request.POST["weight3"]
            trip.weight4=request.POST["weight4"]
            trip.weight5=request.POST["weight5"]
            trip.rate=request.POST["rate"]
            trip.rate2=request.POST["rate2"]
            trip.rate3=request.POST["rate3"]
            trip.rate4=request.POST["rate4"]
            trip.rate5=request.POST["rate5"]
            trip.diesel=request.POST["diesel"]
            trip.trip_kilometers=request.POST["trip_kilometers"]
            trip.trip_expenses=request.POST["trip_expenses"]
            trip.toll_tax=request.POST["toll_tax"]
            trip.fair=request.POST["fair"]
            trip.balance=request.POST["balance"]
            trip.unloading_amount=request.POST["unloading_amount"]
            trip.balance_collected=request.POST["balance_collected"]
            trip.unloading_description=request.POST["unloading_description"]
            trip.save()
            return redirect("/trip_show")
        else:
            return HttpResponse('404 - NOT FOUND ')
    return redirect('/login')

def trip_profile_delete(request,id):
    if request.session.has_key('is_logged'):
        trip=TripProfile.objects.get(id=id)
        trip.delete()
        return redirect('/trip_show')
    return redirect('/login')

#functions for handling all processes related to truck maintenance
def truck_maintenance(request):

    if request.session.has_key('is_logged'):
        return render(request, "app/truck_maintenance.html")
    return redirect('/login')

def truck_maintenance_submit(request):
    if request.session.has_key('is_logged'):
        if request.method =='POST':
            truckno=request.POST["truckno"]
            service_date=request.POST["service_date"]
            service_km=request.POST["service_km"]
            service_details=request.POST["service_details"]
            service_by=request.POST["service_by"]
            service_cost=request.POST["service_cost"]
            service_note=request.POST["service_note"]
            user_id=request.session['user_id']
            obj=User.objects.get(id=user_id)
            truckmaint_record=TruckMaintenance(user=obj,truckno=truckno,service_date=service_date,service_km=service_km,service_details=service_details,service_by=service_by,service_cost=service_cost,service_note=service_note)
            truckmaint_record.save()
            return render(request, "app/truck_maintenance.html")
        else:
            return HttpResponse('404 - NOT FOUND ')
    return redirect('/login')

def truck_maintenance_edit(request,id):
    if request.session.has_key('is_logged'):
        truck=TruckMaintenance.objects.get(id=id)
        truck_dic={'truck': truck}
        return render(request, "app/edit_truck_maintenance.html",truck_dic)
    return redirect('/login')

def truck_maintenance_update(request,id):
    if request.session.has_key('is_logged'):
        if request.method =='POST':
            truck=TruckMaintenance.objects.get(id=id)
            truck.truckno=request.POST["truckno"]
            truck.service_date=request.POST["service_date"]
            truck.service_km=request.POST["service_km"]
            truck.service_details=request.POST["service_details"]
            truck.service_by=request.POST["service_by"]
            truck.service_cost=request.POST["service_cost"]
            truck.service_note=request.POST["service_note"]
            truck.save()
            return redirect("/truck_maintenance_show")
        else:
            return HttpResponse('404 - NOT FOUND ')
    return redirect('/login') 

def truck_maintenance_delete(request,id):
    if request.session.has_key('is_logged'):
        truck=TruckMaintenance.objects.get(id=id)
        truck.delete()
        return redirect('/truck_maintenance_show')
    return redirect('/login') 

def truck_maintenance_show(request):
    if request.session.has_key('is_logged'):
        user_id = request.session['user_id']
        user =  User.objects.get(id = user_id)
        truck_record=TruckMaintenance.objects.filter(user=user)
        paginator = Paginator(truck_record, 6)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)
        context = {'page_obj' : page_obj}
        return render(request,"app/truck_maintenance_show.html",context)  
    return redirect('/login')
    
# extra handling for pages like singup an login (intermediate processing)
def handlesignup(request):
        if request.method =='POST':
            # get the post parameters
            uname = request.POST["uname"]
            fname=request.POST["fname"]
            lname=request.POST["lname"]
            email = request.POST["email"]
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]

            # check for errors in input
            if request.method == 'POST':
                try:
                    user_exists = User.objects.get(username=request.POST['uname'])
                    messages.error(request," Username already taken, Try something else!!!")
                    return redirect("/signup")
                except User.DoesNotExist:
                    if len(uname)>15:
                        messages.error(request," Username must be max 15 characters, Please try again")
                        return redirect("/signup")
            
                    if not uname.isalnum():
                        messages.error(request," Username should only contain letters and numbers, Please try again")
                        return redirect("/signup")
            
                    if password1 != password2:
                        messages.error(request," Password do not match, Please try again")
                        return redirect("/signup")
            
            # create the user
            user = User.objects.create_user(uname, email, password1)
            user.first_name=fname
            user.last_name=lname
            user.save()
            messages.success(request," Your account has been successfully created")
            return redirect("/")
        
        else:
            return HttpResponse('404 - NOT FOUND ')

def handlelogin(request):
    if request.method =='POST':
        # get the post parameters
        loginuname = request.POST["loginuname"]
        loginpassword1=request.POST["loginpassword1"]
        user = authenticate(username=loginuname, password=loginpassword1)

        if user is not None:
            dj_login(request, user)
            messages.success(request, " Successfully logged in")
            request.session['is_logged']=True
            user=request.user.id
            request.session['user_id']=user
            print(user)
            print(request.session['user_id'])
            return redirect("/dashboard")
        else:
            messages.error(request," Invalid Credentials, Please try again")  
            return redirect("/")  
    
    return HttpResponse('404 - NOT FOUND ')

def handlelogout(request):
    del request.session['is_logged']
    del request.session['user_id']
    logout(request)
    messages.success(request, " Successfully logged out")
    return redirect('/')

#functions for handling all processes related to user profile
def view_profile(request):
    if request.session.has_key('is_logged'):
        args={'user':request.user}
        return render(request,"app/profile.html",args)
    return redirect('/login')

def edit_profile(request):
    if request.session.has_key('is_logged'):
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=request.user)

            if form.is_valid():
                form.save()
                return redirect('/profile')
        else:
            form = EditProfileForm(instance=request.user)
            args = {'form': form}
            return render(request, 'app/edit_profile.html', args)
    return redirect('/login')

#functions for handling all processes related to tyre profile
def tyre_record(request):
    if request.session.has_key('is_logged'):
        return render(request, "app/tyre_record.html")    
    return redirect('/login')

def tyre_record_submit(request):
    if request.session.has_key('is_logged'):
        if request.method =='POST':
            truckno=request.POST["truckno"]
            tyre_date=request.POST["tyre_date"]
            tyre_brand=request.POST["tyre_brand"]
            tyre_model=request.POST["tyre_model"]
            tyre_number=request.POST["tyre_number"]
            tyre_price=request.POST["tyre_price"]
            km_reading=request.POST["km_reading"]
            tyre_status=request.POST["tyre_status"]
            tyre_description=request.POST["tyre_description"]
            user_id=request.session['user_id']
            obj=User.objects.get(id=user_id)
            tyre_record=TyreRecord(user=obj,truckno=truckno,tyre_date=tyre_date,tyre_brand=tyre_brand,tyre_model=tyre_model,
            tyre_number=tyre_number,tyre_price=tyre_price,km_reading=km_reading,tyre_status=tyre_status,tyre_description=tyre_description)
            tyre_record.save()
            return redirect("tyre_record")
        return HttpResponse('404 - NOT FOUND ')
    return redirect('/login')

def tyre_record_edit(request,id):
    if request.session.has_key('is_logged'):
        tyre=TyreRecord.objects.get(id=id)
        tyre_dic={'tyre': tyre}
        return render(request, "app/edit_tyre_record.html",tyre_dic)
    return redirect('/login')

def tyre_record_update(request,id):
    if request.session.has_key('is_logged'):
        if request.method =='POST':
            tyre=TyreRecord.objects.get(id=id)
            tyre.truckno=request.POST["truckno"]
            tyre.tyre_date=request.POST["tyre_date"]
            tyre.tyre_brand=request.POST["tyre_brand"]
            tyre.tyre_model=request.POST["tyre_model"]
            tyre.tyre_number=request.POST["tyre_number"]
            tyre.tyre_price=request.POST["tyre_price"]
            tyre.km_reading=request.POST["km_reading"]
            tyre.tyre_status=request.POST["tyre_status"]
            tyre.tyre_description=request.POST["tyre_description"]
            tyre.save()
            return redirect("/tyre_record_show")
        else:
            return HttpResponse('404 - NOT FOUND ')
    return redirect('/login')    

def tyre_record_show(request):
    if request.session.has_key('is_logged'):    
        user_id = request.session['user_id']
        user =  User.objects.get(id = user_id)
        trip=TyreRecord.objects.filter(user=user).order_by("-tyre_date")
        paginator = Paginator(trip, 6)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)
        context = {'page_obj' : page_obj}
        return render(request,"app/tyre_record_show.html",context)  
    return redirect('/login')

def tyre_record_delete(request,id):
    if request.session.has_key('is_logged'):
        bilty=TyreRecord.objects.get(id=id)
        bilty.delete()
        return redirect('/tyre_record_show')
    return redirect('/login')

#function for handling all processes related to search
def search(request):

    if request.session.has_key('is_logged'):
        user_id = request.session['user_id']
        user =  User.objects.get(id = user_id)
        try:
            query=request.GET["query"]
            allBilty= Bilty.objects.filter(user=user,truckno__icontains=query)
            paginator = Paginator(allBilty , 4)
            page_number = request.GET.get('page')
            page_obj = Paginator.get_page(paginator,page_number)
            context = {'page_obj' : page_obj}
            return render(request,"app/bilty_show.html",context)
        except Exception:
            pass

        try:
            query=request.GET["query5"]
            allBilty= Cashbook.objects.filter(user=user,cashbook_date__icontains=query)
            paginator = Paginator(allBilty , 4)
            page_number = request.GET.get('page')
            page_obj = Paginator.get_page(paginator,page_number)
            context = {'page_obj' : page_obj}
            return render(request,"app/cashbook_show.html",context)
        except Exception:
            pass
        try:
            query=request.GET["query6"]
            allBilty= TripProfile.objects.filter(user=user,truckno__icontains=query)
            paginator = Paginator(allBilty , 4)
            page_number = request.GET.get('page')
            page_obj = Paginator.get_page(paginator,page_number)
            context = {'page_obj' : page_obj}
            return render(request,"app/trip_profile_show.html",context)
        except Exception:
            pass

        try:
            query=request.GET["query1"]
            docall= Document.objects.filter(user=user,truckno__icontains=query)
            params={"docs":docall}
            return render(request,"app/document_show.html",params)
        except Exception:
            try:
                query=request.GET["query2"]
                all_loan= Loan_Record.objects.filter(user=user,truckno__icontains=query).order_by("installment_date")
                paginator = Paginator(all_loan , 4)
                page_number = request.GET.get('page')
                page_obj = Paginator.get_page(paginator,page_number)
                context = {'page_obj' : page_obj}
                # params={"loan":all_loan}
                return render(request,"app/loans_record_show.html",context)
            except Exception:
                try:
                    query=request.GET["query3"]
                    mainall= TruckMaintenance.objects.filter(user=user,truckno__icontains=query)
                    params={"truck_maintenance":mainall}
                    return render(request,"app/trcuk_maintenance_show.html",params)
                except Exception:
                    pass        
                try:
                    query=request.GET["query4"]
                    tyreall= TyreRecord.objects.filter(user=user,tyre_number__icontains=query)
                    paginator = Paginator(tyreall , 4)
                    page_number = request.GET.get('page')
                    page_obj = Paginator.get_page(paginator,page_number)
                    context = {'page_obj' : page_obj}
                    return render(request,"app/tyre_record_show.html",context)
                except Exception:
                    pass        
    return redirect("/login")

# def check(request):
#     if request.method == 'POST':
#         user_exists = User.objects.filter(email=request.POST['email'])
#         messages.error(request,"Email not registered, TRY AGAIN!!!")
#         return redirect("/reset_password")         

def about(request):
    if request.session.has_key('is_logged'):
        return render(request,"app/about.html")
    return redirect("/")    

