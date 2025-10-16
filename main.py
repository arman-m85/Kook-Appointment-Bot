
#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

from logging import info
from webbrowser import get
import telebot
from texts import text
import jdatetime
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton,KeyboardButton,ReplyKeyboardMarkup,ReplyKeyboardRemove
from DQL import get_customer_data,get_provider_data,get_customers_ID,get_providers_ID,get_service_info,get_provider_services_id,get_provider_services_row_id,get_provider_service_ID_by_cid,get_service_id_from_provider_service,get_datetime_info,get_service_id_by_name,get_provider_service_id,get_provider_id_from_provider_service,get_time_info_with_id,get_customer_appointment,remove_appointment,get_appointment_info
from DML import insert_customer_data,insert_provider_data,insert_service_data,insert_provider_service_table,delete_service,delete_provider_service_row,insert_time_table,insert_appointment,change_status
import time
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import logging
from config import TOKEN

logging.basicConfig(filename = "bot.log", level=logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

API_TOKEN = TOKEN
user_step={}
provider_step={}
user_info=dict() #{cid:{name:arman,phone:09123}}
provider_info=dict()
service_info=dict()
insert_service_info=dict()
time_info=dict()
select_service=dict()
datetime=dict()
bot = telebot.TeleBot(API_TOKEN)

today=jdatetime.datetime.now()
kabisah_years = [1399, 1403, 1408, 1412, 1416, 1420, 1424, 1428]

months = ['Farvardin', 'Ordibehesht', 'Khordad', 'Tir', 'Mordad', 'Shahrivar', 'Mehr', 'Aban', 'Azar', 'Dey', 'Bahman', 'Esfand']
month_days = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]



iranian_provinces = [
    "آذربایجان شرقی",
    "آذربایجان غربی",
    "اردبیل",
    "اصفهان",
    "البرز",
    "ایلام",
    "بوشهر",
    "تهران",
    "چهارمحال و بختیاری",
    "خراسان جنوبی",
    "خراسان رضوی",
    "خراسان شمالی",
    "خوزستان",
    "زنجان",
    "سمنان",
    "سیستان و بلوچستان",
    "فارس",
    "قزوین",
    "قم",
    "کردستان",
    "کرمان",
    "کرمانشاه",
    "کهگیلویه و بویراحمد",
    "گلستان",
    "گیلان",
    "لرستان",
    "مازندران",
    "مرکزی",
    "هرمزگان",
    "همدان",
    "یزد"
]

SERVICE_CATEGORIES = {
    "آرایش و زیبایی": {
        "آرایشگاه مردانه": "آرایشگاه مردانه",
        "سالن زیبایی و عروس": "سالن زیبایی و عروس",
        "ناخن‌کار": "ناخن‌کار",
        "مژه و ابرو": "مژه و ابرو",
        "ماساژ و اسپا": "ماساژ و اسپا",
        "مراقبت از پوست": "مراقبت از پوست"
    },
    "پزشکی و سلامت": {
        "پزشک عمومی": "پزشک عمومی",
        "متخصص": "متخصص",
        "دندانپزشک": "دندانپزشک",
        "فیزیوتراپی": "فیزیوتراپی",
        "روانشناس": "روانشناس",
        "تغذیه": "تغذیه",
        "بینایی‌سنجی": "بینایی‌سنجی",
        "شنوایی‌سنجی": "شنوایی‌سنجی"
    },
    "خدمات فنی و خودرو": {
        "تعمیرگاه خودرو": "تعمیرگاه خودرو",
        "تعویض روغنی": "تعویض روغنی",
        "کارواش": "کارواش",
        "برق‌کاری ساختمان": "برق‌کاری ساختمان",
        "لوله کشی": "لوله کشی"
    },
    "آموزش و مشاوره": {
        "کلاس موسیقی": "کلاس موسیقی",
        "کلاس زبان": "کلاس زبان",
        "مربی ورزشی": "مربی ورزشی",
        "وکیل": "وکیل",
        "مشاور مالی": "مشاور مالی"
    },
    "حیوانات خانگی": {
        "پت شاپ": "پت شاپ",
        "دامپزشک": "دامپزشک",
        "آرایش حیوانات": "آرایش حیوانات"
    },
    "سایر خدمات": {
        "عکاسی": "عکاسی",
        "خدمات نظافتی": "خدمات نظافتی",
        "خیاطی": "خیاطی"
    }
}


def send_notification():
    for info in get_appointment_info():
        cid=info['ID_customer']
        time=info['ID_time']
        time_info=get_time_info_with_id(time)
        date=time_info['DATE']
        hour=time_info['START_TIME']
        appointment_date =jdatetime.datetime(date.year, date.month, date.day, 0, 0)
        appointment_TIME=appointment_date + hour
        delta = appointment_TIME - jdatetime.datetime.now()
        print(delta)
        if delta > jdatetime.timedelta(minutes=0) and delta < jdatetime.timedelta(hours=1):

            change_status(info['ID'], 'notified')

            if info["status"] != 'notified':

                bot.send_message(cid, f"⏰ یادآوری: {delta} دقیقه دیگر وقت شما شروع می‌شود.")

                logging.info(f"Sent notification to {cid}: {delta} minutes remaining.")




Scheduler = BackgroundScheduler()
Scheduler.add_job(send_notification, 'interval', seconds=5)
Scheduler.start()




