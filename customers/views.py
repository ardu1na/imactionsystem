"""from django.shortcuts import render
from django.views.generic import ListView

from customers.models import Client
from sales.models import Sale

class ClientsRR(ListView):
    def get (self, request, *args, **kwargs):

        clients = Client.objects.all()
        
        tier_1=[]
        tier_2=[]
        tier_3=[]
        tier_4=[]
        tier_5=[]
        for client in clients:
            if client.tier:
                if client.tier == "I":
                    tier_1.append(client)
                elif client.tier == "II":
                    tier_2.append(client)
                elif client.tier == "III":
                    tier_3.append(client)
                elif client.tier == "IV":
                    tier_4.append(client)
                else:
                    tier_5.append(client)    
            else: pass

        t1=len(tier_1)
        t2=len(tier_2)
        t3=len(tier_3)
        t4=len(tier_4)
        t5=len(tier_5)

        get_clients_by_tier = [t1, t2, t3, t4, t5]
        
        sales=Sale.objects.all()

        s_seo = 0
        s_gads= 0
        s_fads= 0
        s_lin= 0
        s_cm = 0
        s_combo = 0
        s_webp = 0
        

        for sale in sales:
            if sale.service == "SEO":
                s_seo += int(sale.price)
            elif sale.service == "Google Ads":
                s_gads += int(sale.price)
            elif sale.service == "Facebook Ads":
                s_fads += int(sale.price)
            elif sale.service == "LinkedIn":
                s_lin  += int(sale.price)
            elif sale.service == "Community Management":
                s_cm  += int(sale.price)
            elif sale.service == "COMBO":
                s_combo  += int(sale.price)
            elif sale.service == "Web Plan":
                s_webp += int(sale.price)
            else: pass

        get_incomes_by_service = [s_seo, s_gads, s_fads, s_lin, s_cm, s_combo, s_webp]

        t1=0
        t2=0
        t3=0
        t4=0
        t5=0

        for sale in sales:
            if sale.account.tier == "I":
                t1 += int(sale.price)
            elif sale.account.tier == "II":
                t2 += int(sale.price)
            elif sale.account.tier == "III":
                t3 += int(sale.price)
            elif sale.account.tier == "IV":
                t4 += int(sale.price)
            elif sale.account.tier == "V":
                t5 += int(sale.price)
            else: pass
        get_incomes_by_tier = [t1, t2, t3, t4, t5]
        
        rr_total= t1+t2+t3+t4+t5
        
        context = {
            'clients' : clients,
            'get_clients_by_tier' : get_clients_by_tier,
            'get_incomes_by_service' : get_incomes_by_service,
            'get_incomes_by_tier' : get_incomes_by_tier,
            'rr_total' : rr_total
            }

        return render(request, 'dashboard/cms/rr.html', context)"""