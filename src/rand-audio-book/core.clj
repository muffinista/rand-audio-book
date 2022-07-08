(ns rand-audio-book.core
  (:require [clojure.tools.cli :refer [parse-opts]])
  (:require [clojure.string :as str])
  (:require [clojure.data.json :as json])
  (:require [clojure.java.io :as io])
  ;; (:use overtone.live)
  ;; ;;(:use overtone.core)
  (:gen-class)
  )

(defn read-digits [src]
  (let [
    text (slurp src)
  ]
  text
  )  
)

(defn parse-lines [text]
  (clojure.string/split-lines text)  
  )

;; (first (parse-lines (read-digits "data/digits.txt")))

;; "00000   10097 32533  76520 13586  34673 54876  80959 09117  39292 74945"

;; (clojure.string/split (first (parse-lines (read-digits "data/digits.txt"))) #"\s+")
;; ["00000" "10097" "32533" "76520" "13586" "34673" "54876" "80959" "09117" "39292" "74945"]

(defn line-groupings [line]
  (clojure.string/split line #"\s+")
  )

(defn line-index [line]
  (first (line-groupings line))
  )

(defn line-data [line]
  (rest (line-groupings line))
  )
  
;; ;; given a voice and the text to be spoken, return the
;; ;; path where we expect the sample to exist
;; (defn path-to-sample [datadir voice text]
;;   (let [
;;         dest (io/file datadir voice-dir)
;;         voice-dest (io/file dest voice)
;;         src (str (md5 text) ".wav")
;;         filename (.toString (io/file voice-dest src))
;;         ]
;;     filename
;;     )
;;   )

;; ;; given a voice and a letter, return the path to the sample
;; ;; NOTE: this is path-to-sample but without the md5 hash, so
;; ;; these two functions can probably be refactored
;; (defn path-to-letter [datadir voice text]
;;   (let [
;;         dest (io/file datadir voice-dir)
;;         voice-dest (io/file dest voice)
;;         src (str text ".wav")
;;         filename (.toString (io/file voice-dest src))
;;         ]
;;     filename
;;     )
;;   )