def create_calender(month,year):
    if int(year) in kabisah_years:
        print(month_days[-1])
        month_days[-1]=30
    else:
        month_days[-1]=29

    markup=InlineKeyboardMarkup(row_width=7)
    count=month_days[int(month)]
   
    list_btn=[]
    markup.add(InlineKeyboardButton(f"{months[int(month)]} {year}",callback_data="nothing"))
    for i in range(1,36):
        if i>count:
            list_btn.append(InlineKeyboardButton(f"{" "}",callback_data="nothing"))
    
        else:
           list_btn.append(InlineKeyboardButton(f"{i}",callback_data=f"set_{year}_{month}_{i}"))
    markup.add(*list_btn)
    markup.add(InlineKeyboardButton("<",callback_data=f"change_{month-1}_{year}_<"),
               InlineKeyboardButton("Cancel",callback_data=f"cancel"),
               InlineKeyboardButton(">",callback_data=f"change_{month+1}_{year}_>"))
    
    return markup


def provider_times(cid,id_provider_service,ID_time_table,service_name):
        info_time_table = get_time_info_with_id(ID_time_table)
        select_id_service = get_service_id_from_provider_service(id_provider_service)
        service_info = get_service_info(select_id_service)
        provider_id = get_provider_id_from_provider_service(id_provider_service)
        provider_name = get_provider_data(provider_id)["full_name"]
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("تایید ✅", callback_data=f"confirm_appointment_{cid}_{id_provider_service}_{ID_time_table}"))
        return markup,info_time_table,service_info,provider_name



def show_time_and_provider_and_city(id_provider_service,cid,service_name):
    markup = InlineKeyboardMarkup()
    for info in get_datetime_info(id_provider_service):
        print("tessssst")
        print(info)
        markup.add(InlineKeyboardButton(f" {info['DATE']} شروع : {info['START_TIME']} پایان : {info['END_TIME']}",callback_data=f"check_appointment_{cid}_{id_provider_service}_{info['ID']}_{service_name}"))
        print(f"{info["DATE"]}\n{info["START_TIME"]}\n{info["END_TIME"]}")
    return markup






def main_menu_markup():
    markup=InlineKeyboardMarkup()
    for cat in SERVICE_CATEGORIES:
        markup.add(InlineKeyboardButton( cat , callback_data=cat))
    return markup


def list_provide_services(cid):
    markup=InlineKeyboardMarkup()
           
    for ID in get_provider_services_id(cid):
        print("heyyyyyyyyyyyyyyyyyyy",type(ID[0]))
        ID=ID[0]
        result=get_service_info(ID)
        print(result)
        markup.add(InlineKeyboardButton(f"{result['name']}",callback_data=f"select_service_{result['ID']}"))
    markup.add(InlineKeyboardButton(" اضافه کردن سرویس جدید ➕",callback_data="add_service"))

    markup.add(InlineKeyboardButton("🗓️ زمان‌های شما",callback_data=f"show_provider_time_service_{cid}"))
    
    
    return markup

def show_customer_service(service_name):
    markup = InlineKeyboardMarkup()
    res = get_service_id_by_name(service_name)
    print(res)
    for id in res:
        id_provider_service = get_provider_service_id(id[0])[0]
        provider_cid = get_provider_id_from_provider_service(id_provider_service)
        info_provider = get_provider_data(provider_cid)
        markup.add(InlineKeyboardButton(f"{info_provider["full_name"]}   {info_provider["city"]}",callback_data = f"show_time_service_{id_provider_service}_service_name_{service_name}"))

        # for info in get_datetime_info(id_provider_service):
        #     markup.add(InlineKeyboardButton(f"تاریخ : {info["DATE"]} ساعت شروع : {info["START_TIME"]}  ساهت پایان : {info["END_TIME"]} شهر : {info_provider["city"]} سرویس دهنذه : {info_provider["full_name"]} ",callback_data="no" ))
        #     print(f"{info["DATE"]}\n{info["START_TIME"]}\n{info["END_TIME"]}")
    return markup


hide_board=ReplyKeyboardRemove()

def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(f"{m.chat.first_name} [{m.chat.id}]: {m.text}")
        else:
            print(f"{m.chat.first_name} [{m.chat.id}]: another type of message recieved, content type: {m.content_type}")


bot.set_update_listener(listener) 
# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid=message.chat.id
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✍️ نوبت بگیرم ",callback_data="Getting_appointment"))
    markup.add(InlineKeyboardButton("🚀 نوبت بدم ",callback_data="Giving_appointment"))
    bot.send_message(cid,f"{text["start"]}",reply_markup=markup)
    logging.info(f"Sent welcome message to {cid}.")



@bot.callback_query_handler(func= lambda call: True)
def call_handler(call):
    from texts import text

    call_id=call.id
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data
    print(f'call id: {call_id}, cid: {cid}, mid: {mid}, data: {data}')
    logging.info(f'call id: {call_id}, cid: {cid}, mid: {mid}, data: {data}')


