from django.contrib import admin
from .models import *
# Register your models here.
class BiltyAdmin(admin.ModelAdmin):
    list_display=("user","invoiceno","truckno","date","lr_no","consignor_details","consignee_details")
class CashbookAdmin(admin.ModelAdmin):
    list_display=("user","cashbook_date","particular","cashbook_amount","transection_type")
class TruckMaintenanceAdmin(admin.ModelAdmin):
    list_display=("user","truckno","service_date","service_km","service_details","service_by","service_cost","service_note")
    
class Loan_RecordAdmin(admin.ModelAdmin):
    list_display=("user","truckno","owner_name","loan_duration","installment_date","month_paid","months")

class TripProfileAdmin(admin.ModelAdmin):
    list_display=("user","truckno","company_name","pickup","diesel","trip_kilometers","trip_expenses","toll_tax","fair","balance","unloading_amount","balance_collected","unloading_description")    

class TyreRecordAdmin(admin.ModelAdmin):
    list_display=("user","truckno","tyre_date","tyre_brand","tyre_model","tyre_number","tyre_price","km_reading","tyre_status","tyre_description")

admin.site.register(Cashbook,CashbookAdmin)
admin.site.register(Bilty,BiltyAdmin)
admin.site.register(Document)
admin.site.register(TyreRecord,TyreRecordAdmin)
admin.site.register(TripProfile,TripProfileAdmin)
admin.site.register(TruckMaintenance,TruckMaintenanceAdmin)
admin.site.register(Loan_Record,Loan_RecordAdmin)

