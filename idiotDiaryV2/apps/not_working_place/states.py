from aiogram.fsm.state import State, StatesGroup

from common.FSM import FSMSingleFactory

NWPStartFSM = FSMSingleFactory("NWPStartFSM", "main")
VideoNoteFSM = FSMSingleFactory("VideoNoteFSM", "download")
MorphFIOFSM = FSMSingleFactory("MorphFIOFSM", "morph")
INNParserFSM = FSMSingleFactory("INNParserFSM", "parse")
ImagesZipFSM = FSMSingleFactory("ImagesZipFSM", "zip")
VoiceFSM = FSMSingleFactory("VoiceFSM", "convert")
StickersFSM = FSMSingleFactory("StickersFSM", "prepare")
