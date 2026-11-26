#!/usr/bin/env python3
"""Patches the platform folders created by `flutter create` (CI step).

* Android: app name, INTERNET permission, AdMob APPLICATION_ID, minSdk 23
  (Android 6+), target/compile SDK >= 35, every screen size (phones,
  tablets, foldables, Chromebooks; resizable multi-window), HTTPS-only
  network security config, optional release signing from CI secrets.
* iOS: display name, AdMob id, SKAdNetwork, tracking text, iOS 14+,
  universal app (iPhone + iPad, every iPad orientation, Split View /
  Stage Manager), App Transport Security kept strict.
* Web: title, description, PWA manifest (any orientation, standalone),
  referrer policy.

Idempotent: safe to run on every build.
"""
import json
import os
import re

APP_NAME = "Toolbox"
APP_NAME_TR = "Araç Kutusu"
# XML/HTML içinde "&" kaçışlı yazılır (AndroidManifest, Info.plist, index.html).
APP_NAME_XML = APP_NAME.replace("&", "&amp;")
# Google's PUBLIC TEST AdMob app ids. Replace before publishing.
ADMOB_ANDROID = os.environ.get("ADMOB_APP_ID_ANDROID") or "ca-app-pub-3940256099942544~3347511713"
ADMOB_IOS = os.environ.get("ADMOB_APP_ID_IOS") or "ca-app-pub-3940256099942544~1458002511"


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def android():
    man = "android/app/src/main/AndroidManifest.xml"
    if os.path.exists(man):
        s = read(man)
        s = re.sub(r'android:label="[^"]*"', 'android:label="%s"' % APP_NAME_XML, s, count=1)
        # Every screen size + resizable windows (tablets, foldables, ChromeOS).
        if "<supports-screens" not in s:
            s = s.replace(
                "<application",
                '<supports-screens android:smallScreens="true" android:normalScreens="true" '
                'android:largeScreens="true" android:xlargeScreens="true" android:anyDensity="true"/>\n    <application',
                1,
            )
        if "android:resizeableActivity" not in s:
            s = s.replace("<application", '<application android:resizeableActivity="true"', 1)
        # HTTPS only (no cleartext traffic) via network security config.
        if "android:networkSecurityConfig" not in s:
            s = s.replace(
                "<application",
                '<application android:networkSecurityConfig="@xml/network_security_config" '
                'android:usesCleartextTraffic="false"',
                1,
            )
        # Never lock orientation in the manifest; the app decides at runtime
        # (phones portrait, tablets/foldables every orientation).
        s = re.sub(r'\s+android:screenOrientation="[^"]*"', "", s)
        if "android.permission.INTERNET" not in s:
            s = s.replace("<application", '<uses-permission android:name="android.permission.INTERNET"/>\n    <application', 1)
        # Araç izinleri: yalnızca ilgili araç açıldığında, önce açıklama
        # gösterilerek istenir. Tüm dosyalara erişim (MANAGE_EXTERNAL_STORAGE)
        # İSTENMEZ: dosya yöneticisi sistem seçicisini (SAF) kullanır.
        for perm in ("android.permission.CAMERA", "android.permission.RECORD_AUDIO",
                     "android.permission.ACCESS_FINE_LOCATION", "android.permission.ACCESS_COARSE_LOCATION",
                     "android.permission.POST_NOTIFICATIONS", "android.permission.SCHEDULE_EXACT_ALARM",
                     "android.permission.RECEIVE_BOOT_COMPLETED", "android.permission.VIBRATE",
                     "android.permission.NFC", "android.permission.ACCESS_WIFI_STATE",
                     "android.permission.ACCESS_NETWORK_STATE"):
            if perm not in s:
                s = s.replace("<application", '<uses-permission android:name="%s"/>\n    <application' % perm, 1)
        for feat in ("android.hardware.camera", "android.hardware.camera.flash", "android.hardware.microphone",
                     "android.hardware.location.gps", "android.hardware.sensor.compass",
                     "android.hardware.sensor.barometer", "android.hardware.sensor.accelerometer",
                     "android.hardware.nfc", "android.hardware.wifi"):
            if feat not in s:
                s = s.replace("<application", '<uses-feature android:name="%s" android:required="false"/>\n    <application' % feat, 1)
        if "ScheduledNotificationReceiver" not in s:
            s = s.replace(
                "</application>",
                '    <receiver android:exported="false" android:name="com.dexterous.flutterlocalnotifications.ScheduledNotificationReceiver"/>\n'
                '        <receiver android:exported="false" android:name="com.dexterous.flutterlocalnotifications.ScheduledNotificationBootReceiver">\n'
                '            <intent-filter>\n'
                '                <action android:name="android.intent.action.BOOT_COMPLETED"/>\n'
                '                <action android:name="android.intent.action.MY_PACKAGE_REPLACED"/>\n'
                '                <action android:name="android.intent.action.QUICKBOOT_POWERON"/>\n'
                '            </intent-filter>\n'
                '        </receiver>\n    </application>',
                1,
            )
        if "com.google.android.gms.ads.APPLICATION_ID" not in s:
            s = s.replace(
                "</application>",
                '    <meta-data android:name="com.google.android.gms.ads.APPLICATION_ID" android:value="%s"/>\n    </application>' % ADMOB_ANDROID,
                1,
            )
        # Firebase: ölçüm ve çökme raporu uygulama içinden (izinle) açılır;
        # reklam kimliği hiç toplanmaz.
        for k in ("firebase_analytics_collection_enabled", "google_analytics_adid_collection_enabled",
                  "firebase_crashlytics_collection_enabled"):
            if k not in s:
                s = s.replace("</application>", '    <meta-data android:name="%s" android:value="false"/>\n    </application>' % k, 1)
        write(man, s)
    values_dir = "android/app/src/main/res/values"
    if os.path.isdir("android/app/src/main/res"):
        os.makedirs(values_dir, exist_ok=True)
        # Crashlytics Gradle eklentisi olmadan yapı kimliği (her derlemede yeni).
        import uuid
        write(
            os.path.join(values_dir, "crashlytics.xml"),
            '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
            '    <string name="com.google.firebase.crashlytics.mapping_file_id" translatable="false">%s</string>\n'
            '    <bool name="com.crashlytics.RequireBuildId">false</bool>\n</resources>\n' % uuid.uuid4().hex,
        )
    xml_dir = "android/app/src/main/res/xml"
    if os.path.isdir("android/app/src/main/res"):
        os.makedirs(xml_dir, exist_ok=True)
        write(
            os.path.join(xml_dir, "network_security_config.xml"),
            """<?xml version="1.0" encoding="utf-8"?>
<!-- HTTPS only; user-installed CAs are not trusted in release builds. -->
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system"/>
        </trust-anchors>
    </base-config>
</network-security-config>
""",
        )
    # R8 strips Room's generated WorkDatabase_Impl (WorkManager comes in via
    # google_mobile_ads), which crashes release builds at startup with
    # "Failed to create an instance of androidx.work.impl.WorkDatabase".
    # The Flutter Gradle plugin applies android/app/proguard-rules.pro.
    rules = "android/app/proguard-rules.pro"
    keep = """
-keep class * extends androidx.room.RoomDatabase { <init>(); }
-keep class androidx.work.impl.WorkDatabase_Impl { *; }
-keep class androidx.work.impl.** extends androidx.room.RoomDatabase { *; }
-dontwarn androidx.work.**
"""
    old = read(rules) if os.path.exists(rules) else ""
    if "WorkDatabase_Impl" not in old:
        write(rules, old + keep)
    for gradle in ["android/app/build.gradle.kts", "android/app/build.gradle"]:
        if not os.path.exists(gradle):
            continue
        s = read(gradle)
        kts = gradle.endswith(".kts")
        if kts:
            s = s.replace("minSdk = flutter.minSdkVersion", "minSdk = maxOf(flutter.minSdkVersion, 23)")
            s = s.replace("targetSdk = flutter.targetSdkVersion", "targetSdk = maxOf(flutter.targetSdkVersion, 35)")
            s = s.replace("compileSdk = flutter.compileSdkVersion", "compileSdk = maxOf(flutter.compileSdkVersion, 35)")
        else:
            s = s.replace("minSdkVersion flutter.minSdkVersion", "minSdkVersion Math.max(flutter.minSdkVersion, 23)")
            s = s.replace("minSdk flutter.minSdkVersion", "minSdk Math.max(flutter.minSdkVersion, 23)")
        # Yerel bildirim eklentisi Java 8+ kütüphaneleri ister (desugaring).
        if kts and "isCoreLibraryDesugaringEnabled" not in s:
            s = s.replace("compileOptions {", "compileOptions {\n        isCoreLibraryDesugaringEnabled = true", 1)
        if kts and "desugar_jdk_libs" not in s:
            s += '\ndependencies {\n    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")\n}\n'
        # Release signing from CI secrets when available (see docs/RELEASE.md).
        if kts and os.environ.get("ANDROID_KEYSTORE_PATH") and "gs100Release" not in s:
            s = s.replace(
                "buildTypes {",
                """signingConfigs {
        create("gs100Release") {
            storeFile = file(System.getenv("ANDROID_KEYSTORE_PATH"))
            storePassword = System.getenv("ANDROID_KEYSTORE_PASSWORD")
            keyAlias = System.getenv("ANDROID_KEY_ALIAS")
            keyPassword = System.getenv("ANDROID_KEY_PASSWORD")
        }
    }
    buildTypes {""",
                1,
            )
            s = s.replace(
                'signingConfig = signingConfigs.getByName("debug")',
                'signingConfig = signingConfigs.getByName("gs100Release")',
            )
        write(gradle, s)


