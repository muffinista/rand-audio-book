(ns rand-audio-book.md5)

(import 'java.security.MessageDigest
        'java.math.BigInteger)

(defn md5
  [^String s]
  (->> s
       .getBytes
       (.digest (MessageDigest/getInstance "MD5"))
       (BigInteger. 1)
       (format "%032x")))

