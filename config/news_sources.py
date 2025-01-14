from pydantic_settings import BaseSettings

NEWS_CATEGORIES = {
    'radiology': {
        'sources': [
            'radiologytoday.net'
            # 'auntminnie.com',
            # 'radiologybusiness.com',
            # 'itnonline.com'
        ],
        'queries': [
            'AI radiology',
            'artificial intelligence imaging',
            'machine learning radiology'
        ]
    },
    'surgery': {
        'sources': [
            'surgicalproductsmag.com',
            'generalsurgerynews.com',
            'surgicaltechnology.net'
        ],
        'queries': [
            'AI surgery',
            'artificial intelligence surgical',
            'robotic surgery AI'
        ]
    },
    'medicine': {
        'sources': [
            'medscape.com',
            'healthcareitnews.com',
            'modernhealthcare.com'
        ],
        'queries': [
            'AI medicine',
            'artificial intelligence healthcare',
            'machine learning medicine'
        ]
    }
}
