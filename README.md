# Changelog release

This GitHub Action reads a CHANGELOG file according to the [KeepAChangelog](https://keepachangelog.com/) format and
outputs the content.

You can fill your release content from your changelog file.

```yml
    - name: Read the changelog
      id: changelog
      uses: 3liz/changelog-release@X.Y.Z

    - name: Create release on GitHub
      uses: ncipollo/release-action@vX.Y.Z
      with:
        body: ${{ steps.changelog.outputs.markdown }}
        token: ${{ secrets.BOT_HUB_TOKEN }}
        allowUpdates: true
```

## Inputs

| Input                  | Description                                                                     | Default value                                  |
|------------------------|---------------------------------------------------------------------------------|------------------------------------------------|
| TAG_NAME               | The tag to look in the changelog file                                           | Default to a current GitHub tag if present     |
| INPUT_CHANGELOG_FILE   | The file to parse                                                               | Default to CHANGELOG.md in the root folder     |
| ADD_EMOJIS             | If emoji must be inserted in the output                                         | Default to True                                |
| EMOJI_END_OF_LINE      | Emoji at the beginning or end of line                                           | Default to False, so the beginning of the line |
| ADD_RAW_CHANGELOG_LINK | If a link to GitHub website must be added between this tag and the previous one | Default to True                                |

## Outputs

| Output                 | Description               |
|------------------------|---------------------------|
| markdown               | The changelog as Markdown |

## Credits

In the backend, it's using the Python library [KeepAChangelog](https://github.com/Colin-b/keepachangelog)

## Testing

There isn't any unittests for now.

```bash
INPUT_CHANGELOG_FILE=tests/fixtures/CHANGELOG.md INPUT_TAG_NAME=10.0.1 ./application/main.py
```