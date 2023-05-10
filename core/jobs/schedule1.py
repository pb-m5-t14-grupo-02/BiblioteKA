from datetime import timedelta
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from books.models import BookLoan
from users.models import User
import ipdb

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


def change_user_suspension_status(user_id):
    user = User.objects.get(id=user_id)
    user.is_suspended = False
    user.save()


def check_user_loan_status():
    print("start day routine check")
    users = User.objects.filter(is_suspended=True)
    if users.count():
        for user in users:
            loans = BookLoan.objects.filter(user=user, returned=False)
            if loans.count() > 0:
                for loan in loans:
                    if loan.return_date < timezone.now():
                        user = loan.user
                        user.is_suspended = True
                        user.save()
                        print("chegou até esse ponto")
            else:
                print("chegou01")
                if (
                    not BookLoan.objects.filter(
                        user=user, returned=False, return_date__lt=timezone.now()
                    ).exists()
                    and user.is_suspended
                ):
                    scheduler.add_job(
                        func=change_user_suspension_status,
                        trigger="date",
                        run_date=timezone.now() + timedelta(days=3),
                        id=f"change_user_suspension_status_{user.id}",
                        args=[user.id],
                    )
                    user.suspension_end_date = timezone.now() + timedelta(days=3)
                    user.save()
    print("day routine check ended")


scheduler.add_job(
    check_user_loan_status,
    trigger=IntervalTrigger(days=1),
    id="check_user_loan_status",
    name="check user loan status",
    replace_existing=True,
)

scheduler.start()
