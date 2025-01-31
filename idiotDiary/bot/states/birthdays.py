from idiotDiary.bot.utils.states_factory import FSMSingleFactory

BirthdaysMenuSG = FSMSingleFactory("BirthdaysMenuSG")
ClearBirthdaysSG = FSMSingleFactory("ClearBirthdaysSG")
TimeCorrectionSG = FSMSingleFactory("TimeCorrectionSG")
CalendarSG = FSMSingleFactory("CalendarSG")

BirthdaysNotificationSG = FSMSingleFactory("BirthdaysNotificationSG")
ClearNotificationSG = FSMSingleFactory("ClearNotificationSG")
AddNotificationTimeSG = FSMSingleFactory("AddNotificationTimeSG")
