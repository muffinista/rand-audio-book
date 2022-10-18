(defproject rand-audio-book "1.0.0"
  :description "Audio book of the RAND corp random number list"
  :url "http://muffinlabs.com"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :dependencies [
    [org.clojure/clojure "1.11.1"]
    [org.clojure/tools.cli "1.0.206"]
    [org.clojure/data.json "0.2.6"]
    [overtone/overtone "0.10.6"]
    [com.cognitect.aws/api "0.8.596"]
    [com.cognitect.aws/endpoints "1.1.12.307"]
    [com.cognitect.aws/polly "822.2.1193.0"]
    [lynxeyes/dotenv "1.0.2"]
  ]
  :main  ^:skip-aot rand-audio-book.core
  :jvm-opts ^:replace []
  :native-path "native"
  :source-paths ["src"]
  :target-path "target/%s"
  :sc-args {:max-buffers 4096}
  :profiles {:uberjar {:aot :all}})

  