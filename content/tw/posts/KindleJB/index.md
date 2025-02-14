---
title: "Kindle 越獄 & KOReader"
date: 2025-02-12
tags: [""]
categories: ["Tech Share"]
draft: true
---
## Kindle Jailbreak

{{< alert cardColor="#e63946" iconColor="#1d3557" textColor="#f1faee">}}

警語：

越獄帶有一定風險，包括讓你的裝置變成磚頭（Bricked），再也無法使用。

{{< /alert >}}
<!--more-->

- 先前的 Jailbreak：

   - 需要特定韌體版本以下。

   - 解法：開著飛航模式硬是不讓他自動更新，然後等有人開發出更新版本的越獄方式。

- [WinterBreak](https://www.mobileread.com/forums/showthread.php?t=365372)

   - 不用特定韌體！

      WinterBreak is a new jailbreak which works on **ANY KINDLE** (from the K5) on **ANY FIRMWARE**

   - 步驟：

      - 建議直接照著[開源的 Wiki](https://kindlemodding.org/jailbreaking/WinterBreak/) 做，他最重要的部分都有附上圖片。

      - 要一路做到 `Post Jailbreak/Disabling OTA Updates` 完成，看到「Your Kindle is now jailbroken! Enjoy.」

      - 韌體版本確認：

         - 右上角三個點 > Device Option > Device Info

## ScreenSaver

- 自訂休眠畫面

- 需求：[韌體版本低於 5.16.3](https://www.mobileread.com/forums/showpost.php?p=4487524&postcount=3016)

- 選項：

   - 可以[降版](https://kindlemodding.org/firmware-and-flashing/downgrading/)

      - 會把裝置重置，所以你存的書、重點、筆記都會被刪掉

   - 裝 KOReader

      - 我是選這個，比較不麻煩，不過平常就不會是用 Kindle 原生的閱讀介面了，會需要適應新的閱讀介面

	  - KOReader 的另一個好處是他可以紀錄你的閱讀進度和各種奇怪的客製化，可以參考[這個影片](https://www.youtube.com/watch?v=HBKD7dh1rDU)。

## [KOReader](https://github.com/koreader/koreader)

- 直接照著 [GitHub 上的 Wiki](https://github.com/koreader/koreader/wiki/Installation-on-Kindle-devices) 做就好了

- 注意：如果你的裝置是 Kindle Paper White 4，然後韌體是在 5.17.1 附近的話，那版本 `2024.11 "Slang"` 可能會有無法啟動的狀態。可以試試看 [Marek's koreader nightly builds](https://fw.notmarek.com/khf/koreader/)。更詳細的討論可看[這個 issue](https://github.com/koreader/koreader/issues/12999#issuecomment-2569962928)。

- 前面如果有都做完的話，應該會裝好 KUAL 了。Launching 就直接走 KUAL 那個選項就好，也不用多裝另一個 launcher。

- 注意：KOReader 在開啟的狀態是不能用 USB 傳輸的，請記得關閉 KOReader 之後再插上 USB 傳輸檔案

### Dictionary

KOReader 裝好之後我遇到的第一個問題是：我之前愛用的 Merriam Webster 抓不到了 QQ

{{< alert icon="pencil" >}}
如果你沒有跟我一樣堅持要裝特定的字典的話，可以直接在 [KOReader 提供的字典](https://github.com/koreader/koreader/wiki/Dictionary-download)中選一個下載，或是[這邊](https://github.com/koreader/koreader/wiki/Dictionary-support#where-to-find--dictionaries)列出的其他開源的字典。
{{< /alert >}}

1. 下載字典本人：

   從 Amazon 的帳號裡面直接下載就好，位置在 `Amazon.com > Content Library > Dictionaries & User Guides > Merriam Webster's Advanced Learner's English Dictionary > Download & transfer via USB`

2. 用 Calibre 解 DRM，可以參考[這篇文章](https://www.reddit.com/r/Calibre/comments/1ck4w8e/2024_guide_on_removing_drm_from_kobo_kindle_ebooks/)來解（直接快轉到「Remove Kindle DRM」那段就可以了。

3. 用 [KindleUnpack](https://github.com/dougmassay/kindleunpack-calibre-plugin) 來解開 mobi 檔，會變成 html 檔

4. 用 [mobi2stardict](https://github.com/anezih/mobi2stardict/tree/main) 來把 html 變成需要的 StarDict 檔

5. 把生成的 StarDict 檔塞到 `koreader/data/dict` 裡面

這過程真的有點麻煩，但我好像也不能直接把最後生成的 StarDict 檔放在公開網路上 XD

### ScreenSaver

- Top Menu > ⚙︎ > screen > Sleep screen > Wallpaper

- 可以自己傳照片進去，長寬可以在 [Wiki 查](https://en.wikipedia.org/wiki/Amazon_Kindle#Device_specifications) Display 的 pixels 是多少

### Calibre-Web

如果你有架 Calibre-Web 的話，KOReader 有[支援 OPDS browser](https://github.com/koreader/koreader/wiki/OPDS-support) 可以去抓上面的書下來。你的網址應該會是 `https://your.address.com/opds`。

### iOS / 網頁

- KOReader 沒有 iOS 的版本，如果還是想要用的話，是有解法的（[感謝網友提供](https://www.facebook.com/groups/ereaderfamily/posts/7034302766626497)）

- 解法：

   - 在 server 上裝 [docker-koreader](https://github.com/zephyros-dev/docker-koreader)

   - 用網頁版的 VNC 去操作他，可以在 iOS 上把網頁變成 App，體驗取決於網速

   - 部分功能缺失：長按觸發字典似乎不 work

- 需求：

   - 有一台可以架網頁的 Server

   - Docker

- [安裝教學](https://github.com/zephyros-dev/docker-koreader?tab=readme-ov-file#installation)

- 裝好之後，要[同步](https://github.com/koreader/koreader/wiki/Progress-sync)兩個裝置的進度

### [rakuyomi](https://github.com/hanatsumi/rakuyomi)

- 這是一個抓網路上的漫畫的 KOReader plugin

- [安裝教學](https://github.com/hanatsumi/rakuyomi?tab=readme-ov-file#installation)

- 需要把設定檔放在 `koreader/data/dict` 
   
   ```json
   {
       "$schema": "https://github.com/hanatsumi/rakuyomi/releases/download/main/settings.schema.json",
       "source_lists": [
           "<your source list URL>"
       ],
       "languages": ["zh"]
   }
   ```

   {{< alert cardColor="#1E293B" iconColor="#1E293B" textColor="#1E293B">}}
   source_lists 裡面的網址可以用https://raw.githubusercontent.com/Skittyblock/aidoku-community-sources/gh-pages/index.min.json

   中文的話可以用 manhuagui 當作來源
   {{< /alert >}}



- 如果也想要在網頁的 KOReader 也用的話，他的 plugin folder 在 `volume/config/.config/koreader/plugins`