def ios():
    plist = "ios/Runner/Info.plist"
    if os.path.exists(plist):
        s = read(plist)
        s = re.sub(
            r"(<key>CFBundleDisplayName</key>\s*<string>)[^<]*(</string>)",
            r"\g<1>%s\g<2>" % APP_NAME_XML,
            s,
        )
        extra = ""
        for key, text in (
            ("NSCameraUsageDescription", "Kamera yalnızca fener, büyüteç, QR okuma ve ölçüm araçları açıkken kullanılır; görüntü cihazdan çıkmaz. / The camera is used only while a camera tool is open; images never leave the device."),
            ("NSMicrophoneUsageDescription", "Mikrofon yalnızca ses ölçer, akort ve alkışla-bul açıkken cihazda dinlenir; kayıt yapılmaz. / The microphone listens on the device only in the sound meter, tuner and clap-to-find tools; nothing is recorded."),
            ("NSLocationWhenInUseUsageDescription", "Konum yalnızca GPS hız ve rakım araçlarında, araç açıkken kullanılır; saklanmaz. / Location is used only in the GPS speed and altitude tools while open; it is not stored."),
            ("NFCReaderUsageDescription", "NFC yalnızca NFC Etiket Okuyucu açıkken, siz okut dediğinizde etiketi okumak için kullanılır. / NFC is used only in the NFC Tag Reader, when you start a scan."),
            ("NSLocalNetworkUsageDescription", "Ağ Bilgisi aracı yalnızca bu cihazın ağ adreslerini gösterir; ağdaki başka cihazlara bağlanmaz. / Network Info only shows this device's own addresses; it does not connect to other devices."),
            ("NSMotionUsageDescription", "Hareket ve basınç sensörleri su terazisi, açı ölçer ve barometre için kullanılır. / Motion and pressure sensors power the level, angle meter and barometer."),
            ("NSBluetoothAlwaysUsageDescription", "Bluetooth yalnızca Bluetooth Cihaz Bulucu açıkken yakındaki cihazların adını ve sinyal gücünü görmek için kullanılır; bağlantı kurulmaz. / Bluetooth is used only in the Bluetooth Device Finder to see nearby devices' names and signal strength; nothing is connected."),
        ):
            if key not in s:
                extra += "\t<key>%s</key>\n\t<string>%s</string>\n" % (key, text)
        if "GADApplicationIdentifier" not in s:
            extra += "\t<key>GADApplicationIdentifier</key>\n\t<string>%s</string>\n" % ADMOB_IOS
        if "SKAdNetworkItems" not in s:
            extra += (
                "\t<key>SKAdNetworkItems</key>\n\t<array>\n\t\t<dict>\n"
                "\t\t\t<key>SKAdNetworkIdentifier</key>\n\t\t\t<string>cstr6suwn9.skadnetwork</string>\n"
                "\t\t</dict>\n\t</array>\n"
            )
        if "NSUserTrackingUsageDescription" not in s:
            extra += (
                "\t<key>NSUserTrackingUsageDescription</key>\n"
                "\t<string>Reklamları ilgi alanlarınıza göre göstermek için kullanılır. / "
                "Used to show more relevant ads.</string>\n"
            )
        # iPad: every orientation (required for Split View / Stage Manager);
        # iPhone orientation is chosen at runtime (portrait).
        if "UISupportedInterfaceOrientations~ipad" not in s:
            extra += (
                "\t<key>UISupportedInterfaceOrientations~ipad</key>\n\t<array>\n"
                "\t\t<string>UIInterfaceOrientationPortrait</string>\n"
                "\t\t<string>UIInterfaceOrientationPortraitUpsideDown</string>\n"
                "\t\t<string>UIInterfaceOrientationLandscapeLeft</string>\n"
                "\t\t<string>UIInterfaceOrientationLandscapeRight</string>\n\t</array>\n"
            )
        s = re.sub(r"\s*<key>UIRequiresFullScreen</key>\s*<true/>", "", s)
        # Keep App Transport Security strict (HTTPS only).
        s = re.sub(r"\s*<key>NSAllowsArbitraryLoads</key>\s*<true/>", "", s)
        if "FIREBASE_ANALYTICS_COLLECTION_ENABLED" not in s:
            extra += "\t<key>FIREBASE_ANALYTICS_COLLECTION_ENABLED</key>\n\t<false/>\n"
        if "FirebaseCrashlyticsCollectionEnabled" not in s:
            extra += "\t<key>FirebaseCrashlyticsCollectionEnabled</key>\n\t<false/>\n"
        if "ITSAppUsesNonExemptEncryption" not in s:
            extra += "\t<key>ITSAppUsesNonExemptEncryption</key>\n\t<false/>\n"
        if extra:
            idx = s.rfind("</dict>")
            s = s[:idx] + extra + s[idx:]
        write(plist, s)
    podfile = "ios/Podfile"
    if os.path.exists(podfile):
        s = read(podfile)
        s = re.sub(r"#?\s*platform :ios, '[0-9.]+'", "platform :ios, '15.0'", s, count=1)
        write(podfile, s)
    pbx = "ios/Runner.xcodeproj/project.pbxproj"
    if os.path.exists(pbx):
        s = read(pbx)
        s = re.sub(r"IPHONEOS_DEPLOYMENT_TARGET = [0-9.]+;", "IPHONEOS_DEPLOYMENT_TARGET = 15.0;", s)
        # Universal app: iPhone (1) + iPad (2).
        s = re.sub(r'TARGETED_DEVICE_FAMILY = "?[0-9,]+"?;', 'TARGETED_DEVICE_FAMILY = "1,2";', s)
        write(pbx, s)


