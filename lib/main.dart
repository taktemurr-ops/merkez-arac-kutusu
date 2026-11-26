import 'package:arac_motoru/arac_motoru.dart';
import 'package:flutter/material.dart';
import 'package:studio_core/apps/apps.dart';
import 'package:uyg_aci_olcer/uyg_aci_olcer.dart';
import 'package:uyg_ag_bilgisi/uyg_ag_bilgisi.dart';
import 'package:uyg_alarm_saati/uyg_alarm_saati.dart';
import 'package:uyg_alkisla_telefonu_bul/uyg_alkisla_telefonu_bul.dart';
import 'package:uyg_arsiv_acici/uyg_arsiv_acici.dart';
import 'package:uyg_ayna/uyg_ayna.dart';
import 'package:uyg_barometre/uyg_barometre.dart';
import 'package:uyg_beden_ve_ayakkabi_numarasi_cevirici/uyg_beden_ve_ayakkabi_numarasi_cevirici.dart';
import 'package:uyg_bilimsel_hesap_makinesi/uyg_bilimsel_hesap_makinesi.dart';
import 'package:uyg_birim_cevirici/uyg_birim_cevirici.dart';
import 'package:uyg_bluetooth_bulucu/uyg_bluetooth_bulucu.dart';
import 'package:uyg_boya_ve_fayans_hesaplayici/uyg_boya_ve_fayans_hesaplayici.dart';
import 'package:uyg_buyutec/uyg_buyutec.dart';
import 'package:uyg_cetvel_ve_olcum/uyg_cetvel_ve_olcum.dart';
import 'package:uyg_denklem_cozucu/uyg_denklem_cozucu.dart';
import 'package:uyg_dokunmatik_ve_tus_testi/uyg_dokunmatik_ve_tus_testi.dart';
import 'package:uyg_dosya_yoneticisi/uyg_dosya_yoneticisi.dart';
import 'package:uyg_doviz_cevirici/uyg_doviz_cevirici.dart';
import 'package:uyg_dunya_saati/uyg_dunya_saati.dart';
import 'package:uyg_ekran_ve_olu_piksel_testi/uyg_ekran_ve_olu_piksel_testi.dart';
import 'package:uyg_el_feneri/uyg_el_feneri.dart';
import 'package:uyg_elektrik_hesaplayici/uyg_elektrik_hesaplayici.dart';
import 'package:uyg_enstruman_akort/uyg_enstruman_akort.dart';
import 'package:uyg_gece_masa_saati/uyg_gece_masa_saati.dart';
import 'package:uyg_geri_sayim/uyg_geri_sayim.dart';
import 'package:uyg_goz_koruma_filtresi/uyg_goz_koruma_filtresi.dart';
import 'package:uyg_gps_hiz_olcer/uyg_gps_hiz_olcer.dart';
import 'package:uyg_grafik_cizen_hesap_makinesi/uyg_grafik_cizen_hesap_makinesi.dart';
import 'package:uyg_hesap_makinesi/uyg_hesap_makinesi.dart';
import 'package:uyg_hoparlor_temizleme/uyg_hoparlor_temizleme.dart';
import 'package:uyg_isik_olcer/uyg_isik_olcer.dart';
import 'package:uyg_kameradan_renk_secici/uyg_kameradan_renk_secici.dart';
import 'package:uyg_karar_carki/uyg_karar_carki.dart';
import 'package:uyg_kidem_ve_ihbar_tazminati_hesaplayici/uyg_kidem_ve_ihbar_tazminati_hesaplayici.dart';
import 'package:uyg_kizilotesi_kumanda/uyg_kizilotesi_kumanda.dart';
import 'package:uyg_kronometre/uyg_kronometre.dart';
import 'package:uyg_lastik_ebati_hesaplayici/uyg_lastik_ebati_hesaplayici.dart';
import 'package:uyg_maas_net_brut_hesaplayici/uyg_maas_net_brut_hesaplayici.dart';
import 'package:uyg_matris_ve_istatistik_hesaplayici/uyg_matris_ve_istatistik_hesaplayici.dart';
import 'package:uyg_mesafe_ve_yukseklik_olcer/uyg_mesafe_ve_yukseklik_olcer.dart';
import 'package:uyg_metal_dedektoru/uyg_metal_dedektoru.dart';
import 'package:uyg_metronom/uyg_metronom.dart';
import 'package:uyg_mors_kodu/uyg_mors_kodu.dart';
import 'package:uyg_mutfak_olcu_cevirici/uyg_mutfak_olcu_cevirici.dart';
import 'package:uyg_nfc_okuyucu/uyg_nfc_okuyucu.dart';
import 'package:uyg_not_ortalamasi_hesaplayici/uyg_not_ortalamasi_hesaplayici.dart';
import 'package:uyg_pil_ve_cihaz_bilgisi/uyg_pil_ve_cihaz_bilgisi.dart';
import 'package:uyg_pusula/uyg_pusula.dart';
import 'package:uyg_qr_olusturucu/uyg_qr_olusturucu.dart';
import 'package:uyg_qr_ve_barkod_okuyucu/uyg_qr_ve_barkod_okuyucu.dart';
import 'package:uyg_rakim_olcer/uyg_rakim_olcer.dart';
import 'package:uyg_rastgele_isim_ve_takim_secici/uyg_rastgele_isim_ve_takim_secici.dart';
import 'package:uyg_roma_rakami_cevirici/uyg_roma_rakami_cevirici.dart';
import 'package:uyg_sayac/uyg_sayac.dart';
import 'package:uyg_sayi_tabani_cevirici/uyg_sayi_tabani_cevirici.dart';
import 'package:uyg_ses_olcer/uyg_ses_olcer.dart';
import 'package:uyg_sifre_uretici/uyg_sifre_uretici.dart';
import 'package:uyg_skor_tutucu/uyg_skor_tutucu.dart';
import 'package:uyg_sos_feneri_ve_acil_durum/uyg_sos_feneri_ve_acil_durum.dart';
import 'package:uyg_su_terazisi/uyg_su_terazisi.dart';
import 'package:uyg_takvim_cevirici/uyg_takvim_cevirici.dart';
import 'package:uyg_titresim_olcer/uyg_titresim_olcer.dart';
import 'package:uyg_ton_ureteci/uyg_ton_ureteci.dart';
import 'package:uyg_yakit_tuketimi_hesaplayici/uyg_yakit_tuketimi_hesaplayici.dart';
import 'package:uyg_yas_ve_tarih_farki/uyg_yas_ve_tarih_farki.dart';
import 'package:uyg_yuzde_ve_kesir_hesaplayici/uyg_yuzde_ve_kesir_hesaplayici.dart';
import 'package:uyg_zamanlayici/uyg_zamanlayici.dart';
import 'package:uyg_zar_yazi_tura_rastgele_sayi/uyg_zar_yazi_tura_rastgele_sayi.dart';

