(ns rand-audio-book.core
  (:require [clojure.tools.cli :refer [parse-opts]])
  (:require [clojure.string :as str])
  ;; (:require [clojure.data.json :as json])
  (:require [clojure.java.io :as io])
  (:use overtone.live)
  ;; ;;(:use overtone.core)
  (:gen-class)
  )

(use 'rand-audio-book.md5)
(use 'rand-audio-book.preflight)

(def datadir "data")
(def voice-dir "voices")
(def long-delay 2000)
(def short-delay 500)


;; (swap! live-config assoc-in [:sc-args :max-buffers] 1024)

;; given a voice and a letter, return the path to the sample
(defn path-to-sample [datadir voice text]
  (let [
        dest (io/file datadir voice-dir)
        voice-dest (io/file dest voice)
        ;; src (str (md5 text) ".wav")
        src (str text ".wav")
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

;; ;;
;; ;; split a line into list of component parts
;; ;;
;; (defn line-groupings [line]
;;   (clojure.string/split line #"\s+")
;;   )

;; ;;
;; ;; get the index of a line
;; ;; ["00000" "10097" "32533" "76520" "13586" "34673" "54876" "80959" "09117" "39292" "74945"]
;; ;; => "00000"
;; ;;
;; (defn line-index [line]
;;   (first (line-groupings line))
;;   )

;; ;;
;; ;; get the data of a line
;; ;; ["00000" "10097" "32533" "76520" "13586" "34673" "54876" "80959" "09117" "39292" "74945"]
;; ;; => ["10097" "32533" "76520" "13586" "34673" "54876" "80959" "09117" "39292" "74945"]
;; ;;
;; (defn line-data [line]
;;   (rest (line-groupings line))
;;   )

;;
;; play a sample for the specified voice/text
;; this assumes the sample has already been generated
;;
;;
;; speak the contents of a line
;; note that we are skipping the index entry
;;
(defn speak-letter [start-at datadir voice letter]
  (let [
      path (path-to-letter datadir voice letter)
      smpl (sample path)
      dur (:duration smpl)
      done-at (+ start-at (* 1000 dur))
    ]
    ;; (prn path)
    (apply-by start-at #(smpl))
    done-at
  )
)

;;
;; read the specified text aloud, letter by letter
;;
(defn read-it [start-at datadir voice data]
  (let [
        obj (first data) ;; this will look like [delay letter]
        key (last obj) ;; the letter itself
        smpl (sample (path-to-letter datadir voice key)) ;; the wav sample
        dur (* 1000 (:duration smpl)) ;; duration of the letter
        pause (+ dur (first obj)) ;; how long to pause
        done-at (+ start-at pause) ;; when will we be done with the sample?
        ]

    (if (some? key)
      ;; schedule to be read
      (apply-by start-at #(speak-letter start-at datadir voice key))
      )

    ;; recurse to the next letter if needed
    (if (empty? (rest data))
      done-at
      (read-it done-at datadir voice (rest data))
      )
    )
  )

;;
;; schedule text to be read
;;
(defn read-text-as-letters [start-at datadir voice txt]
  (if (nil? txt)
    nil
    (read-it start-at datadir voice
      (map (fn [[idx val]] [(if (== (rem (+ idx 1) 5) 0) long-delay short-delay) val])
          (map-indexed vector (
            seq (
              char-array (
                str/lower-case (
                  str/replace txt #"[^a-zA-Z0-9]" ""))))))
      )
    )
)

;; get the last scheduled job
(defn last-job
  []
  ;; we'll ignore jobs with the description 'non-blocking'
  (let [pool (remove (fn [x] (= "non-blocking" (:desc x))) (overtone.at-at/scheduled-jobs player-pool))]
    (println (count pool))
    (if (= 0 (count pool))
      nil
      (reduce
       #(if (> (+ (:created-at %1) (:initial-delay %1)) (+ (:created-at %2) (:initial-delay %2))) %1 %2) pool))
    ))

;; determine when the last job in the queue will be run. note that
;; this is when the job starts, not finishes, so it's not exactly
;; when the queue is clear
(defn queue-is-clear-at
  []
  (if (nil? (last-job))
    0 (let [j (last-job)
            created-at (:created-at j)
            delay (:initial-delay j)]
        (+ created-at delay))))

;; halt processing until there aren't any scheduled overtone jobs
;; this is a little hacky but it certainly gets the job done
(defn block-on-jobs
  ([] (block-on-jobs 2500 1000))

  ([initial-delay poll]
   (println "block on jobs")
   ;; give the queue a little time to start filling
   (Thread/sleep initial-delay)
   (while (some? (last-job))
     (do
        (println (last-job))
       (Thread/sleep poll)))
   ))

(defn generate [datadir voice lines]
  (println (str "datadir: " datadir))
  (println (str "voice: " voice))

  (loop [
          lines lines
          next-at (now)
          ]
    (let [
          line (first lines)
          next-at (read-text-as-letters next-at datadir voice line)
          ]

      (if-not (nil? (first lines))
        (recur (rest lines) next-at)
        )
      )
    )
  )
   
  

;; 50 lines per page
;; 400 pages

(defn -main [& args]
  (let [
    dest "chapter-01.wav"
  ]
    (preflight datadir "Matthew")
    (recording-start dest)
    (generate datadir "Matthew" (parse-lines (read-digits "data/short.txt")))

    (block-on-jobs)
    (Thread/sleep 5000)

    (stop)
    (recording-stop)
  )
)
