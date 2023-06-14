import cv2
import pytesseract
import numpy as np

# for windows
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def image_to_ocr_text(image_path):
    image = clean_image(image_path)
    text = pytesseract.image_to_string(image)
    print(text)
    return text, image

def clean_image(image_path):
    image = cv2.imread(image_path)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = 255 - image

    image = cv2.threshold(image, 120, 255, cv2.ADAPTIVE_THRESH_MEAN_C)[1]
    return image

def image_to_ocr_conversation(image_path):
    image = clean_image(image_path)
    df = pytesseract.image_to_data(image, output_type=pytesseract.Output.DATAFRAME)
    df_clean = df[~df.text.isna()].reset_index(drop=True)

    df_main = df_clean.groupby('block_num', as_index=False).agg({'text': ' '.join, 'left': 'first', 'top': 'first'})
    df_main['person'] = np.where(df_main.left < int(image.shape[1] * 0.15), 'opposite person', 'me')

    df_main.text.replace(',', ' ', inplace=True)
    chat_conversation_string = df_main.to_csv(index=False)

    print(chat_conversation_string)
    return chat_conversation_string, image
