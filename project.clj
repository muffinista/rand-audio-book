(defproject rand-audio-book "1.0.0"
  :description "Audio book of the RAND corp random number list"
  :url "http://muffinlabs.com"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :dependencies [
    [org.clojure/clojure "1.11.1"]
    [org.clojure/tools.cli "1.0.206"]
    [overtone/overtone "0.10.5"]
  ]
  :main rand-audio-book/core
  :native-path "native"
  :source-paths ["src"])
  