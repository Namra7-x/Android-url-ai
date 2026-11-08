# GitHub-hosted setup

No local Android phone, ADB, APK upload or self-hosted runner is required.

1. Open the repository's **Actions** tab.
2. Select **Android URL Atlas CI/CD**.
3. Click **Run workflow**.
4. Select `all`, `chatgpt`, `claude` or `gemini`.
5. Start the workflow and follow its job logs.
6. Download the generated artifact from the completed run, or inspect committed `reports/` and `data/history/`.

The workflow also runs automatically every six hours and when relevant source/configuration files change.

## APK source

The default downloader is EFF apkeep using APKPure. APKPure is a third-party mirror and apkeep explicitly warns that it should be used only for research. The pipeline checks the package name and the signing-certificate SHA-256 before accepting a downloaded APK. An unrecognised signature stops the scan.

For direct Google Play download, add Actions secrets named `GOOGLE_PLAY_EMAIL` and `GOOGLE_PLAY_AAS_TOKEN`, then set the repository variable `APK_DOWNLOAD_SOURCE` to `google-play`. This is optional and requires you to obtain the token independently.

## Where results appear

- GitHub Actions run logs show download, verification and analysis steps.
- Workflow artifacts retain reports and analysis evidence for 30 days.
- `reports/` and `data/history/` are committed automatically after successful scans.
