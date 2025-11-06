from fastapi import HTTPException, status
from .extract_pdf_data import extract_pdf_data
from .extract_doc_data import extract_doc_data
from .extract_ppt_data import extract_ppt_data
from .extract_xls_data import extract_xls_data
from .extract_txt_data import extract_txt_data
from .extract_img_data import extract_img_data

def extract_file_data(file_bytes: bytes, extension: str):
    ext = extension.lower()
    results = None

    try:
        if ext in ['.pdf']:
            results = extract_pdf_data(file_bytes)
        elif ext in ['.doc', '.docx']:
            results = extract_doc_data(file_bytes)
        elif ext in ['.ppt', '.pptx']:
            results = extract_ppt_data(file_bytes)
        elif ext in ['.xls', '.xlsx']:
            results = extract_xls_data(file_bytes)
        elif ext in ['.txt', '.md', '.csv', '.tsv']:
            results = extract_txt_data(file_bytes)
        elif ext in ['.jpg', '.jpeg', '.png', '.webp', '.jp2']:
            results = extract_img_data(file_bytes)
        else:
            results = extract_txt_data(file_bytes)
        
#############################################################
#############################################################
#############################################################    
###                                                       ###    
###        print(                                         ###
###            '\n\n\n \n\n\n \n\n\n',                    ###
###            ext, '\n\n',                               ###
###            results,                                   ###
###            '\n\n\n \n\n\n \n\n\n'                     ###
###        )                                              ###
###                                                       ###
#############################################################
#############################################################
#############################################################
###                                                       ###
###        raise HTTPException(                           ###
###            status_code=status.HTTP_400_BAD_REQUEST,   ###
###            detail='File type is not allowed'          ###
###        )                                              ###
###                                                       ###
#############################################################
#############################################################
#############################################################

        return results
        
    except Exception as e:
        print(f"Error processing file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error processing file: {str(e)}'
        )