# info_time_table = get_time_info_with_id(ID_time_table)
#         select_id_service = get_service_id_from_provider_service(id_provider_service)
#         service_info = get_service_info(select_id_service)
#         provider_id = get_provider_id_from_provider_service(id_provider_service)
#         provider_name = get_provider_data(provider_id)["full_name"]


    print(user_step)
    print(provider_step)
    if data.startswith("Getting") and (cid,) in get_customers_ID():
        user_step[cid] = "login"
        bot.answer_callback_query(call_id,"وارد شدید! ✅")
        logging.info(f"User logged in successfully cid : {cid}.")
        bot.delete_message(cid,mid)
        new_markup = InlineKeyboardMarkup()
        if len(get_customer_appointment(cid)) >= 1:
            for appointment in get_customer_appointment(cid):

                id_provider_service = appointment["ID_provider_service"]
                ID_time_table = appointment["ID_time"]
                info_time_table = get_time_info_with_id(ID_time_table)
                select_id_service = get_service_id_from_provider_service(id_provider_service)
                service_info = get_service_info(select_id_service)
                provider_id = get_provider_id_from_provider_service(id_provider_service)
                provider_name = get_provider_data(provider_id)["full_name"]        
                
                service_name=service_info["name"]
                
                print(f"testttttttt  {appointment}")
                print(service_name)
                print(provider_name)
                print(provider_id)

                logging.debug(f"Processing appointment: {appointment}")
                logging.debug(f"Service name: {service_name}")
                logging.debug(f"Provider name: {provider_name}")
                logging.debug(f"Provider ID: {provider_id}")
                
                new_markup.add(InlineKeyboardButton(f"  {info_time_table['DATE']}  شروع : {info_time_table['START_TIME']}  پایان : {info_time_table['END_TIME']}",callback_data = f"choose_{ID_time_table}_{service_name}_{provider_id}"))
                #f"see_{provider_name}_{service_name}_{provider_id}"
                
            new_markup.add(InlineKeyboardButton("⏰ افزودن زمان‌ جدید",callback_data = "add_service"))
            bot.send_message(cid,"زمان های شما 👇 \n (برای دیدن اطلاعات بیشتر یکی از زمان ها را انتخاب کنید)",reply_markup=new_markup)
            logging.info(f"Sent appointment times to coustomer customer cid : {cid}.")
            
                


                #f"customer_select_service_detail_{provider_name}_{provider_id}"
                #detail_service_{service_info["name"]}_{provider_name}_{provider_id}
        else:
            markup = main_menu_markup()
            bot.send_message(cid,"لطفا یکی از دسته‌بندی‌های زیر را انتخاب کنید:",reply_markup=markup)
            logging.info(f"Sent main menu to unregistered {cid}.")

    elif data.startswith("choose"):
        bot.answer_callback_query(call_id,"در حال بارگذاری اطلاعات...")
        _,ID_time_table,service_name,provider_id = data.split("_")
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("ℹ️ اطلاعات بیشتر  ",callback_data=f"see_{ID_time_table}_{service_name}_{provider_id}"))
        markup.add(InlineKeyboardButton("🗑️ حذف سرویس ",callback_data=f"remove_service_{ID_time_table}_{service_name}_{provider_id}"))

        bot.send_message(cid,"لطفا یکی از گزینه های زیر را انتخاب کنید:",reply_markup=markup)
        logging.info(f"Sent service options to customer cid : {cid}.")

    elif data.startswith("remove_service"):
        bot.answer_callback_query(call_id,"در حال بارگذاری اطلاعات...")
        _,_,ID_time_table,service_name,provider_id = data.split("_")
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("بله ✅",callback_data=f"confirm_remove_service_{ID_time_table}_{service_name}_{provider_id}"),
        InlineKeyboardButton("خیر ❌",callback_data="cancel_remove_service"))
        bot.edit_message_text(f"آیا از حذف سرویس {service_name} مطمئن هستید؟",cid,mid,reply_markup=markup)
        logging.info(f"Sent remove service confirmation to customer cid : {cid}.")

    elif data.startswith("cancel_remove_service"):
        bot.answer_callback_query(call_id,"عملیات حذف سرویس لغو شد.")
        bot.edit_message_text(f"عملیات حذف سرویس لغو شد.",cid,mid)
        logging.info(f"Cancelled remove service for customer cid : {cid}.")

    elif data.startswith("confirm_remove_service"):
        bot.answer_callback_query(call_id,"حذف سرویس در حال انجام است...")
        _,_,_,ID_time_table,service_name,provider_id = data.split("_")
        remove_appointment(cid, ID_time_table)
        bot.edit_message_text(f"❌ سرویس «{service_name}» با موفقیت حذف شد.",cid,mid)
        logging.info(f"Removed service {service_name} for customer cid : {cid}.")

    elif data.startswith("see"):
        bot.answer_callback_query(call_id,"در حال بارگذاری اطلاعات...")
        _,ID_time_table,service_name,provider_id = data.split("_")
        provider_info = get_provider_data(provider_id)
        longitude = provider_info["longitude"]
        latitude = provider_info["latitude"]
        bot.send_message(cid,provider_info["address"])
        bot.send_location(cid,latitude,longitude)
        logging.info(f"Sent provider location to customer cid : {cid}.")

    
    # elif data.startswith("detail_service"):
    #     _,_,service_name,provider_name,provider_id = data.split("_")


    elif data.startswith("Giving") and (cid,) in get_providers_ID():
        provider_step[cid]="login"

        bot.answer_callback_query(call_id,"وارد شدید! ✅")
        logging.info(f"Provider logged in successfully cid : {cid}.")
        bot.delete_message(cid,mid)
        if get_provider_services_id(cid):

            markup = list_provide_services(cid)

            bot.send_message(cid,"سرویس های شما 👇",reply_markup = markup)

        else:

            markup=main_menu_markup()
            bot.send_message(cid,"برای نمایش بهتر خدماتتان، دسته بندی شغلی خود را انتخاب کنید. ✨",reply_markup=markup)
        print(data) 
        provider_step.pop(cid)
        logging.debug(f"Received data from provider cid : {cid} - {data}")

    elif data.startswith("select_service"):
        _,_,ID=data.split("_")
        info = get_service_info(ID)

        select_service.setdefault(cid,dict())
        select_service[cid]["service_id"]=ID

        text=f"""
نام سرویس : {info["name"]}
قیمت سرویس : {info["duration_minutes"]}
زمان سرویس : {info["price"]}

"""     
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🗓️ ثبت نوبت ",callback_data=f"show_calender"))
        markup.add(InlineKeyboardButton("✏️ ویرایش سرویس",callback_data=f"edit_service_{ID}"))
        markup.add(InlineKeyboardButton( "❌ حذف سرویس ",callback_data=f"remove_provider_service_{ID}"))


        bot.edit_message_text(text,cid,mid,reply_markup=markup)
        logging.info(f"Edited service selection for provider cid : {cid}.")


    elif data.startswith("show_calender") :
        bot.edit_message_text(" تاریخ مورد نظر را انتخاب کنید 🗓️ ",cid,mid,reply_markup=create_calender((today.month)-1,today.year))
        
    if data.startswith("change"):

        _,month,year,action=data.split("_")
        month=int(month)
        year=int(year)
        if month==12:

            year+=1
            month=0
        if month==-1:
            year-=1
            month=11
        print(month)
        print(action)
        bot.edit_message_reply_markup(cid,mid,reply_markup=create_calender(int(month),int(year)))

    elif data.startswith("set"):
        _,year,month,day=data.split("_")
        text=f"تاریخ انتخابی شما \n {year}/{int(month)+1}/{day}"
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ تایید تاریخ ✅",callback_data=f"Confirm_the_{year}_{month}_{day}"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="return"))
        bot.edit_message_text(text,cid,mid,reply_markup=markup)
    elif data.startswith("return"):
        text="مجدد انتخاب کنید"
        bot.edit_message_text(text,cid,mid,reply_markup=create_calender((today.month)-1,today.year))
    
    elif data.startswith("Confirm"):
        _,_,year,month,day=data.split("_")
        text=f"   تاریخ تایید شد ✅🗓️\n {year}/{int(month)+1}/{day}"

        select_service[cid]["date"]=f"{year}-{int(month)+1}-{day}"

        logging.info(f"Confirmed appointment date for provider cid : {cid} - {select_service[cid]['date']}")

        bot.answer_callback_query(call_id,"تاریخ ثبت شد")
        bot.edit_message_text(text,cid,mid)
        bot.send_message(cid,"""👋 دوست عزیز، برای رزرو نوبت، لطفا زمان شروع و پایان مورد نظرت رو با فرمت ۲۴ ساعته و به شکل زیر بفرست:
12:30-13:30 🗓️""")
        provider_step[cid] = "time"
        logging.info(f"Requested time for appointment from provider cid : {cid}.")


   # elif data.startswith("remove_service"):
    elif data.startswith("edit_service"):
        _,_,ID_service=data.split("_")

        keyboard=ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("تمایل ندارم ❌"))
        bot.delete_message(cid,mid)
        name_service=get_service_info(ID_service)["name"]
        insert_service_info["name"]=name_service
        delete_provider_service_row(cid,ID_service)
        delete_service(ID_service)
        bot.send_message(cid,"لطفاً اطلاعات سرویس را دوباره وارد کنید. 📝")
        bot.send_message(cid,"لطفاً مدت زمان سرویس را وارد کنید (به دقیقه). ⏰",reply_markup=keyboard)
        provider_step[cid] = "service_duration"
        logging.info(f"Requested service duration for provider in edit_service cid : {cid}.")


    elif data.startswith("remove_provider_service"):
        _,_,_,ID_service=data.split("_")
        delete_provider_service_row(cid,ID_service)
        delete_service(ID_service)
        markup = list_provide_services(cid)

        bot.edit_message_text("سرویس های شما 👇",cid,mid,reply_markup = markup)
        logging.info(f"Removed service {ID_service} for provider cid : {cid}.")
        

        
        

    elif data.startswith("add_service"):
        markup=main_menu_markup()
        bot.edit_message_text("لطفا یکی از دسته‌بندی‌های زیر را انتخاب کنید:",cid,mid,reply_markup=markup)
        logging.info(f"Sent service categories to {cid}.")


    elif data in SERVICE_CATEGORIES.keys() and (cid,) in get_customers_ID():
        markup=InlineKeyboardMarkup(row_width=2)
        service_list=[]
        
        for service in SERVICE_CATEGORIES[data]:
            service_list.append(InlineKeyboardButton(service,callback_data=f"customer_select_service_{service}"))
        print(service_list)
        markup.add(*service_list)
        markup.add(InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main_menu"))

        bot.edit_message_text(f"شما دسته ' {data} ' را انتخاب کردید. حالا سرویس مورد نظر خود را از لیست زیر انتخاب کنید: 👇",cid,mid,reply_markup=markup)
        logging.debug(f"Sent service options to customer cid : {cid}.")

    elif data.startswith("customer_select_service"):
        _,_,_,service_name= data.split("_")
        markup = InlineKeyboardMarkup()
        markup = show_customer_service(service_name)
        bot.send_message(cid,"لطقا نام شهر و سرویس دهنده خود را انتخاب کنید ",reply_markup=markup)
        logging.info(f"Requested city and provider selection for customer cid : {cid}.")

    
    
    elif data.startswith("show_time_service"):
        print(data,"testtttttttttttttttttttttttt")
        _,_,_,id_provider_service,_,_,service_name = data.split("_")
        markup = InlineKeyboardMarkup()
        if get_datetime_info(id_provider_service):

            markup = show_time_and_provider_and_city(id_provider_service,cid,service_name)
            
            markup.add(InlineKeyboardButton("بازگشت 🔙",callback_data = f"go_back_to_show_customer_service_{service_name}"))
            bot.edit_message_text("لطفا زمان و روز مورد نظر خود را انتخاب کنید ",cid,mid,reply_markup = markup)
            logging.info(f"Requested time and date selection for customer cid : {cid}.")
        else:
            markup.add(InlineKeyboardButton("بازگشت 🔙",callback_data = f"go_back_to_show_customer_service_{service_name}"))
            bot.edit_message_text("زمانی از طرف سرویس دهنده ارائه نشده ",cid,mid,reply_markup = markup)
            logging.warning(f"No time slots available for provider id_provider_service : {id_provider_service}.")

    elif data.startswith("go_back_to_show_customer_service") :
        _,_,_,_,_,_,service_name = data.split("_")
        markup = show_customer_service(service_name)
        bot.edit_message_text("لطقا نام شهر و سرویس دهنده خود را انتخاب کنید ",cid,mid,reply_markup=markup)




    







    elif data.startswith("check_appointment"):
        _,_,cid,id_provider_service,ID_time_table,service_name = data.split("_")
        #r = provider_times(cid,id_provider_service,ID_time_table,service_name)
        # info_time_table = r[1]
        # provider_name = r[3]
        # markup = r[0]
        info_time_table = get_time_info_with_id(ID_time_table)
        select_id_service = get_service_id_from_provider_service(id_provider_service)
        service_info = get_service_info(select_id_service)
        provider_id = get_provider_id_from_provider_service(id_provider_service)
        provider_name = get_provider_data(provider_id)["full_name"]
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("تایید ✅", callback_data=f"confirm_appointment_{cid}_{id_provider_service}_{ID_time_table}"))
        # print(f"{info_time_table} testttttt")

        markup.add(InlineKeyboardButton("بازگشت 🔙",callback_data=f"Bback_to_show_time_{id_provider_service}_{cid}_{service_name}"))
        bot.edit_message_text(f"نام سرویس : {service_name} \n  نام سرویس دهنده : {provider_name}  \n  تاریخ : {info_time_table["DATE"]} \n  ساعت شروع : {info_time_table["START_TIME"]} \n  ساعت پایان : {info_time_table["END_TIME"]}",cid,mid,reply_markup=markup )
        logging.info(f"Displayed appointment details for customer cid : {cid}.")

        #bot.edit_message_text(f"سرویس : {service_name} ")

    elif data.startswith("Bback_to_show_time"):
        _,_,_,_,id_provider_service,cid,service_name = data.split("_")
        markup = show_time_and_provider_and_city(id_provider_service,cid,service_name)
        bot.edit_message_text("لطفا زمان و روز مورد نظر خود را انتخاب کنید ",cid,mid,reply_markup = markup)

        
        
    elif data.startswith("confirm_appointment"):
        _,_,cid,id_provider_service,ID_time_table = data.split("_")

        bot.edit_message_text("در حال ثبت نوبت شما ...", cid, mid)
        sent_message=bot.send_message(cid, "⌛")
        insert_appointment (id_provider_service, ID_time_table, cid)
        time.sleep(2)
        bot.delete_message(cid, sent_message.message_id)



        bot.edit_message_text("نوبت شما با موفقیت ثبت شد. ✅",cid,mid)
        logging.info(f"Successfully registered appointment for customer cid : {cid}.")

        

           


    
    elif data in SERVICE_CATEGORIES.keys() and (cid,) in get_providers_ID():
        markup=InlineKeyboardMarkup(row_width=2)
        service_list=[]
        
        for service in SERVICE_CATEGORIES[data]:
            service_list.append(InlineKeyboardButton(service,callback_data=f"provider_{service}"))
            logging.debug(f"Added service button for {service} in category {data}.")

        markup.add(*service_list)
        markup.add(InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main_menu"))

        bot.edit_message_text(f"شما دسته ' {data} ' را انتخاب کردید. حالا سرویس مورد نظر خود را از لیست زیر انتخاب کنید: 👇",cid,mid,reply_markup=markup)

        
      
    elif data.startswith("provider_"):
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(f"ادامه ➡️",callback_data=f"accept_{data.split("_")[1]}"))
        markup.add(InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main_menu"))
        bot.edit_message_text(f"سرویس {data.split("_")[1]} انتخاب شد ✅",cid,mid,reply_markup=markup)

    elif data.startswith("accept_"):
        logging.debug(f"service_name : {data.split('_')[1]}")
        print(f"my test   {data.split('_')[1]}   my test")
        insert_service_info["name"]=data.split("_")[1]
        print(f"my test   {insert_service_info}   my test")
        logging.debug(f"service_name : {data.split('_')[1]}")
        keyboard=ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("تمایل ندارم ❌"))
        bot.delete_message(cid,mid)

        bot.send_message(cid,"لطفاً مدت زمان سرویس را وارد کنید (به دقیقه). ⏰",reply_markup=keyboard)

        provider_step[cid]="service_duration"
        print(provider_step.get(call.message.chat.id))

    if data.startswith("back"):
        bot.edit_message_text("شما به منوی اصلی بازگشتید.", cid, mid, reply_markup=main_menu_markup())

    if data.startswith("Getting") and (cid,) not in get_customers_ID():
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(f"{text["Registration Button"]}",callback_data="Registration_user"))
        logging.info(f"Requested user registration cid : {cid}.")
        bot.edit_message_text(f"{text["Registration"]}",cid,mid,reply_markup=markup)
    
    elif data.startswith("Giving") and (cid,) not in get_providers_ID():
        markup=InlineKeyboardMarkup()
        logging.info(f"Requested provider registration cid : {cid}.")
        logging.debug(f" text : {text}")
        print(text)
        markup.add(InlineKeyboardButton(f"{text["Registration Button"]}",callback_data="Registration_provider"))
        
        bot.edit_message_text(f"{text["Registration"]}",cid,mid,reply_markup=markup)
        

    if data.startswith("Registration_provider"):
        bot.edit_message_text(f"{text["first_name and last_name"]}",cid,mid)
        provider_step[cid]="Full_Name"
        print("final",provider_step)
        logging.debug(f"provider_step : {provider_step}")


    if data.startswith("Registration_user"):

       # bot.delete_message(cid,mid)
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("👨🏻 مرد ",callback_data=f"MALE_{cid}"),
                   InlineKeyboardButton("👩🏻 زن ",callback_data=f"FEMALE_{cid}")
        )
        bot.edit_message_text("لطفا جنسیت خود را انتخاب کنید 👇",cid,mid,reply_markup=markup)
        logging.info(f"Requested gender selection for user cid : {cid}.")

    elif data.startswith("MALE") or data.startswith("FEMALE") :
        SEX,_=data.split("_")
        user_info.setdefault(cid,dict())
        user_info[cid]["SEX"]=SEX

        logging.debug(f"user_info : {user_info} user_step : {user_step} cid : {cid}")
        print(user_info)
        print(user_step)
        print(cid)
        
        bot.edit_message_text(f"{text["first_name and last_name"]}",cid,mid)
        user_step[cid]="Full_Name"
        logging.debug(f"user_info : {user_info} user_step : {user_step} cid : {cid}")
        print(user_info)
        print("*********",user_step.get(cid))
        print(type(call.message.chat.id))
        

    elif data.startswith("show_provider_time_service"):
        _,_,_,_,cid=data.split("_")
        text=""
        for provider_service_id in get_provider_service_ID_by_cid(cid):
            print(provider_service_id)
            service_id = get_service_id_from_provider_service(provider_service_id[0])
            service_name = get_service_info(service_id)["name"]
            text+="\n"
            for id in provider_service_id:
                res=get_datetime_info(id)
                for info in res:
                    print(f"{info["DATE"]}\n{info["START_TIME"]}\n{info["END_TIME"]}")
                    text+=f"""
نام سرویس : {service_name}
تاریخ سرویس : {info["DATE"]}
زمان شروع سرویس : {info["START_TIME"]}
زمان پایان سرویس : {info["END_TIME"]}
""" 
                    if info["IS_BOOKED"] == 0:

                        text+="وضعیت : رزرو نشده \n"
                        
                    else:
                        text+="وضعیت : رزرو شده \n"
                        logging.debug(f"Appointment details for provider cid : {cid} service_id : {id} info : {info}")

        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("بازگشت 🔙",callback_data=f"goback_from_datetime_list_{cid}"))
        
        bot.edit_message_text(text,cid,mid,reply_markup=markup)

    elif data.startswith("goback_from_datetime_list"):
        _,_,_,_,cid = data.split("_")

        markup = list_provide_services(cid)
        bot.edit_message_text("سرویس های شما 👇",cid,mid,reply_markup = markup)

    

               

