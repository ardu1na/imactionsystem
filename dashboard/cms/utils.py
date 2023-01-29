import re
from dashboard import setup_config

def nodes_per_page():
    load_config_data = setup_config.loadConfig()
    nodes_per_page =  int(load_config_data['Reading']['nodes_per_page']['value'])
    return nodes_per_page

def slugify(s):
  s = s.lower().strip()
  s = re.sub(r'[^\w\s-]', '', s)
  s = re.sub(r'[\s_-]+', '-', s)
  s = re.sub(r'^-+|-+$', '', s)
  return s

def data_filter(filter_form_data,model_obj):
    title = filter_form_data.get('filter_title')
    status = filter_form_data.get('filter_status')
    date = filter_form_data.get('filter_date')
    filter_data=None

    if title :
        print("I am in page title")
        if filter_data:
            filter_data = filter_data.filter(title__icontains=title)
        else:
            filter_data = model_obj.objects.filter(title__icontains=title)

    if status:
        print("I am in page status")
        if filter_data:
            print("status on filter_data")
            filter_data = filter_data.filter(status__exact=status)
        else:
            print("new filter_data")
            filter_data = model_obj.objects.filter(status__exact=status)

    if date:
        print("I am in page date")
        year = date.split('-')[0]
        month = date.split('-')[1]
        day = date.split('-')[2]

        if filter_data:
            filter_data = filter_data.filter(publish_on__year=year,publish_on__month=month,publish_on__day=day)
        else:
            filter_data = model_obj.objects.filter(publish_on__year=year,publish_on__month=month,publish_on__day=day)
    
    return filter_data

#Data filter for contactus and Subscribers

def data_filter_other(filter_form_data,model_obj):
    name = filter_form_data.get('filter_name')
    email = filter_form_data.get('filter_email')
    phone = filter_form_data.get('filter_phone')
    filter_data=None

    if name :
        if filter_data:
            filter_data = filter_data.filter(name__icontains=name)
        else:
            filter_data = model_obj.objects.filter(name__icontains=name)

    if email:
        if filter_data:
            filter_data = filter_data.filter(email__icontains=email)
        else:
            filter_data = model_obj.objects.filter(email__icontains=email)

    if phone:
        if filter_data:
            filter_data = filter_data.filter(phone__icontains=phone)
        else:
            filter_data = model_obj.objects.filter(phone__icontains=phone)

    return filter_data
    