def ios_entitlements():
    """NFC etiket okuma yetkisi (Core NFC). İmzasız CI derlemesini etkilemez;
    imzalı derlemede profilde 'NFC Tag Reading' yeteneği açık olmalıdır."""
    if not os.path.isdir("ios/Runner"):
        return
    ent = "ios/Runner/Runner.entitlements"
    if not os.path.exists(ent):
        write(
            ent,
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
            '<plist version="1.0">\n<dict>\n'
            '\t<key>com.apple.developer.nfc.readersession.formats</key>\n'
            '\t<array>\n\t\t<string>NDEF</string>\n\t\t<string>TAG</string>\n\t</array>\n'
            '</dict>\n</plist>\n',
        )
    pbx = "ios/Runner.xcodeproj/project.pbxproj"
    if os.path.exists(pbx):
        s = read(pbx)
        if "CODE_SIGN_ENTITLEMENTS" not in s:
            # Yalnızca Runner hedefinin yapılandırmaları (INFOPLIST_FILE = Runner/Info.plist).
            s = s.replace(
                "INFOPLIST_FILE = Runner/Info.plist;",
                "CODE_SIGN_ENTITLEMENTS = Runner/Runner.entitlements;\n\t\t\t\tINFOPLIST_FILE = Runner/Info.plist;",
            )
            write(pbx, s)


