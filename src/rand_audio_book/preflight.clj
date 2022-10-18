(ns rand-audio-book.preflight
  (:require [clojure.data.json :as json])
  (:require [clojure.java.io :as io])
  (:require [dotenv :refer [env app-env]])
  (:require [cognitect.aws.client.api :as aws])
  (:require [cognitect.aws.credentials :as credentials])

  (:use [clojure.java.shell :only (sh)])
  (:use [clojure.string :as s])
  (:use rand-audio-book.md5)
  )
  
(defn generate-sample [dest voice text]
  (let [
        tmpfile (java.io.File/createTempFile "dest" "ogg")
        out (clojure.java.io/output-stream dest)
        ssml (if (s/includes? text "<speak") text (str "<speak><amazon:domain name=\"news\">" text "</amazon:domain></speak>"))
        polly (aws/client {:api :polly
        :credentials-provider (credentials/basic-credentials-provider
        {:access-key-id     (env "AWS_ACCESS_KEY_ID")
         :secret-access-key (env "AWS_SECRET_ACCESS_KEY")})
        
        })
        ;; Body is a blob type, which always returns an InputStream
        {stream :AudioStream} (aws/invoke polly {:op :SynthesizeSpeech :request {:Engine "neural"
          :TextType "ssml"
          :Text ssml
          :OutputFormat "ogg_vorbis"
          :VoiceId voice}})
    ]

    (clojure.java.io/copy stream tmpfile)
    (sh "sox" (str tmpfile) "--norm=-0.1" (str dest))    

    (.delete tmpfile)
    dest
    )
  )

(defn generate-if-missing [voice-dest voice k v]
  (let [
        file (clojure.java.io/file voice-dest k)
        built (.exists file)
        ]

    ;; make the directory for the specific voice
    (if-not (.exists (io/file voice-dest))
      (.mkdir (io/as-file voice-dest)))
    
    (println (str voice-dest " " voice " " k " " v))
    (if-not built
      (generate-sample file voice v)
      )
    )
  )

(defn letters-preflight [datadir voice]
  (let [
        sample-src (.toString (io/file datadir "voice-samples.json"))
        dest (io/file datadir "voices")

        voice-dest (.toString (io/file dest voice))
        letters (json/read-str (slurp sample-src))
        ]

    ;; make the directory for the voice samples
    (if-not (.exists (io/file dest))
      (.mkdir (io/as-file dest)))
    
    ;; make the directory for the specific voice
    (if-not (.exists (io/file voice-dest))
      (.mkdir (io/as-file voice-dest)))

    (doseq [keyval (seq letters)]
      (println (str "**** " voice-dest " -- " (key keyval)))
      (generate-if-missing voice-dest voice (key keyval) (val keyval))
      )
    )
  )

;; (defn read-preflight [datadir entry]
;;   (let [
;;         text (get entry :text)
;;         voice (get entry :voice)
;;         dest "voices"
;;         voice-dest (io/file datadir dest voice)
;;         filename (str (md5 text) ".wav")
;;         ]

;;     (println (str "generate this text: " text " " filename))
;;     (generate-if-missing voice-dest voice filename text)
;;     ;;(text-to-speech text voice)
;;     )
;;   )


(defn preflight [datadir voice]
  (letters-preflight datadir voice)
  )
