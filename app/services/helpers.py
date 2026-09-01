import math

from app.services.llm_services import LLMServices
from app.enums import Audience, Tone
from app.core.config import settings

CONVERSATIONS = {}

def get_conversation(conversation_id: str) -> list:
    return CONVERSATIONS.get(conversation_id, [])

def reset_conversations(conversation_id:str):
    if conversation_id in CONVERSATIONS:
        CONVERSATIONS.pop(conversation_id)

def store_conversations(conversation:dict, conversation_id:str):
    #check total conversation threads
    if len(CONVERSATIONS) >= settings.MAX_CONVERSATION_THREAD_COUNT:
        # get the key to delete. don't consider current thread if it is present in the set
        if conversation_id in CONVERSATIONS:
            key = list(set(CONVERSATIONS.keys()) - {conversation_id})[0]
        else:
            key = list(CONVERSATIONS.keys())[0]
        CONVERSATIONS.pop(key)
    print(f"CONVERSATIONS : {CONVERSATIONS}")
    #check total messages in a thread
    if conversation_id not in CONVERSATIONS:
        CONVERSATIONS[conversation_id] = []
    CONVERSATIONS[conversation_id].append(conversation)
    if len(CONVERSATIONS[conversation_id]) >= settings.MAX_CONVERSATION_LENGTH:
        # delete first 2 converations for particular conversation_id(thread) in CONVERSATIONS
        CONVERSATIONS[conversation_id].pop(0)
        CONVERSATIONS[conversation_id].pop(0)
    
    return CONVERSATIONS[conversation_id]

def get_role(tone:str, audience:str)->str:
    tone = Tone(tone)
    audience = Audience(audience)
    if(tone in [Tone.TECHNICAL,Tone.PROFESSIONAL] and audience in (Audience.DEVELOPER,Audience.BACKEND_ENGINEER)):
        return "technical"
    elif(tone == Tone.FRIENDLY and audience == Audience.BEGINNER):
        return "friendly professional"
    elif(tone == Tone.CONCISE and audience == Audience.EXECUTIVE):
        return "executive professional"
    elif(tone in [Tone.TECHNICAL,Tone.PROFESSIONAL] and audience in (Audience.CEO,Audience.CTO,Audience.FOUNDER,Audience.ENTREPRENEUR,Audience.C_SUITE)):
        return "Executive professional"
    else:
        return "professional"


def get_domain(audience:str)->str:
    audience = Audience(audience)

    if audience == Audience.EXECUTIVE:
        return "business"
    elif audience == Audience.BEGINNER:
        return "general"
    elif audience == Audience.DEVELOPER:
        return "computer science"
    elif audience == Audience.BACKEND_ENGINEER:
        return "Backend engineering"
    else:
        return "general"


def get_file_name(file_path:str)->str:
    file_name = file_path.split("/")[-1]
    return file_name
    
    