def web():
    index = "web/index.html"
    if os.path.exists(index):
        s = read(index)
        s = re.sub(r"<title>[^<]*</title>", "<title>%s</title>" % APP_NAME_XML, s)
        s = re.sub(
            r'<meta name="description" content="[^"]*">',
            '<meta name="description" content="%s - %s">' % (APP_NAME_XML, APP_NAME_TR),
            s,
        )
        if 'name="referrer"' not in s:
            s = s.replace("<head>", '<head>\n  <meta name="referrer" content="strict-origin-when-cross-origin">', 1)
        write(index, s)
    manifest = "web/manifest.json"
    if os.path.exists(manifest):
        m = json.loads(read(manifest))
        m["name"] = APP_NAME
        m["short_name"] = APP_NAME[:12]
        m["description"] = APP_NAME_TR
        m["display"] = "standalone"
        m["orientation"] = "any"
        m["categories"] = ["utilities", "productivity"]
        write(manifest, json.dumps(m, indent=2, ensure_ascii=False))


# Güvenlik denetimi (2026-11-26): Android yedekleme kuralları.
# Biyometrik anahtarın şifreli deposu (flutter_secure_storage) ve gizli albüm
# hiçbir yedeğe alınmaz (anahtar Keystore'da kalır, geri yüklenince bozulur).
# LOCAL_ONLY: sağlık/finans kayıtları Google bulut yedeğine alınmaz; yalnızca
# yeni telefona doğrudan aktarımda (cihazdan cihaza) taşınır.
LOCAL_ONLY_BACKUP = False

