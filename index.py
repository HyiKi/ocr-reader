import json
import easyocr
import base64

reader = easyocr.Reader(['ch_sim', 'en'], model_storage_directory="model")

def render(data) :
    result_dict = {}
    result_dict['code'] = 'SUCCESS'
    result_dict['msg'] = 'success'
    result_dict['data'] = data
    return json.dumps(result_dict)

def parse(result) :
    dict_list = []
    # 转换为字典集列表
    for item in result:
        coordinates = item[0]
        text = item[1]
        dict_item = {
            'coordinates': [{'x': int(coord[0]), 'y': int(coord[1])} for coord in coordinates],
            'text': text
        }
        dict_list.append(dict_item)
    return dict_list

def ocr(image) :
    result = reader.readtext(image=image)
    return result

def readimage(image) :
    # call ocr
    result = ocr(image)

    # parse result
    data = parse(result)

    # return value must be iterable
    return render(data)

def handler(environ, start_response):
    # get request_body
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)
    body = json.loads(request_body)
    base64_image = body['image']
    # do something here
    image_data = base64.b64decode(base64_image)
    image_bytes = bytes(image_data)

    status = '200 OK'
    response_headers = [('Content-type', 'application/json;charset=utf-8')]
    start_response(status, response_headers)

    # return value must be iterable
    return readimage(image_bytes)

if __name__ == '__main__':
    # # 打开图像文件
    # with open('demo.png', 'rb') as file:
    #     # 读取图像文件的内容
    #     image_data = file.read()

    # # 将图像内容转换为字节对象
    # byte_data = bytes(image_data)
    base64_image = "iVBORw0KGgoAAAANSUhEUgAAANkAAAAXCAMAAACxghqAAAAAclBMVEX///9fY2hjZ2ze3+BqbnTw8fGgoqWbnaGEhor8/Pz4+Pnk5ebz8/TQ0dP19fakpqmJjJDCxMbq6uvMzc/IycpvcnixsrV3en/V1tjZ2duoqq2Qk5ZzdnuWmJy8vL9+gIW+v8GSlZh6fYKztbe3ubusrrE+jDOeAAAD40lEQVRYw+2U6a7aMBBG5/OSnZCV0BDIRt7/FeuxQ5pb6IL6o610j0Q0NvZ4juOYPvnk3yOJI/oNBkkf0XFIv0APmv4aZwVg+o0CcNy3wmMNIEjop3zBgX5FWMb0FgPcBJWZHwzNbFqjoI/EEHPlQYVvmmWol1sAlfyxWWQSv8XtYRYQCdW2I7AQXb43m/HFPE84v2d2QMd70WL+y2aZCVIhXphdkfJ/VUEUj0J5kVnqqNANROe66o1xGUD5EZt5QowmYHyXPZw48zyhv9M+GCY0sjux2ZaXcY2rmXvqqhq8OaWCqEu/4XjsTb9sMOVck6fEGD+2qBci06/NWKJ4NhuQFS7SSnhXBKEZd2k7lFQCk1ecoY4ZeiKIrm1wIUtT00aLvp1w2gU56jYT8KzZlpfRQvi+UJo8iOwYsmqLaZEDzsYFvuuvUVIY4OrxSKaAMoeu+5FZgPDJjBOg8+TjNdzNCqfcVADfmF15vkq4ZklQKVEn3CxrGCUGMzSzydMtIFFHPMeZbXkZH5LojKMxyPenkaUohzT9nmkpRRUGIomWGNkWRB70s1kQRcUJAT2bmXVGAVxCUpBSHnDiLZJnM7h0+9iSw3oekbpqfPPsYaADD+PBW6BtEr2abXmZbrLPnjyEezPKhPkpLr+wxyA94mzmoSdHGH+5QD6bgenil2Ys1yAnOK5U8XA240wS+f4GOTkzEgFfI3negGZbS4zbFkgMXMtqtuVlMJLT8EAfzEp8ibDQ2p9D9rC4etOM41dm3e3Wc/+zmSzc3e+TahIm0mhKHanMmSVYXpn1SFz2jip8YUsctsC9UenMtrzE1AEZmubJLBTHCtuRW6B9aJ6Wrod4iZN8NTug2s6NyLj44JXZJEJ7O99pFCZnepMH3vECqxkp/mbyJv5oVtrijZVPhQ2v0FtAE0rSnTPb8pLBNAqyM/ZmV1u8ujTEZrPR7AQN9mznJTGN4MyrWequozsqNrN/nF+Y5aiHwyxQkER9yxtIjTof1GaWI8gX1Pt3xgSmu/IhEpMTvon8XaAFgMCZbXmJ4cZdiXhnRp24F7y5uFsztHlg9NJanKoL97E2vNIHJK2tfjAL1elqVqDhxU9MvFPjKmqec2gAVZL9zpb6YUZ3BfR6NZsfZuERhqDg8Cog/HAXUFq11fqdbXkZ15jOtDerhP2WBbQ1M03BSxUBIBayJCbuTg8zOtqdS8iauUk0wpLTDi3TNYqStSckx9Z8RSyjbcTH4D6HZK/tfd6tsc7ad/HvUeS3bKHeDdnFrC1D+hss6JeLEPqNKXkAuZr909wnUY/viJGq3RueJ/rkk0/+A74CeeA7FiJ0LE4AAAAASUVORK5CYII="
    image_data = base64.b64decode(base64_image)
    image_bytes = bytes(image_data)
    result = readimage(image_bytes)
    print(str(result))