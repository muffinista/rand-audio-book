(ns rand-audio-book.core
  (:require [clojure.tools.cli :refer [parse-opts]])
  (:require [clojure.string :as str])
  (:require [clojure.data.json :as json])
  (:require [clojure.java.io :as io])
  (:use overtone.live)
  ;;(:use overtone.core)
  (:gen-class)
  )

;; given a voice and the text to be spoken, return the
;; path where we expect the sample to exist
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

;; given a voice and a letter, return the path to the sample
;; NOTE: this is path-to-sample but without the md5 hash, so
;; these two functions can probably be refactored
(defn path-to-letter [datadir voice text]
  (let [
        dest (io/file datadir voice-dir)
        voice-dest (io/file dest voice)
        src (str text ".wav")
        filename (.toString (io/file voice-dest src))
        ]
    filename
    )
  )