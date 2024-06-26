from common.FSM import FSMSingleFactory

BirthdaysFSM = FSMSingleFactory("BirthdaysFSM", "main")
ClearBirthdaysFSM = FSMSingleFactory("ClearBirthdaysFSM", "clear_confirm")
TimeCorrectionFSM = FSMSingleFactory("TimeCorrectionFSM", "start")
CalendarFSM = FSMSingleFactory("CalendarFSM", "main")

BirthdaysNotificationFSM = FSMSingleFactory("BirthdaysNotificationFSM", "main")
ClearNotificationFSM = FSMSingleFactory("ClearNotificationFSM", "clear")
AddNotificationTimeFSM = FSMSingleFactory("AddNotificationTimeFSM", "add_time")