# @bot.message_handler(commands=["location"])
# def send_loc(message):
#     cid=message.chat.id

#     provider_location=get_provider_data(cid)
#     print(provider_location)
    
#     one=provider_location["longitude"]
#     two=provider_location["latitude"]
#     bot.send_location(cid,two,one)

@bot.message_handler(func=lambda message : provider_step.get(message.chat.id) == "Full_Name")
def provider_name_handler(message):
    cid=message.chat.id
    user_name=message.text
    provider_info.setdefault(cid,dict())
    provider_info[cid]["FULL_NAME"]=user_name.strip()
    logging.info(f"Received full name for provider cid : {cid} name : {user_name.strip()}.")
    provider_step.pop(cid)
    print("final",provider_info)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_provinces=[]

    for i in iranian_provinces:
        button_provinces.append(KeyboardButton(f"{i}"))

    keyboard.add(*button_provinces)
    
    bot.send_message(cid," لطفا شهر مورد نظر خود را انتخاب کنید ازطریق کلید های زیر 👇",reply_markup=keyboard)
    provider_step[cid]="provider_city"
    print("*******360***",provider_step)
    logging.info(f"Requested city selection for provider cid : {cid}.")
    logging.debug(f"provider_step : {provider_step}")



@bot.message_handler(func=lambda message : user_step.get(message.chat.id) == "Full_Name")
def user_name_handler(message):
    cid=message.chat.id
    user_name=message.text
    
    user_info[cid]["FULL_NAME"]=user_name.strip()
    logging.info(f"Received full name for user cid : {cid} name : {user_name.strip()}.")
    user_step.pop(cid)
    print(user_info)

    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(f"{text["phone number"]}",request_contact=True))
    markup.add(KeyboardButton(f"{text["another phone number"]}"))
    markup.add(KeyboardButton(f"{text["I don't want"]}"))
    bot.send_message(cid,f"لطفاً یکی از روش‌های زیر رو برای ارسال شماره موبایل انتخاب کن: 📱",reply_markup=markup)
    logging.info(f"Displayed phone number options for user cid : {cid}.")
    
    user_step[cid]="phone number"
    logging.debug(f"user_info : {user_info} user_step : {user_step} cid : {cid}")
   

@bot.message_handler(func=lambda message : provider_step.get(message.chat.id) == "phone number")
def provider_phone_handler(message):
    
    cid=message.chat.id

    if message.text == f"{text["another phone number"]}":
        
        bot.send_message(cid,"شماره مورد نظر خود را وارد کنید ",reply_markup=hide_board)
        print(provider_info)
        #bot.send_message(cid,"ثبت نام شما با موفقیت انجام شد ✅ \n لطفا مجدد نقش خود را انتخاب کنید",reply_markup=hide_board)
        provider_step[cid] = "another phone number"
        # insert_provider_data(cid,provider_info[cid]["FULL_NAME"],provider_info[cid]["Address"],provider_info[cid]["city"],provider_info[cid]["PHONE"],provider_info[cid]["longitude"],provider_info[cid]["latitude"])
        # logging.info(f"Inserted provider data for cid : {cid}.")
        # provider_step[cid]="login"
        # send_welcome(message)


    provider_info[cid]["PHONE"]=message.text
    print(f"\n{provider_info}\n")
    
    if message.text==f"{text["I don't want"]}":
        provider_info[cid]["PHONE"]=None
        print(provider_info)
        bot.send_message(cid,"هیچ شماره ای انتخاب نشد \n (وارد کردن شماره اجباری هست)",reply_markup=hide_board)
        bot.send_message(cid,"لظفا مجدد تلاش کنید")
        send_welcome(message)
        logging.info(f"Inserted provider data without phone number for cid : {cid}.")

        
    

@bot.message_handler(func=lambda message : user_step.get(message.chat.id)=="phone number")
def user_phone_handler(message):
    
    cid=message.chat.id
    if message.text==f"{text["another phone number"]}":
        bot.send_message(cid,"شماره مورد نظر خود را وارد کنید \n مثال: 9123456789",reply_markup=hide_board)
        print(message.text)
        user_step[cid]="another phone number"
        logging.info(f"Requested another phone number for user cid : {cid}.")
     
    elif message.text==f"{text["I don't want"]}":
        user_info[cid]["PHONE"]=None
        print(user_info)
        
        bot.send_message(cid,"ثبت نام شما با موفقیت انجام شد ✅ \n لطفا مجدد نقش خود را انتخاب کنید",reply_markup=hide_board)
        
        insert_customer_data(cid,user_info[cid]['FULL_NAME'],user_info[cid]['PHONE'],user_info[cid]["SEX"])
        logging.info(f"Inserted customer data without phone number for cid : {cid}.")
        user_step[cid]="login"
        send_welcome(message)


@bot.message_handler(func = lambda message : user_step.get(message.chat.id) == "another phone number")
def another_phone_handler(message):
    cid=message.chat.id
    user_info[cid]["PHONE"]=message.text
    print(f"\n{user_info}\n")
    insert_customer_data(cid,user_info[cid]['FULL_NAME'],user_info[cid]['PHONE'],user_info[cid]["SEX"])
    bot.send_message(cid,"ثبت نام شما با موفقیت انجام شد ✅ \n لطفا مجدد نقش خود را انتخاب کنید",reply_markup=hide_board)
    logging.info(f"Inserted customer data for cid : {cid}.")
    user_step[cid]="login"
    send_welcome(message)


@bot.message_handler(func = lambda message : provider_step.get(message.chat.id) == "provider_city")
def provider_sign_up(message):
    cid=message.chat.id
    print("360@@",message.text)
    try:
        provider_info[cid].setdefault("city",f"{message.text}")
    except Exception as e:
        logging.error(f"Error occurred while setting city for provider cid : {cid} error : {e}")

    logging.debug(f"provider_info : {provider_info}")
    print(provider_info)
    
   # 
    bot.send_message(cid,f"{text["Address"]}",reply_markup=hide_board)
    provider_step[cid]="Address"

    

  
@bot.message_handler(func=lambda message : provider_step.get(message.chat.id) == "Address")
def provider_Address_handler(message):
    cid=message.chat.id

    provider_info[cid]["Address"]=message.text
    Keyboard=ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(cid,f"{text["location"]}")
    provider_step[cid] = "location"


    logging.debug(f"provider_step : {provider_step}")
    print("testtttttttt",provider_step)
    

@bot.message_handler(func=lambda message: provider_step.get(message.chat.id) == "location")
def location_handler(message):
    cid=message.chat.id
    print(message)
    try:
        if message.location_info.latitude:
            logging.info(f"Received location for provider cid : {cid} location : {message.location_info}")
    except:
        logging.warning(f"Location not received for provider cid : {cid}")
        bot.send_message(cid,"لطفا یک لوکیشن ارسال کنید")


@bot.message_handler(func = lambda message: provider_step.get(message.chat.id) == "service_duration")
def service_duration_handler(message):
    print("hiiiiiiiiiii")
    cid=message.chat.id
    logging.debug(f"service_info : {service_info}")
    print(f"testtttttttt         {service_info}")
    
    duration=message.text
    logging.debug(f"insert_service_info : {insert_service_info}")
    print(f"test          {insert_service_info}    testttt")
    if duration=="تمایل ندارم ❌":
        insert_service_info["time"]=None
    else:
        insert_service_info["time"]=duration

    print(f"hooooooo       {insert_service_info}")
    logging.debug(f"insert_service_info : {insert_service_info}")
    bot.send_message(cid,"لطفا مبلغ مورد نظر را وارد کنید (به تومان). 💰",reply_markup=hide_board)


    provider_step[cid]="service_price"

@bot.message_handler(func = lambda message: provider_step.get(message.chat.id) == "another phone number")
def another_phone_handler(message):
    cid=message.chat.id
    provider_info[cid]["PHONE"] = message.text
    insert_provider_data(cid,provider_info[cid]["FULL_NAME"],provider_info[cid]["Address"],provider_info[cid]["city"],provider_info[cid]["PHONE"],provider_info[cid]["longitude"],provider_info[cid]["latitude"])
    logging.info(f"Inserted provider data for cid : {cid}.")
    provider_step[cid]="login"
    send_welcome(message)


@bot.message_handler(func = lambda message: provider_step.get(message.chat.id) == "service_price")
def service_price_handler(message):
    cid=message.chat.id
    price=message.text
    print(insert_service_info)
    insert_service_info["price"]=price
    bot.send_message(cid,"سرویس شما با موفقیت ثبت شد ✅")
    
    print(f"service_info: {insert_service_info}")
    
    try:
        last_id=insert_service_data(insert_service_info["name"],insert_service_info["time"],insert_service_info["price"])
        logging.info(f"Your service has been successfully inserted with id : {last_id}")
        #print(last_id)

    except Exception as e:
        logging.error(f"Error occurred while inserting service data for cid : {cid} error : {e}")

    insert_provider_service_table(cid,last_id)

    insert_service_info.clear()


@bot.message_handler(func = lambda message : provider_step.get(message.chat.id) == "time")
def provider_time_handler(message):
    cid=message.chat.id
    provider_time=message.text.split("\n")
    for time in provider_time:
        start = time.split("-")[0]
        end = time.split("-")[1]
        select_service[cid]["start_time"]=start
        select_service[cid]["end_time"]=end
        print(get_provider_services_row_id(select_service[cid]["service_id"]))

        id_provider_service_table = get_provider_services_row_id(select_service[cid]["service_id"])

        insert_time_table(select_service[cid]["start_time"],select_service[cid]["end_time"],select_service[cid]["date"],id_provider_service_table[0])
    bot.send_message(cid,"✅ زمان‌ شما با موفقیت ثبت شد.")
    logging.info(f"Inserted time for provider cid : {cid} time : {select_service[cid]['start_time']} - {select_service[cid]['end_time']}")
    markup=list_provide_services(cid)
    bot.send_message(cid,"سرویس های شما 👇",reply_markup = markup)
    

    

@bot.message_handler(content_types=["contact"])
def contact_handler(message):
    cid=message.chat.id
    
    print("<<<<<<<<<<<",user_step)
    if user_step.get(cid)=='phone number':
        contact_info = message.contact
        print(contact_info)
        print(contact_info.phone_number)
        if contact_info.user_id == cid:
            bot.send_message(cid,"ثبت نام شما با موفقیت انجام شد ✅ \n لطفا مجدد نقش خود را انتخاب کنید",reply_markup=hide_board)
            
            user_info[cid]["PHONE"]=contact_info.phone_number[2:]
            print(user_info)
            insert_customer_data(cid,user_info[cid]['FULL_NAME'],user_info[cid]['PHONE'],user_info[cid]["SEX"])
            user_step[cid]="login"
            send_welcome(message)
    
        else:
            bot.send_message(cid,"شماره اشتباه است ❌\n لطفا دوباره ارسال کنید ")
            bot.send_location()



    elif provider_step.get(cid)=="phone number":
        contact_info = message.contact
        print(contact_info)
        print(contact_info.phone_number)
        if contact_info.user_id == cid:
           
           bot.send_message(cid,"ثبت نام شما با موفقیت انجام شد ✅ \n لطفا مجدد نقش خود را انتخاب کنید",reply_markup=hide_board)
           provider_info[cid]["PHONE"]=contact_info.phone_number[2:]

           insert_provider_data(cid,provider_info[cid]["FULL_NAME"],provider_info[cid]["Address"],provider_info[cid]["city"],provider_info[cid]["PHONE"],provider_info[cid]["longitude"],provider_info[cid]["latitude"])
           provider_step[cid]="login"

           logging.info(f"Inserted provider data for cid : {cid}")
           logging.debug(f"provider_info : {provider_info[cid]}")
           print(provider_info)
           send_welcome(message)
        
        else:
            bot.send_message(cid,"شماره اشتباه است ❌\n لطفا دوباره ارسال کنید ")

@bot.message_handler(content_types=["location"])
def location(message):
    cid=message.chat.id
    if provider_step.get(cid) == "location":

        location_info=message.location
        longitude=location_info.longitude
        latitude=location_info.latitude
        provider_info[cid]["longitude"]=longitude
        provider_info[cid]["latitude"]=latitude
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton(f"{text["phone number"]}",request_contact=True))
        markup.add(KeyboardButton(f"{text["another phone number"]}"))
        markup.add(KeyboardButton(f"{text["I don't want"]}"))
        provider_step.pop(cid)
        bot.send_message(cid,f"طفاً یکی از روش‌های زیر رو برای ارسال شماره موبایل انتخاب کن. 📱",reply_markup=markup)
        provider_step[cid]="phone number"
        print(location_info)
        print(message.location.latitude)
        print(provider_step)
    else:
        echo_message(message)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()