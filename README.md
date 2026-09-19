# Personal Nix packages

tignear の個人用 Nix パッケージ集。各プロジェクトに Nix 設定を追加せずに利用できます。
Nix の `nix-command` と `flakes` 機能が必要です。

## mbx

[mr-boxington](https://github.com/jdx/mr-boxington) 1.14.0 の公式バイナリをパッケージ化しています。
対応環境: x86_64-linux / aarch64-linux。

一度だけ実行:

```sh
nix run github:tignear/nix-packages#mbx -- --help
```

任意のプロジェクトで一時的に利用:

```sh
cd /path/to/project
nix shell github:tignear/nix-packages#mbx
mbx --help
```

ユーザー環境にインストール:

```sh
nix profile add github:tignear/nix-packages#mbx
```

ローカルでビルド・動作確認:

```sh
nix build .#mbx
nix run .#mbx -- --version
```

`pkgs/mbx/default.nix` にバージョンとアーキテクチャ別のハッシュを定義し、
`flake.lock` で nixpkgs を固定しています。
