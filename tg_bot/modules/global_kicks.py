import html
from typing import List, Optional

from telegram import Message, Update, Bot, User, Chat, ParseMode
from telegram.error import BadRequest, TelegramError
from telegram.ext import run_async, CommandHandler, MessageHandler, Filters
from telegram.utils.helpers import mention_html

from tg_bot import dispatcher, CallbackContext, OWNER_ID, DEV_USERS, SUDO_USERS, SUPPORT_USERS
from tg_bot.modules.helper_funcs.chat_status import user_admin, is_user_admin, support_plus
from tg_bot.modules.helper_funcs.extraction import extract_user, extract_user_and_text
from tg_bot.modules.helper_funcs.filters import CustomFilters
from tg_bot.modules.helper_funcs.misc import send_to_list
from tg_bot.modules.sql.users_sql import get_user_com_chats
import tg_bot.modules.sql.global_kicks_sql as sql

GKICK_ERRORS = {
    "User is an administrator of the chat",
    "Chat not found",
    "Not enough rights to restrict/unrestrict chat member",
    "User_not_participant",
    "Peer_id_invalid",
    "Group chat was deactivated",
    "Need to be inviter of a user to kick it from a basic group",
    "Chat_admin_required",
    "Only the creator of a basic group can kick group administrators",
    "Channel_private",
    "Not in the chat",
    "Method is available for supergroup and channel chats only",
    "Reply message not found",
    "Bots can't add new chat members",
    "Can't demote chat creator",
    "Method is available only for supergroups",
    "Can't remove chat owner",
    "User not found",
}


@support_plus
def gkick(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    message = update.effective_message

    user_id = extract_user(message, args)
    sender_id = update.effective_user.id
    try:
        user_chat = bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message in GKICK_ERRORS:
            pass
        else:
            message.reply_text(
                "User cannot be Globally kicked because: {}".format(
                    excp.message))
            return
    except TelegramError:
        pass

    if not user_id:
        message.reply_text("You do not seems to be referring to a user")
        return

    if user_id == sender_id:
        message.reply_text("No. You're not going to gkick yourself.")
        return
    elif int(user_id) == OWNER_ID:
        message.reply_text(
            "Wow! Someone's so noob that he want to gkick my owner! *Grabs Potato Chips*"
        )
        return

    if user_id == sender_id:
        message.reply_text("No. You're not going to gkick yourself.")
        return
    elif int(user_id) in DEV_USERS:
        message.reply_text("OOOF! Try again later XoXo >.<")
        return

    if user_id == sender_id:
        message.reply_text("No. You're not going to gkick yourself.")
        return
    elif int(user_id) in SUDO_USERS:
        message.reply_text(
            "I spy, with my little eye... a sudo user war! Why are you guys turning on each other?"
        )
        return

    if user_id == sender_id:
        message.reply_text("No. You're not going to gkick yourself.")
        return
    elif int(user_id) in SUPPORT_USERS:
        message.reply_text(
            "OOOH someone's trying to gkick a support user! *grabs popcorn*")
        return

    if user_id == bot.id:
        message.reply_text(
            "-_- So funny, lets gkick myself why don't I? Nice try.")
        return

    message.reply_text("*Snaps with fingers* 😉")

    chats = get_user_com_chats(user_id)
    kicker = update.effective_user  # type: Optional[User]
    send_to_list(bot, SUDO_USERS + SUPPORT_USERS,
                 "<b>Global Kick</b>" \
                 "\n#GKICK" \
                 "\n<b>Status:</b> <code>Enforcing</code>" \
                 "\n<b>Sudo Admin:</b> {}" \
                 "\n<b>User:</b> {}" \
                 "\n<b>ID:</b> <code>{}</code>".format(mention_html(kicker.id, kicker.first_name),
                                                       mention_html(user_chat.id, user_chat.first_name),
                                                                    user_chat.id),
                html=True)

    message.reply_text(
        "Done! Gkicked.\n<b>ID:</b> <code>{}</code>".format(user_id),
        parse_mode=ParseMode.HTML)
    for chat in chats:
        try:
            bot.unban_chat_member(chat.chat_id, user_id)
        except BadRequest as excp:
            if excp.message in GKICK_ERRORS:
                pass
            else:
                message.reply_text(
                    "User cannot be Globally kicked because: {}".format(
                        excp.message))
                return
        except TelegramError:
            pass


@support_plus
def gkickset(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    message = update.effective_message
    user_id, value = extract_user_and_text(message, args)
    try:
        user_chat = bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message in GKICK_ERRORS:
            pass
        else:
            message.reply_text("GENERIC ERROR: {}".format(excp.message))
    except TelegramError:
        pass

    if not user_id:
        message.reply_text("You do not seems to be referring to a user")
        return

    if int(user_id) in SUDO_USERS or int(user_id) in SUPPORT_USERS:
        message.reply_text("SUDOER: Irrelevant")
        return

    if int(user_id) == OWNER_ID:
        message.reply_text("OWNER: Irrelevant")
        return

    if user_id == bot.id:
        message.reply_text("It's me, nigga")
        return

    sql.gkick_setvalue(user_id, user_chat.username, int(value))
    return


@support_plus
def gkickreset(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    message = update.effective_message
    user_id, value = extract_user_and_text(message, args)
    try:
        user_chat = bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message in GKICK_ERRORS:
            pass
        else:
            message.reply_text("GENERIC ERROR: {}".format(excp.message))
    except TelegramError:
        pass

    if not user_id:
        message.reply_text("You do not seems to be referring to a user")
        return

    if int(user_id) in SUDO_USERS or int(user_id) in SUPPORT_USERS:
        message.reply_text("SUDOER: Irrelevant")
        return

    if int(user_id) == OWNER_ID:
        message.reply_text("OWNER: Irrelevant")
        return

    if user_id == bot.id:
        message.reply_text("It's me, nigga")
        return

    sql.gkick_reset(user_id)
    return


def __user_info__(user_id):
    times = sql.get_times(user_id)

    text = "<b>Globally Kicked</b>: {}"
    if times != 0:
        text = text.format(
            "<code>Yes</code> (Times: <code>{}</code>)".format(times))
    else:
        text = text.format("<code>No</code>")

    return text


GKICK_HANDLER = CommandHandler("gkick",
                               gkick,
                               run_async=True)
SET_HANDLER = CommandHandler("gkickset",
                             gkickset,
                             run_async=True)
RESET_HANDLER = CommandHandler("gkickreset",
                               gkickreset,
                               run_async=True)

dispatcher.add_handler(GKICK_HANDLER)
dispatcher.add_handler(SET_HANDLER)
dispatcher.add_handler(RESET_HANDLER)
