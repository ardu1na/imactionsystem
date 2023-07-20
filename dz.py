#Static Folder Name
foldername_d = "dashboard" 
foldername_f = "frontend"

dz_array = {
        "public":{
            "favicon":f"{foldername_d}/images/favicon.png",
            "description":"W3CMS  : Django CMS With Dashboard & FrontEnd Template",
            "og_title":"W3CMS  : Django CMS With Dashboard & FrontEnd Template",
            "og_description":"W3CMS  : Django CMS With Dashboard & FrontEnd Template",
            "og_image":"https://w3cms.dexignzone.com/django/social-image.png",
            "title":"W3CMS  : Django CMS With Dashboard & FrontEnd Template",
        },
        "global":{
            "css":[
                    f"{foldername_d}/vendor/jquery-nice-select/css/nice-select.css",
                    f"{foldername_d}/css/style.css"
                ],

            "js":{
                "top":[
                    f"{foldername_d}/vendor/global/global.min.js",
                    f"{foldername_d}/vendor/jquery-nice-select/js/jquery.nice-select.min.js",
                ],
                "bottom":[
                f"{foldername_d}/js/utils.js",
                    f"{foldername_d}/js/custom.js",
                    f"{foldername_d}/js/dlabnav-init.js",

                ]
            },
        },
        "pagelevel":{
            "frontend":{
                "public":{
                    
                    "description":"W3CMS  : Django CMS With Dashboard & FrontEnd Template",
                    "og_title":"W3CMS  : Django CMS With Dashboard & FrontEnd Template",
                    "og_description":"W3CMS  : Django CMS With Dashboard & FrontEnd Template",
                    "og_image":"https://w3cms.dexignzone.com/django/social-image.png",
                    "title":"W3CMS  : Django CMS With Dashboard & FrontEnd Template",
                },
                "global":{
                    "css":{
                        
                        f"{foldername_f}/vendor/aos/aos.css",
                        f"{foldername_f}/vendor/lightgallery/css/lightgallery.min.css",
                        f"{foldername_f}/vendor/magnific-popup/magnific-popup.min.css",
                        f"{foldername_f}/vendor/swiper/swiper-bundle.min.css",
                        # f"{foldername_f}/vendor/animate/animate.css",
                        # f"{foldername_f}/vendor/rangeslider/rangeslider.css",
                        f"{foldername_f}/css/style.css"
                    },
                    
                    "js":{
                        "top":{
                            f"{foldername_f}/js/jquery.min.js",
                            f"{foldername_f}/vendor/bootstrap/js/bootstrap.bundle.min.js",
                        },
                        "bottom":{
                            f"{foldername_f}/vendor/magnific-popup/magnific-popup.js",
                            f"{foldername_f}/vendor/lightgallery/js/lightgallery-all.min.js",
                            f"{foldername_f}/vendor/counter/waypoints-min.js",
                            f"{foldername_f}/vendor/counter/counterup.min.js",
                            f"{foldername_f}/vendor/swiper/swiper-bundle.min.js",
                            
                            f"{foldername_f}/vendor/aos/aos.js",
                            f"{foldername_f}/js/dz.carousel.js",
                            f"{foldername_f}/js/dz.ajax.js",
                            f"{foldername_f}/js/custom.js",
                            f"{foldername_f}/vendor/slider/rangeslider.js",
                            
                        },
                    }

                },
                "css":{
                   

                },
                "js":{

                 
                }
            },
            "dashboard":{
                #AppName
                "dashboard_views":{
                            "css":{
                                "index":[
                                    f"{foldername_d}/vendor/bootstrap-datetimepicker/css/bootstrap-datetimepicker.min.css"
                                ],
                                
                                "activity":[],
                                "profile":[],

                                "permissions":[
                                    f"{foldername_d}/vendor/sweetalert2/dist/sweetalert2.min.css", 
                                ],

                                "users":[
                                    f"{foldername_d}/vendor/sweetalert2/dist/sweetalert2.min.css",    
                                ],
                                "add_user":[
                                    f"{foldername_d}/vendor/bootstrap-daterangepicker/daterangepicker.css",
                                    f"{foldername_d}/vendor/select2/css/select2.min.css",
                                ],
                                "bi":[
                                    f"{foldername_d}/vendor/bootstrap-daterangepicker/daterangepicker.css",
                                    f"{foldername_d}/vendor/select2/css/select2.min.css",
                                ],
                                "edit_user":[
                                    f"{foldername_d}/vendor/bootstrap-daterangepicker/daterangepicker.css",
                                    f"{foldername_d}/vendor/select2/css/select2.min.css",
                                ],
                                "groups_list":[
                                    f"{foldername_d}/vendor/sweetalert2/dist/sweetalert2.min.css",
                                ],
                                "assign_permissions_to_user":[
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/prettify.min.css",
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/src/bootstrap-duallistbox.css",
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/dist/bootstrap-duallistbox.css",
                                ],

                                "group_add":[
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/prettify.min.css",
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/src/bootstrap-duallistbox.css",
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/dist/bootstrap-duallistbox.css",
                                ],


                                "group_edit":[
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/prettify.min.css",
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/src/bootstrap-duallistbox.css",
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/dist/bootstrap-duallistbox.css",
                                ],
                                

                                
                                "clients":[
                                    f"{foldername_d}/vendor/datatables/css/jquery.dataTables.min.css",
                                ],
                                "expenses":[
                                    f"{foldername_d}/vendor/datatables/css/jquery.dataTables.min.css",
                                ],
                                "expenseshistory":[
                                    f"{foldername_d}/vendor/datatables/css/jquery.dataTables.min.css",
                                ],
                                "employees":[
                                    f"{foldername_d}/vendor/datatables/css/jquery.dataTables.min.css",
                                ],
                                "salaries":[
                                    f"{foldername_d}/vendor/datatables/css/jquery.dataTables.min.css",
                                ],
                                "editemployee":[
                                    f"{foldername_d}/vendor/datatables/css/jquery.dataTables.min.css",
                                ],
                                "employeesold":[
                                    f"{foldername_d}/vendor/datatables/css/jquery.dataTables.min.css",
                                ],
                                "editceo":[
                                    f"{foldername_d}/vendor/datatables/css/jquery.dataTables.min.css",
                                ],
                                "ceo":[
                                    f"{foldername_d}/vendor/datatables/css/jquery.dataTables.min.css",
                                ],


                                
                                "app_profile":[
                                    f"{foldername_d}/vendor/lightgallery/css/lightgallery.min.css",
                                    f"{foldername_d}/vendor/magnific-popup/magnific-popup.css"
                                ],
                                
                                "bi":[
                                    f"{foldername_d}/vendor/bootstrap-daterangepicker/daterangepicker.css",
                                    f"{foldername_d}/vendor/clockpicker/css/bootstrap-clockpicker.min.css",
                                    f"{foldername_d}/vendor/jquery-asColorPicker/css/asColorPicker.min.css",
                                    f"{foldername_d}/vendor/bootstrap-material-datetimepicker/css/bootstrap-material-datetimepicker.css",
                                    f"{foldername_d}/vendor/pickadate/themes/default.css",
                                    f"{foldername_d}/vendor/pickadate/themes/default.date.css",
                                ],
                                
                                "sales":[
                                    f"{foldername_d}/vendor/datatables/css/jquery.dataTables.min.css",
                                ],
                                "editemployee":[
                                    f"{foldername_d}/vendor/datatables/css/jquery.dataTables.min.css",
                                ],
                                "adjustment":[
                                    f"{foldername_d}/vendor/datatables/css/jquery.dataTables.min.css",
                                ],
                                "cancellations":[
                                    f"{foldername_d}/vendor/datatables/css/jquery.dataTables.min.css",
                                ],
                                "page_login":[],
                                "page_register":[],
                                "page_forgot_password":[],
                                "page_lock_screen":[],
                                "page_error_400":[],
                                "page_error_403":[],
                                "page_error_404":[],
                                "page_error_500":[],
                                "page_error_503":[],
                                "empty_page":[],
                            },
                            "js":{
                                "index":[
                                    f"{foldername_d}/vendor/chart.js/Chart.bundle.min.js",
                                    f"{foldername_d}/vendor/apexchart/apexchart.js",
                                    f"{foldername_d}/vendor/bootstrap-datetimepicker/js/moment.js",
                                    f"{foldername_d}/vendor/bootstrap-datetimepicker/js/bootstrap-datetimepicker.min.js",
                                    f"{foldername_d}/js/dashboard/dashboard-1.js",
                                ],
                                
                                "activity":[],
                                "profile":[
                                    f"{foldername_d}/vendor/chart.js/Chart.bundle.min.js",
                                    f"{foldername_d}/vendor/apexchart/apexchart.js",
                                    f"{foldername_d}/vendor/peity/jquery.peity.min.js",
                                    f"{foldername_d}/js/dashboard/my-profile.js",
                                ],

                                "permissions":[
                                    f"{foldername_d}/vendor/sweetalert2/dist/sweetalert2.min.js",
                                ],

                                "users":[
                                    f"{foldername_d}/vendor/sweetalert2/dist/sweetalert2.min.js",
                                    f"{foldername_d}/js/modules/users/user_list.js"
                                ],
                                "add_user":[
                                    f"{foldername_d}/vendor/moment/moment.min.js",
                                    f"{foldername_d}/vendor/bootstrap-daterangepicker/daterangepicker.js",
                                    f"{foldername_d}/vendor/select2/js/select2.full.min.js",
                                    f"{foldername_d}/js/plugins-init/select2-init.js"
                                ],
                                "edit_user":[
                                    f"{foldername_d}/vendor/moment/moment.min.js",
                                    f"{foldername_d}/vendor/bootstrap-daterangepicker/daterangepicker.js",
                                    f"{foldername_d}/vendor/select2/js/select2.full.min.js",
                                    f"{foldername_d}/js/plugins-init/select2-init.js"
                                ],
                                "groups_list":[
                                    f"{foldername_d}/vendor/sweetalert2/dist/sweetalert2.min.js",
                                ],
                                "assign_permissions_to_user":[
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/ajax/libs/popper.js/1.12.9/umd/popper.min.js",
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/run_prettify.js",
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/dist/jquery.bootstrap-duallistbox.js",
                                ],
                                "group_add":[
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/ajax/libs/popper.js/1.12.9/umd/popper.min.js",
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/run_prettify.js",
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/dist/jquery.bootstrap-duallistbox.js",
                                ],

                                "group_edit":[
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/ajax/libs/popper.js/1.12.9/umd/popper.min.js",
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/run_prettify.js",
                                    f"{foldername_d}/vendor/bootstrap-duallistbox/dist/jquery.bootstrap-duallistbox.js",
                                ],
                                

                                
                                "bi":[
                                    f"{foldername_d}/vendor/chart.js/Chart.bundle.min.js",
                                    f"{foldername_d}/vendor/apexchart/apexchart.js",
                                    f"{foldername_d}/vendor/peity/jquery.peity.min.js",
                                    f"{foldername_d}/vendor/owl-carousel/owl.carousel.js",
                                    #f"{foldername_d}/js/dashboard/instructor-courses.js",
                                    f"{foldername_d}/js/dlab.carousel.js",
                                ],
                                
                                "clients":[
                                    f"{foldername_d}/vendor/chart.js/Chart.bundle.min.js",
                                    f"{foldername_d}/vendor/apexchart/apexchart.js",
                                    f"{foldername_d}/vendor/datatables/js/jquery.dataTables.min.js",
                                    f"{foldername_d}/js/plugins-init/datatables.init.js",
                                    f"{foldername_d}/vendor/owl-carousel/owl.carousel.js",
                                    f"{foldername_d}/js/dashboard/instructor-student.js",
                                ],
                                "ceo":[
                                    f"{foldername_d}/vendor/chart.js/Chart.bundle.min.js",
                                    f"{foldername_d}/vendor/apexchart/apexchart.js",
                                    f"{foldername_d}/vendor/datatables/js/jquery.dataTables.min.js",
                                    f"{foldername_d}/js/plugins-init/datatables.init.js",
                                    f"{foldername_d}/vendor/owl-carousel/owl.carousel.js",
                                    f"{foldername_d}/js/dashboard/instructor-student.js",
                                ],
                                "employees":[
                                    f"{foldername_d}/vendor/chart.js/Chart.bundle.min.js",
                                    f"{foldername_d}/vendor/apexchart/apexchart.js",
                                    f"{foldername_d}/vendor/datatables/js/jquery.dataTables.min.js",
                                    f"{foldername_d}/js/plugins-init/datatables.init.js",
                                    f"{foldername_d}/vendor/owl-carousel/owl.carousel.js",
                                    f"{foldername_d}/js/dashboard/instructor-student.js",
                                ],
                                 "salaries":[
                                    f"{foldername_d}/vendor/chart.js/Chart.bundle.min.js",
                                    f"{foldername_d}/vendor/apexchart/apexchart.js",
                                    f"{foldername_d}/vendor/datatables/js/jquery.dataTables.min.js",
                                    f"{foldername_d}/js/plugins-init/datatables.init.js",
                                    f"{foldername_d}/vendor/owl-carousel/owl.carousel.js",
                                    f"{foldername_d}/js/dashboard/instructor-student.js",
                                ],
                                 
                                "editceo":[
                                    f"{foldername_d}/vendor/chart.js/Chart.bundle.min.js",
                                    f"{foldername_d}/vendor/apexchart/apexchart.js",
                                    f"{foldername_d}/vendor/datatables/js/jquery.dataTables.min.js",
                                    f"{foldername_d}/js/plugins-init/datatables.init.js",
                                    f"{foldername_d}/vendor/owl-carousel/owl.carousel.js",
                                    f"{foldername_d}/js/dashboard/instructor-student.js",
                                ],
                                "editemployee":[
                                    f"{foldername_d}/vendor/chart.js/Chart.bundle.min.js",
                                    f"{foldername_d}/vendor/apexchart/apexchart.js",
                                    f"{foldername_d}/vendor/datatables/js/jquery.dataTables.min.js",
                                    f"{foldername_d}/js/plugins-init/datatables.init.js",
                                    f"{foldername_d}/vendor/owl-carousel/owl.carousel.js",
                                    f"{foldername_d}/js/dashboard/instructor-student.js",
                                ],
                                "employeesold":[
                                    f"{foldername_d}/vendor/chart.js/Chart.bundle.min.js",
                                    f"{foldername_d}/vendor/apexchart/apexchart.js",
                                    f"{foldername_d}/vendor/datatables/js/jquery.dataTables.min.js",
                                    f"{foldername_d}/js/plugins-init/datatables.init.js",
                                    f"{foldername_d}/vendor/owl-carousel/owl.carousel.js",
                                    f"{foldername_d}/js/dashboard/instructor-student.js",
                                ],
                                "expenses":[
                                    f"{foldername_d}/vendor/chart.js/Chart.bundle.min.js",
                                    f"{foldername_d}/vendor/apexchart/apexchart.js",
                                    f"{foldername_d}/vendor/datatables/js/jquery.dataTables.min.js",
                                    f"{foldername_d}/js/plugins-init/datatables.init.js",
                                    f"{foldername_d}/vendor/owl-carousel/owl.carousel.js",
                                    f"{foldername_d}/js/dashboard/instructor-student.js",
                                ],
                                "expenseshistory":[
                                    f"{foldername_d}/vendor/chart.js/Chart.bundle.min.js",
                                    f"{foldername_d}/vendor/apexchart/apexchart.js",
                                    f"{foldername_d}/vendor/datatables/js/jquery.dataTables.min.js",
                                    f"{foldername_d}/js/plugins-init/datatables.init.js",
                                    f"{foldername_d}/vendor/owl-carousel/owl.carousel.js",
                                    f"{foldername_d}/js/dashboard/instructor-student.js",
                                ],
                                
                                
                                "app_profile":[
                                    f"{foldername_d}/vendor/lightgallery/js/lightgallery-all.min.js",
                                    f"{foldername_d}/vendor/magnific-popup/magnific-popup.js"
                                ],
                                
                            "bi":[
                                f"{foldername_d}/vendor/bootstrap-select/dist/js/bootstrap-select.min.js",
                                f"{foldername_d}/vendor/chart.js/Chart.bundle.min.js",
                                f"{foldername_d}/vendor/apexchart/apexchart.js",
                                f"{foldername_d}/vendor/moment/moment.min.js",
                                f"{foldername_d}/vendor/bootstrap-daterangepicker/daterangepicker.js",
                                f"{foldername_d}/vendor/bootstrap-material-datetimepicker/js/bootstrap-material-datetimepicker.js",
                                f"{foldername_d}/vendor/pickadate/picker.js",
                                f"{foldername_d}/vendor/pickadate/picker.date.js",
                                f"{foldername_d}/js/plugins-init/bs-daterange-picker-init.js",
                                f"{foldername_d}/js/plugins-init/clock-picker-init.js",
                                f"{foldername_d}/js/plugins-init/material-date-picker-init.js",
                                f"{foldername_d}/js/plugins-init/pickadate-init.js",
                            ],
                            
                            "sales":[
                                f"{foldername_d}/vendor/chart.js/Chart.bundle.min.js",
                                f"{foldername_d}/vendor/apexchart/apexchart.js",
                                f"{foldername_d}/vendor/datatables/js/jquery.dataTables.min.js",
                                f"{foldername_d}/js/plugins-init/datatables.init.js",
                            ],
                            "editemployee":[
                                f"{foldername_d}/vendor/chart.js/Chart.bundle.min.js",
                                f"{foldername_d}/vendor/apexchart/apexchart.js",
                                f"{foldername_d}/vendor/datatables/js/jquery.dataTables.min.js",
                                f"{foldername_d}/js/plugins-init/datatables.init.js",
                            ],
                            "adjustment":[
                                f"{foldername_d}/vendor/chart.js/Chart.bundle.min.js",
                                f"{foldername_d}/vendor/apexchart/apexchart.js",
                                f"{foldername_d}/vendor/datatables/js/jquery.dataTables.min.js",
                                f"{foldername_d}/js/plugins-init/datatables.init.js",
                            ],
                             
                            "cancellations":[
                                f"{foldername_d}/vendor/chart.js/Chart.bundle.min.js",
                                f"{foldername_d}/vendor/apexchart/apexchart.js",
                                f"{foldername_d}/vendor/datatables/js/jquery.dataTables.min.js",
                                f"{foldername_d}/js/plugins-init/datatables.init.js",
                            ],
                            "page_login":[],
                            "page_register":[],
                            "page_forgot_password":[],
                            "page_lock_screen":[],
                            "page_error_400":[],
                            "page_error_403":[],
                            "page_error_404":[],
                            "page_error_500":[],
                            "page_error_503":[],
                            "empty_page":[],


                            },
                }
            }
        }


}