_SECRET_EXCLUDES = (
    '    <exclude domain="sharedpref" path="FlutterSecureStorage.xml"/>\n'
    '    <exclude domain="root" path="app_flutter/gizli_album/"/>\n'
    '    <exclude domain="root" path="app_flutter/gizli_album_tmp/"/>\n'
)
_ALL_EXCLUDES = "".join(
    '    <exclude domain="%s" path="."/>\n' % d for d in ("root", "file", "database", "sharedpref", "external")
)


def android_backup():
    man = "android/app/src/main/AndroidManifest.xml"
    res = "android/app/src/main/res"
    if not os.path.exists(man) or not os.path.isdir(res):
        return
    os.makedirs(res + "/xml", exist_ok=True)
    full = _ALL_EXCLUDES if LOCAL_ONLY_BACKUP else _SECRET_EXCLUDES
    write(res + "/xml/gs100_backup_rules.xml",
          '<?xml version="1.0" encoding="utf-8"?>\n<full-backup-content>\n%s</full-backup-content>\n' % full)
    cloud = _ALL_EXCLUDES if LOCAL_ONLY_BACKUP else _SECRET_EXCLUDES
    write(res + "/xml/gs100_data_extraction_rules.xml",
          '<?xml version="1.0" encoding="utf-8"?>\n<data-extraction-rules>\n'
          '  <cloud-backup>\n%s  </cloud-backup>\n'
          '  <device-transfer>\n%s  </device-transfer>\n'
          '</data-extraction-rules>\n' % (cloud.replace("    <", "    <"), _SECRET_EXCLUDES))
    s = read(man)
    if "android:fullBackupContent" not in s:
        s = s.replace(
            "<application",
            '<application android:fullBackupContent="@xml/gs100_backup_rules" '
            'android:dataExtractionRules="@xml/gs100_data_extraction_rules"',
            1,
        )
        write(man, s)


if __name__ == "__main__":
    android()
    android_backup()
    ios()
    ios_entitlements()
    web()
    print("platform folders patched")
