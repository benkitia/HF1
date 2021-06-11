import os

class Config:
    staff_roles = [
        663903105133576202
    ]
    admin_roles = [
        429849578326589441
    ]
    
    private_inf_log = 449336282511048721
    public_inf_log = 845914504990556201
    user_log = 707867871765594142

    embed_colors = {
        "positive" : 0x43C759,
        "negative" : 0xF53B30,
        "log_join" : 0x197AFF,
        "log_leave" : 0xFCCC00,
        "log_name" : 0x5AC8FA,
        "log_message_edit" : 0xF89502,
        "log_message_delete" : 0xF52C56,
        "log_infraction" : 0xF53B30
    }

    log_icon_urls = {
        "ban" : "https://hair-force-one.s3.us-east-2.amazonaws.com/infraction-logging-thumbnails/ban.png",
        "kick" : "https://hair-force-one.s3.us-east-2.amazonaws.com/infraction-logging-thumbnails/kick.png",
        "mute" : "https://hair-force-one.s3.us-east-2.amazonaws.com/infraction-logging-thumbnails/mute.png",
        "warning" : "https://hair-force-one.s3.us-east-2.amazonaws.com/infraction-logging-thumbnails/warn.png",
        "unmute" : "https://hair-force-one.s3.us-east-2.amazonaws.com/infraction-logging-thumbnails/unmute.png",
        "unban" : "https://hair-force-one.s3.us-east-2.amazonaws.com/infraction-logging-thumbnails/unban.png"
    }

    photo_of_the_week_channel = 844261014630694942

    mute_role = 410604540568666132
    auto_dehoist = True