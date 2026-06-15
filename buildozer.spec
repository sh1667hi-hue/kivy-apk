[app]

title = hazegh-ks
package.name = hazeghks
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0

requirements = python3,kivy,requests,pyjnius

orientation = portrait

fullscreen = 0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21

[buildozer]

log_level = 2
warn_on_root = 1
