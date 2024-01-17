{
    "name": "school_app",
    "summary": """Basic School App""",
    "description": """
    """,
    "author": "bizzappdev",
    "website": "http://www.bizzappdev.com",
    "category": "Uncategorized",
    "version": "15.0.1.0.0",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/teacher_menu_views.xml",
        "views/teacher_views.xml",
        "views/course_view.xml",
    ],
    # only loaded in demonstration mode
    # "demo": [
    #     "demo/demo.xml",
    # ],
    "application": True,
    "license": "LGPL-3",
}
