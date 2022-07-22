(ns rand-audio-book.core
  (:require [clojure.tools.cli :refer [parse-opts]])
  (:require [clojure.string :as str])
  ;; (:require [clojure.data.json :as json])
  (:require [clojure.java.io :as io])
  ;; (:use overtone.live)
  ;; ;;(:use overtone.core)
  (:gen-class)
  )

(def voice-dir "voices")
(def long-delay 2000)
(def short-delay 500)

;; given a voice and a letter, return the path to the sample
(defn path-to-sample [datadir voice text]
  (let [
        dest (io/file datadir voice-dir)
        voice-dest (io/file dest voice)
        src (str (md5 text) ".wav")
        filename (.toString (io/file voice-dest src))
        ]
    filename
    )
  )

;; (first (parse-lines (read-digits "data/digits.txt")))

;; "00000   10097 32533  76520 13586  34673 54876  80959 09117  39292 74945"

;; (clojure.string/split (first (parse-lines (read-digits "data/digits.txt"))) #"\s+")
;; ["00000" "10097" "32533" "76520" "13586" "34673" "54876" "80959" "09117" "39292" "74945"]

;;
;; load in the source digits file
;;
(defn read-digits [src]
  (let [
    text (slurp src)
  ]
  text
  )  
)

;;
;; split text file into lines
;;
(defn parse-lines [text]
  (clojure.string/split-lines text)  
  )

;;
;; split a line into list of component parts
;;
(defn line-groupings [line]
  (clojure.string/split line #"\s+")
  )

;;
;; get the index of a line
;; ["00000" "10097" "32533" "76520" "13586" "34673" "54876" "80959" "09117" "39292" "74945"]
;; => "00000"
;;
(defn line-index [line]
  (first (line-groupings line))
  )

;;
;; get the data of a line
;; ["00000" "10097" "32533" "76520" "13586" "34673" "54876" "80959" "09117" "39292" "74945"]
;; => ["10097" "32533" "76520" "13586" "34673" "54876" "80959" "09117" "39292" "74945"]
;;
(defn line-data [line]
  (rest (line-groupings line))
  )

;;
;; speak the contents of a line
;;
(defn speak-line [line]
  (prn (line-index line))  
  )


(doseq [line (parse-lines (read-digits "data/digits.txt"))]
    (speak-line line)
  )
