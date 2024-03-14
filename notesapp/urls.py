from django.urls import path
from . import views

urlpatterns=[path('',views.allnotes,name="allnotes"),
            path('addnote/',views.addnewnote,name='addnewnote'),
            path('addnote/adding/',views.adding,name='adding'),
            path("delete/<int:id>",views.delete,name="delete"),
            path("update/<int:id>",views.update,name="update"),
            path("update/updating/<int:id>",views.updating,name="updating"),
            path("folders/",views.showfolders,name="showfolders"),
            path("folders/openfold/<int:id>",views.openfold,name="openfold"),
            path("folders/openfold/update/<int:id>",views.update,name="update"),
            path("folders/openfold/update/updating/<int:id>",views.updating,name="updating"),
            path("folders/openfold/delete/<int:id>",views.delete,name="delete"),
            path("print/<int:id>",views.prints,name="print"),
             path("print/mailing/<int:id>",views.mailing,name="mailing"),
            ]