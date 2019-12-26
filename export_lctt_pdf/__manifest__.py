{
    'name': 'Export lctt Info in Pdf',
    'version': '0.2',
    'category': 'LcTt',
    'license': "AGPL-3",
    'author': 'Itech reosurces',
    'company': 'ItechResources',
    'depends': [
                'base',
                'purchase',

                'account',
                ],
    'data': [
            'views/wizard_view.xml',
            'views/lctt_report.xml'

            ],
    'installable': True,
    'auto_install': False,
}
