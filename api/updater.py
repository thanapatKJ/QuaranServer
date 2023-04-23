# from apscheduler.schedulers.background import BackgroundScheduler
# from .cronjobs import  end_quarantine, send_email_check, send_email_inactive, send_email_warning, end_quarantine


# def start():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(send_email_check, 'cron', hour=9,minute=0)
#     scheduler.add_job(send_email_check, 'cron', hour=12,minute=0)
#     scheduler.add_job(send_email_check, 'cron', hour=15,minute=0)
#     scheduler.add_job(send_email_check, 'cron', hour=18,minute=0)
#     scheduler.add_job(send_email_check, 'cron', hour=21,minute=0)

#     scheduler.add_job(send_email_warning, 'cron', hour=9,minute=15)
#     scheduler.add_job(send_email_warning, 'cron', hour=12,minute=15)
#     scheduler.add_job(send_email_warning, 'cron', hour=15,minute=15)
#     scheduler.add_job(send_email_warning, 'cron', hour=18,minute=15)
#     scheduler.add_job(send_email_warning, 'cron', hour=21,minute=15)
    
#     scheduler.add_job(send_email_inactive, 'cron', hour=9,minute=30)
#     scheduler.add_job(send_email_inactive, 'cron', hour=12,minute=30)
#     scheduler.add_job(send_email_inactive, 'cron', hour=15,minute=30)
#     scheduler.add_job(send_email_inactive, 'cron', hour=18,minute=30)
#     scheduler.add_job(send_email_inactive, 'cron', hour=21,minute=30)

#     # scheduler.add_job(end_quarantine, 'cron', hour=15,minute=47)
#     scheduler.add_job(end_quarantine, 'cron', hour=0,minute=0)

#     # scheduler.add_job(send_email_check, 'cron', hour=23,minute=56)
#     # scheduler.add_job(send_email_warning, 'cron', hour=23,minute=57)
#     # scheduler.add_job(send_email_inactive, 'cron', hour=23,minute=58)

#     scheduler.start()