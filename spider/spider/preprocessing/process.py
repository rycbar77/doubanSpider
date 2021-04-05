from .TFIDF import TFIDF
import sqlite3


def process_in_db():
    tf_idf = TFIDF()
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    sqlstate = 'select bookid,comment1,comment2 from books'
    c.execute(sqlstate)
    rows = c.fetchall()
    for row in rows:
        bookid = row[0]
        s = row[1]
        tags1 = tf_idf.extract_tags(s, withWeight=False, topK=10)
        print(tags1)
        features1 = ",".join(tags1)
        s = row[2]
        tags2 = tf_idf.extract_tags(s, withWeight=False, topK=10)
        print(tags2)
        features2 = ','.join(tags2)
        sqlstate = "update books set features1 = '%s' , features2='%s' where bookid=%d" % (
            features1, features2, bookid)
        c.execute(sqlstate)

    conn.commit()
    c.close()
    conn.close()


def process_while_crawling(text):
    tf_idf = TFIDF()
    return ",".join(tf_idf.extract_tags(text, withWeight=False, topK=10))

# process()
