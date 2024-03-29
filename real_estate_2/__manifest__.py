{
    'name': "Real Estate 2",
    'description': "Real Estates App",
    'depends': ['base', 'mail'],
    'data': [
        "security/ir.model.access.csv",
        "data/sequnces.xml",
        "wizard/rejection_reason_views.xml",
        "views/real_state_views.xml"
    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