/// Araç Kutusu: 68 sade, çevrimdışı araç tek uygulamada. Her aracın verisi
/// ayrı saklanır; reklam yalnızca bir araçtan çıkarken ve en az 3 dakika
/// arayla gösterilir.
final hubConfig = AppHubConfig(
  hubId: 'merkez-arac-kutusu',
  title: aracHubTitle,
  tagline: aracHubTagline,
  icon: Icons.handyman_rounded,
  style: aracHubStyle,
  categories: aracCategories,
  tools: [
    hesapMakinesiTool,
    bilimselHesapMakinesiTool,
    birimCeviriciTool,
    dovizCeviriciTool,
    elFeneriTool,
    qrVeBarkodOkuyucuTool,
    qrOlusturucuTool,
    pusulaTool,
    suTerazisiTool,
    cetvelVeOlcumTool,
    sesOlcerTool,
    buyutecTool,
    aynaTool,
    gpsHizOlcerTool,
    rakimOlcerTool,
    zarYaziTuraRastgeleSayiTool,
    kararCarkiTool,
    kronometreTool,
    zamanlayiciTool,
    alarmSaatiTool,
    dunyaSaatiTool,
    geriSayimTool,
    metronomTool,
    enstrumanAkortTool,
    dosyaYoneticisiTool,
    pilVeCihazBilgisiTool,
    sayacTool,
    skorTutucuTool,
    barometreTool,
    isikOlcerTool,
    titresimOlcerTool,
    metalDedektoruTool,
    aciOlcerTool,
    mesafeVeYukseklikOlcerTool,
    kameradanRenkSeciciTool,
    morsKoduTool,
    ekranVeOluPikselTestiTool,
    hoparlorTemizlemeTool,
    dokunmatikVeTusTestiTool,
    geceMasaSaatiTool,
    takvimCeviriciTool,
    yasVeTarihFarkiTool,
    romaRakamiCeviriciTool,
    sayiTabaniCeviriciTool,
    yuzdeVeKesirHesaplayiciTool,
    denklemCozucuTool,
    grafikCizenHesapMakinesiTool,
    matrisVeIstatistikHesaplayiciTool,
    elektrikHesaplayiciTool,
    boyaVeFayansHesaplayiciTool,
    mutfakOlcuCeviriciTool,
    bedenVeAyakkabiNumarasiCeviriciTool,
    lastikEbatiHesaplayiciTool,
    yakitTuketimiHesaplayiciTool,
    rastgeleIsimVeTakimSeciciTool,
    notOrtalamasiHesaplayiciTool,
    maasNetBrutHesaplayiciTool,
    kidemVeIhbarTazminatiHesaplayiciTool,
    sifreUreticiTool,
    sosFeneriVeAcilDurumTool,
    tonUreteciTool,
    nfcOkuyucuTool,
    agBilgisiTool,
    gozKorumaFiltresiTool,
    alkislaTelefonuBulTool,
    kizilotesiKumandaTool,
    bluetoothBulucuTool,
    arsivAciciTool,
  ],
  featured: aracFeatured,
  privacyUrl: 'https://github.com/taktemurr-ops/merkez-arac-kutusu/blob/main/PRIVACY.md',
);

void main() => bootstrapAppHub(hubConfig);
