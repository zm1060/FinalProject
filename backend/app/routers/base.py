'''API base router
'''
from fastapi import APIRouter

router = APIRouter()


@router.get('/health')
def health():
    '''Health check
    '''
    return {
        'name': "Eyes",
        'version':"0.0.1",
    }
