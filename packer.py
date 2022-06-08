from datetime import datetime
from dateutil.tz import tzoffset
from inflection import camelize
import json
import arrow


def db_pack(item: dict, iso_format_date=False, pack_depth=False) -> dict:
    if isinstance(item, dict):
        to_return = dict()
        for i in item:
            to_return[camelize(i, True)] = db_pack(item[i], iso_format_date, True)
        if pack_depth:
            return json.dumps(to_return, ensure_ascii=False)
        else:
            return to_return
    elif isinstance(item, str):
        try:
            if item.startswith('[') or item.startswith('{'):
                _d = json.loads(item)
                _dt = db_pack(_d, True, False)
                return json.dumps(_dt, ensure_ascii=False)
            else:
                return item
        except:
            return item

    elif isinstance(item, list):
        to_return = list()
        for i in item:
            to_return.append(db_pack(i, iso_format_date, True))
        if pack_depth:
            return json.dumps(to_return, ensure_ascii=False)
        else:
            return to_return

    elif isinstance(item, datetime):
        if iso_format_date:
            return arrow.get(item).isoformat()
        else:
            return item.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    else:
        return item


def db_unpack(item: dict, iso_format_date=False) -> dict:
    if isinstance(item, dict):
        to_return = dict()
        for i in item:
            to_return[camelize(i, False)] = db_unpack(item[i], iso_format_date)
        return to_return
    elif isinstance(item, str):
        try:
            if item.startswith('[') or item.startswith('{'):
                _d = json.loads(item)
                return db_unpack(_d, iso_format_date)
            else:
                return item
        except:
            return item

    elif isinstance(item, list):
        to_return = list()
        for i in item:
            to_return.append(db_unpack(i, iso_format_date))
        return to_return

    elif isinstance(item, datetime):
        if iso_format_date:
            return arrow.get(item).isoformat()
        else:
            return item
    else:
        return item


if __name__ == '__main__':
    a = {
        "workerId": "worker_1",
        "job": "queryInstructor",
        "instructor": {
            "instructorId": "26903378",
            "title": "Emrah Yüksel",
            "name": "Emrah",
            "jobTitle": "Web Geliştirici ve Eğitmen",
            "description": "<p>Kurslarıma ilgi gösterek beni 2017'de Udemy'nin En İyi 3 Eğitmeni arasına sokan değerli öğrencilerime teşekkürler. </p>\n\n<p>\"Anadolu Üniversitesi - Yönetim Bilişim Sistemleri lisans derecemi tamamlamakla birlikte çeşitli kamu kuruluşlarında edindiğim  11 yıla yakın tecrübenin ardından şu an Bilgi İşlem Yöneticisi olarak profesyonel hayatıma devam etmekteyim. </p>\n\n\n\n<p>Ek olarak freelancer ve olarak Web Programlama üzerine aktif olarak çalışarak projeler geliştiriyorum.  </p>\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n<p>Son yıllarda çeşitli platformlar üzerinde 400 'den fazla konu üzerine yayınladığım eğitim videoları 2.000.000'u aşan izlenme almış bulunmakta. 2017 itibariyle Udemy'de, kapsayıcı müfredata sahip çeşitli konular üzerine yeni eğitimler üretmeye karar vermiş bulunmaktayım. </p>\n\n<p>1 Nisan 2018 İtibariyle Dijital içeriklerimi Akademi bünyesinden üretmek ve dijital içerik üretecek eğitmenlerin gelişimine katkı sunmak ve ortak çalışma yapmak amacıyla Eğitimin Anahtarı sloganıyla  EDUKEY Dijital Eğitim Akademisini kurdum. </p>\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n<p>Detaylı bilgi için internet sitemi yada Youtube kanalımı yada internet sitemi \"emrah yüksel\" olarak aratarak ziyaret edebilirsiniz.</p>\n\n\n\n\n\n\n\n\n\n<p>Derslerde görüşmek dileğiyle...</p>\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n<p><br><strong></strong></p>",
            "instructorImagePath": "/home/vids/up/instructors/26903378.jpg",
            "urlTwitter": "https://twitter.com/eyuksel2015",
            "urlFacebook": "https://www.facebook.com/emrahyukselcom",
            "urlLinkedin": "",
            "urlYoutube": "https://www.youtube.com/channel/UC2u9Gc37Rq44dB3mW4Kdi-w",
            "urlPersonalWebsite": "http://www.emrahyuksel.com.tr"
        }
    }

    print(json.dumps(db_pack(a['instructor']), ensure_ascii=False))

