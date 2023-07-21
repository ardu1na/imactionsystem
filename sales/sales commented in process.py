
class Sale(models.Model):


    @property
    def get_comm_per(self):
        
        if self.change >= comms.rr_1:
            ## obtener el porcentaje de comisiones por venta para los empleados vendedores
            if self.revenue == "OneOff":
                return comms.one_off
            else:    
                if self.kind == "Upsell":
                    return comms.up_sell
                else:
                    # el porcentaje de comisión de las ventas rr q no son upsell varian según parámetros configurados x el usuario
                    # se obtienen de dashboard.comms pk=1
                    if self.change >= comms.rr_1 and self.change < comms.rr_2:
                        return comms.com_rr_1
                    elif self.change >= comms.rr_2 and self.change < comms.rr_3:
                        return comms.com_rr_2
                    elif self.change >= comms.rr_3 and self.change < comms.rr_4:
                        return comms.com_rr_3
                    elif self.change >= comms.rr_4 and self.change < comms.rr_5:
                        return comms.com_rr_4
                    elif self.change >= comms.rr_5:
                        return comms.com_rr_5
            
    @property
    def get_comm(self):
        # obtener el valor de la comisión según el precio de la venta y el prcjje
        try:
            comm = (self.get_comm_per * self.change)/100
            return comm
        # si la venta es menor a comms.rr_1 retornar 0 comisión
        except:
            return 0
        
    

    UPSELL='Upsell'
    NEW_CLIENT='New Client'
    CROSSSELL = 'Cross Sell'
    NEW = ' - '
    KIND_CHOICES = (
        (UPSELL, ('Upsell')),
        (NEW_CLIENT, ('New Client')),
        (CROSSSELL, ('Cross Sell')),
        (NEW, (' - ')))

    P = "P"
    FCD = "FCD"
    FC = "FC"
    S_CHOICES=(
        (P, ("P")),
        (FCD, ("FCD")),
        (FC, ("FC")),)

    SEO ='SEO'
    GADS = 'Google Ads'
    FADS = 'Facebook Ads'
    DW = 'Web Design'
    HO = 'Hosting'
    LIKD = 'LinkedIn'
    SSL = 'SSL certificate'
    WEB_PLAN = 'Web Plan'
    COMBO = 'Combo'
    CM = 'Community Management'
    EMKTG = 'Email Marketing'
    OTHER = 'Others'
    OTHER_RR = 'Others RR'
    SERVICE_CHOICES = (
        (SEO, ('SEO')),
        (GADS, ('Google Ads')),
        (FADS, ('Facebook Ads')),
        (LIKD, ('LinkedIn')),
        (CM, ('Community Management')),
        (WEB_PLAN, ('Web Plan')),
        (COMBO, ('Combo')),
        (DW, ('Web Design')),
        (HO, ('Hosting')),
        (SSL, ('SSL certificate')),
        (OTHER, ('Others')),
        (OTHER_RR, ('Others RR')),

    )
       
    ARS = "ARS"
    USD = "USD"
    COIN_CHOICES = (
        (ARS, ('ARS')),
        (USD, ('USD')))

    client = models.ForeignKey(Client, related_name='sales', null=True, blank=True, on_delete=models.CASCADE, verbose_name="ACCOUNT")
    
    sales_rep = models.ForeignKey(
                    Employee,
                    related_name='sales',
                    null=True, blank=True,
                    on_delete=models.SET_NULL, verbose_name="SALES REP")
    
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, verbose_name="SERVICE", blank=False, default=None)

    suscription = models.ForeignKey(Service, related_name="sales", on_delete=models.CASCADE, null=True, blank=True)
    
    kind = models.CharField(max_length=50, choices=KIND_CHOICES, null=True, blank=False, default=None, verbose_name="KIND")
    
    date = models.DateField(default=date.today, verbose_name="DATE")
    
    total = models.IntegerField(blank=True, null=True, verbose_name="TOTAL")
    
    comments =models.CharField(max_length=500, null=True, blank=True, verbose_name="COMMENTS")
  
    
    note = models.CharField(max_length=400, null=True, blank=True, verbose_name="NOTES")
    cost = models.IntegerField(default=0, verbose_name="COST")
    status = models.CharField(max_length=5, choices=S_CHOICES, null=True, blank=False, default=None, verbose_name="STATUS $")
    
    
    price = models.DecimalField(default=0, verbose_name="PRICE", decimal_places=2, max_digits=12)
    currency = models.CharField(max_length=50, default="ARS", choices=COIN_CHOICES, null=True, blank=False, verbose_name="CURRENCY")
    
    change = models.DecimalField(default=0, verbose_name="CHANGE", decimal_places=2, max_digits=12, null=True, blank=True)
    
    @property
    def get_change(self):
        change = 0
        if self.currency == "USD":
            change = self.price*Decimal(blue)
            return change
        else:
            return self.price
        
    RR = 'RR'
    OneOff = 'OneOff'
    REVENUE_CHOICES=(
        (RR, ("RR")),
        (OneOff, ("OneOff")),)
    revenue = models.CharField(max_length=20, null=True, blank=False, default=None, choices=REVENUE_CHOICES, help_text="Leave blank to automatically fill", verbose_name="REVENUE")
    # check the service and get the revenue type
    def get_revenue(self):
        if self.service == 'SEO' or self.service == 'Google Ads' or self.service == 'Community Management' \
        or self.service == 'Facebook Ads' or self.service == 'Web Plan' or self.service == 'LinkedIn' \
        or self.service == 'Combo' or self.service == 'Others RR':
            return ("RR")
        else:
            return ("OneOff") 
    

    ###################
    ## service sale auto relation 
    def get_service_or_update (self, *args, **kwargs):  
                
        try:
            service = Service.objects.get(
                client=self.client, service=self.service) 
               
            if not self.suscription:                
                service.total += Decimal(self.change)
                service.save()     
                self.suscription=service                              
            
        except Service.DoesNotExist:                  
            
            values = {
                "client": self.client,
                "service": self.service,
                "total": self.change,
                }            
            service = Service(**values)
            service.save()  
            self.suscription=service
    
    def save(self, *args, **kwargs):                                    


        self.change = self.get_change
        self.revenue = self.get_revenue()


        if self.suscription is None and self.revenue == "RR":
                    
            self.get_service_or_update()
            

        super(Sale, self).save(*args, **kwargs)

        
    
    def __str__(self):
       return '{} - {} '.format(self.client, self.service)

    class Meta:
        ordering = ['-date']
        
        
    ##### custom methods as properties to display in templates or use in functions
    
    @property
    def total(self):
        result = self.price - self.cost
        return '${:,}'.format(result)


    @property
    def price_service(self):
        return "$%s" % self.price if self.price else ""

    @property
    def cost_service(self):
        return "$%s" % self.cost if self.cost else "$0"

   
    @property
    def get_date(self):
        formatdate = self.date.strftime('%d/%m/%Y')
        return formatdate
    
    @property
    def get_date_can(self):
        formatdate = self.date_can.strftime('%d/%m/%Y')
        return formatdate
        
        
            
      
    
    
                
    
    
    
                        
                    

            
        


   

    
        
        