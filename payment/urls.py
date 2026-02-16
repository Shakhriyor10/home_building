from django.urls import path

from payment.views import WorkerList, WorkerCreate, WorkerUpdate, CarList, CarUpdate, OutlayCategoryList, \
    OutlayCategoryUpdate, OutlayUpdate, OutlayCategoryDetail, OutlayPaymentCreateView, OutlayPaymentReturnCreateView, \
    ReportsIncomePaymentsView, ReportsOutcomePaymentsView

urlpatterns = [
    path('workers/', WorkerList.as_view(), name='workers'),
    path('worker_create/', WorkerCreate.as_view(), name='worker_create'),
    path('worker_update/<int:pk>/', WorkerUpdate.as_view(), name='worker_update'),
    path('cars/', CarList.as_view(), name='cars'),
    path('car_update/<int:pk>/', CarUpdate.as_view(), name='car_update'),
    path('outlay_cat/', OutlayCategoryList.as_view(), name='outlay_cat'),
    path('outlay_cat_update/<int:pk>/', OutlayCategoryUpdate.as_view(), name='outlay_cat_update'),
    path('outlay_cat_detail/<int:pk>/', OutlayCategoryDetail.as_view(), name='outlay_cat_detail'),
    path('outlay/', OutlayPaymentCreateView.as_view(), name='outlay'),
    path('outlay_update/<int:pk>', OutlayUpdate.as_view(), name='outlay_update'),
    path('return/outlay/payment/create', OutlayPaymentReturnCreateView.as_view(), name='return_outlay'),
    path('report/income/', ReportsIncomePaymentsView.as_view(), name='report_income'),
    path('report/outcome/', ReportsOutcomePaymentsView.as_view(), name='report-outcome'),
]
