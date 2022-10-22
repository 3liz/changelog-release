# Changelog release

This GitHub Action reads a CHANGELOG file according to the [KeepAChangelog](https://keepachangelog.com/) format and
outputs the content.

You can fill your release content from your changelog file.

```yml
    - name: Read the changelog
      id: changelog
      uses: 3liz/changelog-release@0.2.0

    - name: Create release on GitHub
      uses: ncipollo/release-action@v1.10.0
      with:
        body: ${{ steps.changelog.outputs.markdown }}
        token: ${{ secrets.BOT_HUB_TOKEN }}
        allowUpdates: true
```

## Inputs

| Input                  | Description                                                                     | Default value                                  |
|------------------------|---------------------------------------------------------------------------------|------------------------------------------------|
| TAG_NAME               | The tag to look in the changelog file                                           | Default to a current GitHub tag if present     |
| CHANGELOG_FILE         | The file to parse                                                               | Default to CHANGELOG.md in the root folder     |
| ADD_EMOJIS             | If emoji must be inserted in the output                                         | Default to True                                |
| EMOJI_END_OF_LINE      | Emoji at the beginning or end of line                                           | Default to False, so the beginning of the line |
| ADD_RAW_CHANGELOG_LINK | If a link to GitHub website must be added between this tag and the previous one | Default to True                                |

## Credits

In the backend, it's using the Python library [KeepAChangelog](https://github.com/Colin-b/keepachangelog)
