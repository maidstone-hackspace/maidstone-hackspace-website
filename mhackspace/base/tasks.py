import requests
from celery import shared_task
from django.conf import settings
from mhackspace.feeds.helper import import_feeds


@shared_task
def update_homepage_feeds():
    import_feeds()
    return {'result': 'Homepage feeds imported'}

matrix_url = "https://matrix.org/_matrix/client/r0"
matrix_login_url = matrix_url + "/login"
matrix_join_room_alias_url = matrix_url + "/join/{room}?access_token={access_token}"
matrix_join_room_id_url = matrix_url + "rooms/%21{room}/join?access_token={access_token}"
matrix_send_msg_url = matrix_url + "/rooms/%21{room}/send/m.room.message?access_token={access_token}"


@shared_task
def send_email(email_to,
               message,
               email_from='no-reply@maidstone-hackspace.org.uk',
               reply_to='no-reply@maidstone-hackspace.org.uk'):

    if settings.EMAIL_NOTIFY is False:
        return
    email = EmailMessage(
        '[%s] - %s' % (settings.MSG_PREFIX, instance.topic.title),
        'A topic you have interacted with has been updated click link to see new comments %s' % instance.get_absolute_url(),
        'no-reply@maidstone-hackspace.org.uk',
        to=[email_to],
        headers={'Reply-To': 'no-reply@maidstone-hackspace.org.uk'})
    email.send()
    return {'result', 'Email sent to %s' % email_to}

@shared_task
def matrix_message(message, prefix=''):
    # we dont rely on theses, so ignore if it goes wrong
    # TODO at least log that something has gone wrong
    try:
        # login
        details = {
            "type":"m.login.password",
            "user":settings.MATRIX_USER,
            "password":settings.MATRIX_PASSWORD}
        r0 = requests.post(matrix_login_url, json = details)
        access_token = r0.json().get('access_token')

        # join room by id
        url_params = {
            'room': settings.MATRIX_ROOM,
            'access_token': access_token}
        url = matrix_join_room_id_url.format(**url_params)
        r1 = requests.post(url)

        # send message
        url_params = {
            "room": settings.MATRIX_ROOM,
            "access_token": access_token}
        url = matrix_send_msg_url.format(**url_params)
        details = {
            "msgtype": "m.text",
            "body": "[%s%s] %s" % (settings.MSG_PREFIX, prefix, message)}
        r2 = requests.post(url, json=details)
    except:
        pass
    return {'result', 'Matrix message sent successfully'}
