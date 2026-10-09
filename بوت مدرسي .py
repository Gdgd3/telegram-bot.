from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram.ext import ConversationHandler
import sqlite3

#==========================
# الكلاسات 🤞🤞🤞
#============================

class student :
	def __init__(self,name,Class,section) :
		self.name=name
		self.Class=Class
		self.section=section
		
	def show_information (self) :
		return f"الاسم : {self.name}\nالصف : {self.Class}\nالشعبة : {self.section}"
		
				
class degree :	
	def __init__ (self,arbic,aslam,manth) :
		self.arbic=arbic
		self.aslam=aslam
		self.manth=manth
	
	
	def show_degree (self) :
		return f"العربي : {self.arbic}\nالرياضيات : {self.manth}\nالإسلامية : {self.aslam} \n المعدل : {self.all}"
				
	
#=====================				
# قاعدة بيانات sqlite3
#=====================


try:
    data = sqlite3.connect("file:studints1.db?mode=rw", uri=True)
    cursor = data.cursor()

except sqlite3.OperationalError:
    print("قاعدة البيانات غير موجودة")



#======================
#تجهيز الازار 🎛️
#==========================
        		        		
				
TOKEN = "8621958807:AAGwSniP60ZQAMesgTUepx3mY9DaV7JRdaA"

 #الازرار 🎛️
 
button_degree = InlineKeyboardButton(
    "درجات الطالب📑",
    callback_data="student_degree"
)

button_information=InlineKeyboardButton(
    "معلومات الطالب👤",
    callback_data="student_information"
)

button_nots=InlineKeyboardButton(
    "الملاحضة والسلوك📝",
    callback_data="studint_nots"
)


hide_button = InlineKeyboardButton(
    "الغيابات🚫",
    callback_data="studint_hide"
)

button_month1=InlineKeyboardButton(
    "الشهر الاول",
    callback_data="month1"
)

button_month2=InlineKeyboardButton(
    "الشهر الثاني",
    callback_data="month2"
)


back_button = InlineKeyboardButton(
    "↩️ رجوع",
    callback_data="back"
)



back_keyboard=[[back_button]]

months_keyboard=[[button_month1,button_month2]]

keyboard = [[button_degree],[button_information],[button_nots],[hide_button]]

reply_markup = InlineKeyboardMarkup(keyboard)
	                  
#دالة ال start
           
async def start(update, context):

    await update.message.reply_text("ادخل الرمز الخاص بالطالب : ")

    return PASSWARD


# دالة الازرار

async def student_code(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "student_degree":
        await query.edit_message_text(
            "اختر",
            reply_markup=InlineKeyboardMarkup(months_keyboard)
        )

    elif query.data == "student_information":
        data=context.user_data.get("studint")
        name =data[2]
        Class =data[3]
        section=data[4]
        
        studint=student(name,Class,section)

        await query.edit_message_text(
        studint.show_information() ,
            reply_markup=InlineKeyboardMarkup(back_keyboard)
        )

    elif query.data == "month1":
        aslam = context.user_data["result"][1]
        math = context.user_data["result"][2]
        arbic = context.user_data["result"][3]
        add=sum([int(aslam),int(math),int(arbic)])
        result=add//3
                       
        results=degree(aslam,math,arbic)
        results.all=result
                
        await query.edit_message_text(
        results.show_degree() ,
            reply_markup=InlineKeyboardMarkup(back_keyboard)
                )
    elif query.data == "studint_nots":
        notess= context.user_data.get("notes")        
        
        text=" "
        for i in notess:
        	text += i[1] + "\n \n"
        
        await query.edit_message_text(
        "سجل الملاحضات 🗒️ \n  \n"
            f" {text}",
            reply_markup=InlineKeyboardMarkup(back_keyboard)
        )        

    elif query.data == "studint_hide":
        hide= context.user_data.get("الغيابات")
        text="\n".join(hide)

        await query.edit_message_text(
            f" {text}",
            reply_markup=InlineKeyboardMarkup(back_keyboard)
        )        


    elif query.data == "month2":
        await query.edit_message_text(
            "قريبا",
            reply_markup=InlineKeyboardMarkup(back_keyboard)
        )

    elif query.data == "back":
        await query.edit_message_text(
            "اختر : ",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# دالة التحقق 🔐

PASSWARD = 1


async def check(update, context):
    passward = update.message.text

    cursor.execute("SELECT * FROM studints WHERE code=?",(passward,))
    
    studint= cursor.fetchone()
		
    if studint:        
        cursor.execute("SELECT * FROM degree WHERE name=?",(studint[2],))
        result=cursor.fetchone()
        
        cursor.execute("SELECT * FROM absences WHERE name=?",(studint[2],))
        absence=cursor.fetchone()
        
        cursor.execute("SELECT * FROM notes WHERE name=?",(studint[2],))
        notes=cursor.fetchall()
        
        
        context.user_data["studint"] = studint
        context.user_data["result"] = result
        context.user_data["absence"] =absence
        context.user_data["notes"] =notes
        
        name=studint[2]
        

        await update.message.reply_text(
            f"سجل الطالب : {name}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return ConversationHandler.END

    else:
        await update.message.reply_text("الرمز غير صحيح ❌")
        return ConversationHandler.END
        
        
async def cancel(update, context):
    await update.message.reply_text("تم إلغاء العملية ❌")
    return ConversationHandler.END                                       

# دالة ال conversation

conversation = ConversationHandler(
    entry_points=[
        CommandHandler("start", start)
    ],

    states={
        PASSWARD: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                check
            )
        ],
    },

    fallbacks=[
        CommandHandler("cancel", cancel)
    ]
)                                                          
    
# تجهيز البوت 🤖

app = Application.builder().token(TOKEN).build()

app.add_handler(conversation)

app.add_handler(CallbackQueryHandler(student_code))


app.run_polling()                    
          
          
          