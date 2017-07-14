# coding=utf-8
from django.http import HttpResponse
import simplejson as json
from core.models import VerityCodeType
from django.core.mail import EmailMessage


json_response = lambda x: HttpResponse(
    json.dumps(x, ensure_ascii=False),
    content_type='application/json; charset=utf-8')


def send_mail(request, user, mail_type, **kwargs):
    code = kwargs['code']
    if mail_type == VerityCodeType.ACTIVE_ACCOUNT:  # 账户激活
        subject = u'账号激活'
        # TODO 是否需要传入user? >> 需要
        url = request.build_absolute_uri('/account/active_account/?code=%s' % (code,))
        body = u"请点击下面的链接激活您的账号。此链接将在24小时后失效，请您尽快完成激活。<br/>"
        body += u'<a href="%s">%s</a><br>' % (url, url)
        body += u"(如果无法点击该URL链接地址，请将它复制并粘帖到浏览器的地址输入框，然后单击回车即可。)"
    elif mail_type == VerityCodeType.FORGET_PWD:
        subject = u'忘记密码'
        url = request.build_absolute_uri('/account/reset_pwd/?code=%s' % (code,))
        body = u"请点击下面的链接重置您的账号密码。此链接将在24小时后失效，请您尽快完成激活。<br/>"
        body += u'<a href="%s">%s</a><br>' % (url, url)
        body += u"(如果无法点击该URL链接地址，请将它复制并粘帖到浏览器的地址输入框，然后单击回车即可。)"
    # elif mail_type == VerityCodeType.RESET_PWD:
    #     subject = u'忘记密码'
    #     url = request.build_absolute_uri('/account/reset_pwd/?code=%s' % (code, user,
    #                                                                                              user_type))
    #     body = u"请点击下面的链接重置您的账号密码。此链接将在24小时后失效，请您尽快完成激活。<br/>"
    #     body += u'<a href="%s">%s</a><br>' % (url, url)
    #     body += u"(如果无法点击该URL链接地址，请将它复制并粘帖到浏览器的地址输入框，然后单击回车即可。)"

    # else:
    #     subject = u'变更邮箱'
    #     url = request.build_absolute_uri('/account/confirm/?code=%s' % code)
    #     body = u"请点击下面的链接变更您的邮箱。此链接将在24小时后失效，请您尽快完成激活。<br/>"
    #     body += u'<a href="%s">%s</a><br>' % (url, url)
    #     body += u"(如果无法点击该URL链接地址，请将它复制并粘帖到浏览器的地址输入框，然后单击回车即可。)"

    to = kwargs.get('to')
    # TODO from_email 申请一个测试, 是否需要配置 邮箱密码
    msg = EmailMessage(subject, body, to=[user.email if to is None else to])
    msg.content_subtype = 'html'
    try:
        msg.send()
    except Exception, e:
        print(str(e))
        # TODO raise 错误 如何 custom一个errror
        raise StandardError
    return True