Installation

send Mail
pip install django-smtp-ssl

django rest_framework
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support
pip install django-cors-headers 

Description
    - กำลังทำงานในส่วนของ APScheduler ในการทำ cron
    - ทำส่วนของที่เชื่อมต่อกับ QuarantinePlace & Profile & Home Screen เสร็จแล้ว
    - เหลือดังนี้
        - ทำให้สามารถทำการรัน cron ที่ ทุกๆ 9:00, 12:00, 15:00 18:00, 21:00 เพื่อทำการส่งอีเมล์แจ้งเตือนครั้งที่ 1 ได้
        - ทำให้สามารถทำการรัน cron ที่ ทุกๆ 9:15, 12:15, 15:15 18:15, 21:15 เพื่อทำการส่งอีเมล์แจ้งเตือนครั้งที่ 2 ได้
        - ทำให้สามารถทำการรัน cron ที่ ทุกๆ 9:30, 12:30, 15:30 18:30, 21:30 เพื่อทำการส่งอีเมล์แจ้งระงับสัญญาณได้
        - ทำการเก็บไฟล์ Vector สำหรับทำ Face Recognition